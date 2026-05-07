# Operations KPI Automation — SLA & Backlog Analytics

## Problem This Solves

Ops-heavy teams lose control when SLA breaches, backlog, and team-level performance are tracked manually or only reviewed after escalation. The problem is turning ticket lifecycles into a daily operating dashboard.

## How It Helps

- Generates a realistic support/ops ticket dataset and computes SLA compliance, backlog trends, breach drivers, and team-level scorecards.
- Gives founders and ops leads a starter reporting layer for staffing, escalation, process quality, and customer experience decisions.
- Exports BI-ready datasets that can be loaded into Tableau or adapted to another dashboard layer.

## When To Fork This

- Fork this if you run support, onboarding, sales ops, shipment ops, training ops, or any queue-based team.
- Fork it when leadership asks which team, priority, or process is driving SLA pain and no one has a clean answer.
- Adapt the team names, SLA thresholds, backlog logic, breach definitions, and dashboard views to your own workflow.

**End-to-end operational analytics pipeline** tracking 80,000 ticket 
lifecycles across 5 teams. Monitors SLA compliance, identifies breach 
drivers, and surfaces backlog trends for operational decision-making.

Built to simulate the kind of self-serve reporting infrastructure that 
ops and support teams rely on to manage performance without depending 
on ad hoc data pulls.

---

## Use This In Your Company

This repo is designed to be forked into an internal company workflow. Fork it, replace the sample inputs with your company context, and keep only the parts that match your operating cadence. No permission request or sales call is needed before using it; the repo is the handoff. Check the license if you plan to redistribute your version.

- Use it as an operations dashboard starter for support, onboarding, fulfillment, sales ops, or service delivery teams.
- Keep the logic: tickets -> SLA compliance -> backlog -> breach drivers -> team scorecards.
- Replace sample queues, teams, priorities, and SLA thresholds with your company workflow.

## Minimum Edits To Make It Yours

Change these first:

| Edit | Where | Why |
|---|---|---|
| Replace ticket or operations data. | `data/ops_tickets.csv` | This drives SLA, backlog, breach, and team-level metrics. |
| Update team names and lifecycle fields. | `src/analysis.py` and data columns | Makes the KPI logic match your org and workflow. |
| Tune SLA and priority thresholds. | `src/analysis.py` | Changes what the system marks as urgent, delayed, or breached. |
| Regenerate KPI CSVs and dashboard image. | `data/*.csv` and `dashboard/SLA_Backlog_Dashboard.png` | Keeps operating outputs aligned with your data. |

You can leave the dashboard structure, analysis flow, and generated-output names alone on the first fork. First map your fields; then tune SLA definitions.

## Key Results

| Metric | Value |
|---|---|
| Tickets Analyzed | 80,000 |
| SLA Compliance Rate | 90.4% |
| Average Backlog | 1,213 tickets |
| Teams Monitored | Onboarding, Sales Ops, Shipment, Support, Training |

---

## What It Does

- **SLA breach detection** — flags tickets exceeding thresholds by team and priority
- **Backlog trend monitoring** — moving average + monthly volume to isolate demand spikes
- **Team-level compliance scoring** — ranked view to identify lowest-performing queues
- **Breach root cause view** — individual ticket drill-down with breach hours by department

---

## Dashboard Preview

![SLA & Backlog Dashboard](dashboard/SLA_Backlog_Dashboard.png)

🔗 **[Open Live Tableau Dashboard](https://public.tableau.com/views/SLABacklog/Dashboard1)**

---

## Tech Stack

`Python` · `Pandas` · `Tableau Public` · `Git`

**Pipeline:**
1. Synthetic data generation with weighted SLA distribution
2. KPI computation and breach modeling
3. Automated export of BI-ready datasets
4. Tableau dashboard visualization

---

## How to Run

```bash
python3 src/generate_data.py
python3 src/analysis.py
```

---

## Strategic Context

Simulates real-world operational reporting workflows used in 
large-scale e-commerce and ops-heavy startups where support team 
SLA visibility drives staffing, escalation, and process decisions.

---

*Part of a founder/operator toolkit for people building practical startup operating systems.*  
*[← Back to Profile](https://github.com/shubham1502-hue)*
