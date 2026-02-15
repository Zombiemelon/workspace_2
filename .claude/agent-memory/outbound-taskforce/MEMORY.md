# Outbound Taskforce Agent Memory

## STRICT RULES

- **NEVER delete or remove anything (cards, dashboards, records, leads) without the user's explicit permission.** Always ask first before any destructive operation.

## Key Tables
- `salesforce_current.leads` - main lead data, outbound filter via JOIN to `views.definition_lead_source` WHERE `source_group = 'Outbound'`
- `salesforce_current.tasks` - BDM activity tracking; meetings = subject='meeting' AND status='Completed'
- `salesforce_current.opportunities` - opp tracking; `owner_full_name_c` for BDM name, `client_classification_c` for size tier
- `views.definition_lead_source` - canonical inbound/outbound classification (19 outbound sources as of Feb 2026)
- `salesforce_current.users` - needed for tasks (tasks use `owner_id`, not `owner_full_name_c`)

## Salesforce Field Notes
- Lead conversion date field is `converted_date` (NOT `lead_converted_date_c`; that field does not exist)
- Lead timestamp fields: `contacted_timestamp_c`, `in_conversation_timestamp_c`, `in_conversation_time_stamp_c` (duplicate!), `lead_converted_timestamp_c`, `lead_converted_time_stamp_c` (duplicate!)
- Opp size: `client_classification_c` = 'Large Enterprise (51+ orders)', 'Store Large Enterprise', 'Medium Business (16-50 orders)', 'Small Business (5-15 orders)', 'Micro-Business (0-4 orders)'
- `client_priority_c` NULL on 73%+ of opps; `probability_weighted_revenue_c` empty on 98%
- Opp stages: 'In Conversation', 'First Proposal Sent', 'Agreement with client on pricing', 'Negotiation', 'Deal Done', 'Deal Lost'

## Query Patterns That Work
- Outbound filter: Always JOIN to `views.definition_lead_source` WHERE `source_group = 'Outbound'` (includes non-obvious sources like 'Employee Referral', 'Inbound: Seamless', 'BDM Referral')
- Meeting counting: Two paths (opp_meetings via what_id + lead_meetings via who_id), UNION DISTINCT, COUNT(DISTINCT task_id)
- BDM name: `owner_full_name_c` from opps, but `users.name` via `owner_id` JOIN from tasks

## Data Quality Issues
- **Meeting under-logging is severe**: 13 meetings Jan-Feb 2026 vs 34 opps. Aram Jaber = 92% of meetings. Most BDMs log zero.
- Many converted leads skip 'In conversation' stage entirely
- Some leads have in_conversation_timestamp_c AFTER converted_date (negative velocity)
- Feb 2026: 44% DQ rate on 373 leads from 'Outbound: Own research'
- Activation: orders table has `client_order_id`/`external_order_id` (NOT `client_id`). Link path needs investigation.

## Baseline Metrics (Feb 2026)
- H2 2025-Feb 2026 win rate: Micro 47.1% (n=17 resolved), M/L/S 18.9% (n=37 resolved)
- Plan: 20 opps/mo, 60 meetings/mo, mix 4L/3M/5S/8Micro
- Jan 2026: 20 opps (100%), 4 meetings (7%). Feb MTD: 14 opps (107% prorated), 9 meetings (32% prorated)

## CSV Audit Insights (Feb 2026)
- **Khushi CSV vs SF audit (Feb 13)**: 47 claimed leads, only 15 created in Feb 9-15 window, 4 not in SF at all
- Worldef event leads (Taager/Khalaf, Dubaiaradepo, Nexport, Centre Point) never entered in SF
- Lemlist tasks are the reliable "contacted" evidence; many CSV "contacted" claims have no Lemlist tasks
- Leads with NULL `lead_source` (e.g., Jwpei) won't show in outbound reporting -- tag immediately
- Khushi's only logged SF meeting (Feb 10) was on inbound OnCargo opp, not any outbound CSV lead
- `in_conversation_timestamp_c` rarely gets updated even when email replies come in via Lemlist
- Some BDMs recycle old leads (2022 vintage) and report them as current week activity
- Full report: `projects/outbound_taskforce/khushi_csv_vs_sf_audit_2026-02-13.md`
