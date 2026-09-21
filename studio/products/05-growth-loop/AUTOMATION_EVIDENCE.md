# Weekly automation evidence snapshot

Inspection date: 2026-09-21

This is a sanitized, portable record of the local host automation definition.
It intentionally omits the local thread identifier and other host runtime
fields. The original file remains outside the repository at:

`/Users/batmanosama/.codex/automations/weekly-airpods-ad-scan/automation.toml`

## Recorded configuration

- Automation ID: `weekly-airpods-ad-scan`
- Kind: heartbeat
- Name: Weekly AirPods Ad Scan
- Status: ACTIVE
- Schedule: `FREQ=WEEKLY;BYDAY=MO;BYHOUR=8;BYMINUTE=0`
- Query: AirPods, US, ACTIVE, ALL, limit 50
- Reporting: inline bounded top-50 scan report
- Safety: no create, edit, archive, pause, or delete operations
- Failure rule: report the exact blocker without guessing or fabricating

## Integrity

The inspected local file had SHA-256:

`7dd0627198f5c57ce529c95f1c9cce551fd245b008ae936e5f9347806a45c34c`

That hash is evidence of the version inspected on the date above. It is not a
claim that the mutable host automation is still unchanged. Re-read and rehash
the live file before relying on this record operationally.

## Known limitation

The automation prompt compares against the older 49-row `.zcode` baseline and
does not explicitly require persistence of a dated unique-ID snapshot. Update
that prompt before claiming fully automated longitudinal collection.
