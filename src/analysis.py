import pandas as pd
import numpy as np
import os


def analyze_ops_data(input_path, output_dir):

    # -----------------------------
    # Load Data
    # -----------------------------
    df = pd.read_csv(input_path)

    df["created_at"] = pd.to_datetime(df["created_at"])
    df["resolved_at"] = pd.to_datetime(df["resolved_at"])

    # -----------------------------
    # Derived Columns
    # -----------------------------
    df["sla_met"] = np.where(
        df["actual_resolution_hours"] <= df["sla_target_hours"],
        1,
        0
    )

    df["breach_hours"] = np.where(
        df["actual_resolution_hours"] > df["sla_target_hours"],
        df["actual_resolution_hours"] - df["sla_target_hours"],
        0
    )

    df["month"] = df["created_at"].dt.to_period("M").astype(str)

    # -----------------------------
    # 1. KPI SUMMARY
    # -----------------------------
    total_tickets = len(df)
    total_breaches = (df["sla_met"] == 0).sum()
    overall_sla = df["sla_met"].mean()

    monthly_backlog = (
        df.groupby("month")["backlog_flag"]
        .sum()
    )

    avg_monthly_backlog = monthly_backlog.mean()

    kpi_summary = pd.DataFrame({
        "metric": [
            "Overall SLA Compliance %",
            "Total Tickets",
            "Average Monthly Backlog"
        ],
        "value": [
            round(overall_sla, 4),
            total_tickets,
            round(avg_monthly_backlog, 2)
        ]
    })

    # -----------------------------
    # 2. SLA BY TEAM
    # -----------------------------
    sla_by_team = (
        df.groupby("team")
        .agg(
            total_tickets=("ticket_id", "count"),
            sla_met=("sla_met", "sum"),
            avg_resolution_hours=("actual_resolution_hours", "mean"),
            total_breaches=("sla_met", lambda x: (x == 0).sum())
        )
        .reset_index()
    )

    sla_by_team["sla_compliance_rate"] = (
        sla_by_team["sla_met"] / sla_by_team["total_tickets"]
    )

    sla_by_team["avg_resolution_hours"] = (
        sla_by_team["avg_resolution_hours"].round(2)
    )

    sla_by_team["sla_compliance_rate"] = (
        sla_by_team["sla_compliance_rate"].round(4)
    )

    # -----------------------------
    # 3. BACKLOG TREND
    # -----------------------------
    backlog_trend = (
        df.groupby("month")
        .agg(
            total_tickets=("ticket_id", "count"),
            backlog_count=("backlog_flag", "sum")
        )
        .reset_index()
    )

    backlog_trend["backlog_rate"] = (
        backlog_trend["backlog_count"] /
        backlog_trend["total_tickets"]
    ).round(4)

    # -----------------------------
    # 4. TOP SLA BREACHES
    # -----------------------------
    top_sla_breaches = (
        df[df["breach_hours"] > 0]
        .sort_values("breach_hours", ascending=False)
        .head(10)
        [
            [
                "ticket_id",
                "team",
                "priority",
                "actual_resolution_hours",
                "sla_target_hours",
                "breach_hours"
            ]
        ]
    )

    latest_backlog = backlog_trend.iloc[-1]["backlog_count"] if not backlog_trend.empty else 0
    first_backlog = backlog_trend.iloc[0]["backlog_count"] if not backlog_trend.empty else 0
    backlog_delta = latest_backlog - first_backlog
    top_breach = top_sla_breaches.iloc[0] if not top_sla_breaches.empty else None

    # -----------------------------
    # Export
    # -----------------------------
    os.makedirs(output_dir, exist_ok=True)

    kpi_summary.to_csv(f"{output_dir}/kpi_summary.csv", index=False)
    sla_by_team.to_csv(f"{output_dir}/sla_by_team.csv", index=False)
    backlog_trend.to_csv(f"{output_dir}/backlog_trend.csv", index=False)
    top_sla_breaches.to_csv(f"{output_dir}/top_sla_breaches.csv", index=False)
    write_executive_summary(
        output_path=f"{output_dir}/executive_summary.md",
        total_tickets=total_tickets,
        total_breaches=total_breaches,
        overall_sla=overall_sla,
        avg_monthly_backlog=avg_monthly_backlog,
        backlog_delta=backlog_delta,
        top_breach=top_breach,
    )

    # -----------------------------
    # Sanity Print
    # -----------------------------
    print("-- Analysis Summary --------------------------")
    print(f"Total Tickets       : {total_tickets:,}")
    print(f"Total Breaches      : {total_breaches:,}")
    print(f"Overall Compliance  : {round(overall_sla*100,2)}%")
    print(f"Avg Monthly Backlog : {round(avg_monthly_backlog,2)}")
    print(f"Top Breach (hrs)    : {round(top_sla_breaches['breach_hours'].max(),2)}")


def write_executive_summary(
    output_path,
    total_tickets,
    total_breaches,
    overall_sla,
    avg_monthly_backlog,
    backlog_delta,
    top_breach,
):
    backlog_direction = "increased" if backlog_delta > 0 else "decreased" if backlog_delta < 0 else "stayed flat"

    if top_breach is not None:
        top_driver = (
            f"{top_breach['team']} had the largest sampled SLA breach: "
            f"{round(top_breach['breach_hours'], 2)} hours over target on ticket {top_breach['ticket_id']}."
        )
        recommended_action = (
            f"Review the {top_breach['team']} queue first, then inspect similar "
            f"{top_breach['priority']} priority tickets for routing, staffing, or escalation gaps."
        )
    else:
        top_driver = "No SLA breaches were found in the current dataset."
        recommended_action = "Keep the current SLA operating cadence and monitor backlog trend weekly."

    lines = [
        "# Operations KPI Executive Summary",
        "",
        "## KPI snapshot",
        "",
        f"- Total tickets analyzed: {total_tickets:,}",
        f"- SLA compliance: {overall_sla:.2%}",
        f"- Total SLA breaches: {total_breaches:,}",
        f"- Average monthly backlog: {round(avg_monthly_backlog, 2):,}",
        "",
        "## Backlog trend",
        "",
        f"Backlog {backlog_direction} by {abs(int(backlog_delta)):,} tickets from the first to the latest month in the sample.",
        "",
        "## Top breach driver",
        "",
        top_driver,
        "",
        "## Recommended action",
        "",
        recommended_action,
        "",
    ]

    with open(output_path, "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines))


if __name__ == "__main__":

    analyze_ops_data(
        input_path="data/ops_tickets.csv",
        output_dir="data"
    )
