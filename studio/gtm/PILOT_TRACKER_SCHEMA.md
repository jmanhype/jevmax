# Pilot tracker schema

Use this schema before adding real leads. Do not fabricate company names,
leads, or outcomes.

## CSV columns

| Column | Type | Example | Notes |
|---|---|---|---|
| `opportunity_id` | string | `OPP-001` | internal ID |
| `created_date` | date | `2026-09-21` | first qualification date |
| `channel` | enum | `email` | email, dm, referral, inbound, event |
| `category` | string | `phone accessories` | client market |
| `product_focus` | string | `wired earbuds` | primary product |
| `stage` | enum | `qualified` | new, researching, qualified, call_scheduled, proposal_sent, won, lost |
| `next_action` | string | `send sales kit` | concrete action |
| `next_action_date` | date | `2026-09-22` | when action is due |
| `estimated_monthly_ad_spend` | number | 3000 | use client-reported value |
| `account_audit_available` | boolean | true | read-only access confirmed |
| `identity_asset_available` | boolean | false | approved character or client seed |
| `blockers` | string | `pixel not firing` | semicolon-separated |
| `outcome` | enum | empty | won, lost, postponed |
| `loss_reason` | string | `budget timing` | required when lost |
| `evidence_note` | string | `scan preview sent` | factual note only |

## Rules

1. Never invent a company or contact.
2. Never record a performance claim without live measured evidence.
3. Every `qualified` opportunity needs a concrete next action and date.
4. Every `won` pilot must cite a signed or written approval artifact.
5. Every `lost` pilot must include a loss reason.

## Initial target categories

- phone accessories
- home fitness accessories
- personal care tools
- pet products
- kitchen gadgets
- travel gear
- sleep products
- hobby and craft kits

These are target categories, not claimed leads.
