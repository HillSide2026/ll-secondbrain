# Matters

## Status layout

```
05_MATTERS/
├── OPEN/
│   ├── essential/
│   ├── strategic/
│   ├── standard/
│   └── parked/
├── PENDING/
└── CLOSED/
```

`OPEN` subfolders map to the delivery status values (essential, strategic, standard, parked).

## Matter template

```
{MATTER_ID}/

├── 00_META.md
STATUS:                        # OPEN/PENDING/CLOSED
DELIVERY_STATUS:               # essential/strategic/standard/parked
PRACTICE_AREA:                 # corporate / contract / compliance / transaction

├── 01_OPS/
│   ├── TASKS.md               # task table (stateful)
│   ├── DEADLINES.md           # hard dates + consequences
│   ├── NEXT_ACTIONS.md        # top 5–10 next moves
│   └── STATUS_SUMMARY.md      # one-page “where we are”

├── 02_WORK/
│   ├── 01_INTAKE/
│   ├── 02_TRIAGE/
│   ├── 03_RESEARCH/
│   ├── 04_ANALYSIS/
│   ├── 05_DRAFTS/
│   ├── 06_REVIEW/
│   ├── 07_DECISIONS/
│   ├── 08_OUTPUTS/
│   └── 09_RUN_LOGS/
```
