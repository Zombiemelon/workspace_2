# Outbound Taskforce Agent Memory

## Key Tables
- `salesforce_current.leads` - main lead data, outbound filter: `lead_source LIKE 'Outbound%'`
- `salesforce_current.tasks` - BDM activity tracking
- `views.definition_lead_source` - canonical inbound/outbound classification
- `clay_score__c` - Clay enrichment score field on leads

## Salesforce Field Notes
<!-- Add field behavior discoveries here -->

## Query Patterns That Work
<!-- Add successful query patterns here -->

## Data Quality Issues
<!-- Add data quality findings here -->
