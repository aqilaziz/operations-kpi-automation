# How to fork and use Operations KPI Command Center

This guide is for a founder or operator who wants to adapt the repo without turning it into a generic portfolio project.

## First pass

1. Fork the repo.
2. Rename it for your company or operating workflow.
3. Read the README Quick Start section.
4. Replace sample inputs, templates, or context files with your own company context.
5. Run the workflow if executable, or copy the first template if it is a playbook.
6. Open the main output listed in the README before changing deeper logic.

## Company fork path

1. Click Fork.
2. Rename the repo if needed.
3. Replace `data/ops_tickets.csv` with your ticket export.
4. Update SLA thresholds and team mappings in `src/analysis.py`.
5. Run the analysis before the weekly operations review.
6. Move outputs into Google Sheets, Notion, Airtable, Linear, Asana, ClickUp, or your BI tool.

## Non-technical path

- Replace one CSV: `data/ops_tickets.csv`.
- Edit one threshold section in `src/analysis.py` if needed.
- Run two commands.
- Read one output first: `data/kpi_summary.csv`.

## Data safety

The included sample data is synthetic, anonymized, or template-only unless a public source is explicitly documented. Do not commit private customer, prospect, employee, investor, borrower, merchant, payment, or company data to a public fork.

## Tools to connect later

Start with files first. After the workflow is useful, connect outputs to Google Sheets, Notion, Airtable, HubSpot, Pipedrive, Attio, Linear, Asana, ClickUp, Slack, or your internal ops tracker where relevant.
