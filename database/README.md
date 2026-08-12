# Small Business Grants & Funding Database

A SQLite database identifying grant and funding programs relevant to:

1. **Cybersecurity** — R&D/innovation funding (e.g., SBIR/STTR cybersecurity topics)
2. **Cybersecurity protection** — direct compliance/protection funding (e.g., SOC services, CMMC tooling, pen testing, certification)
3. **Small business general** — broader grants and funding not specific to cybersecurity (export, microenterprise, women/minority-owned, corporate-sponsored)

## Contents

```
database/
├── schema.sql                  # Table/view definitions
├── data/
│   ├── seed_data.json          # Source-of-truth grant records (human-editable)
│   └── grants_export.csv       # Flat CSV export (regenerate with query.py --export csv)
├── scripts/
│   ├── build_database.py       # Builds grants.db from schema.sql + seed_data.json
│   └── query.py                # CLI to search/filter/export the database
└── grants.db                   # Built SQLite database (regenerate any time)
```

## Schema

- **`grants`** — one row per program: name, provider, `provider_type` (federal/state/private/nonprofit/portal), `primary_category` (`cybersecurity` / `cybersecurity_protection` / `small_business_general`), description, eligibility, funding amount (text + numeric min/max where known), geographic scope, application status, how to apply, application URL, source URL, and `last_verified` date.
- **`grant_tags`** — many-to-many tags (e.g. `federal`, `rolling`, `women-owned`, `SBIR`, `pass-through`) for flexible filtering.
- **`grants_with_tags`** view — grants joined with a comma-separated tag list.

## Usage

Rebuild the database from the seed data at any time:

```bash
python3 scripts/build_database.py
```

Query it:

```bash
# List everything
python3 scripts/query.py --list

# Filter by category
python3 scripts/query.py --category cybersecurity
python3 scripts/query.py --category cybersecurity_protection
python3 scripts/query.py --category small_business_general

# Filter by provider type
python3 scripts/query.py --provider-type federal
python3 scripts/query.py --provider-type private

# Keyword search (name/description/notes)
python3 scripts/query.py --keyword "penetration test"

# Filter by tag
python3 scripts/query.py --tag women-owned
python3 scripts/query.py --tag SBIR

# Export results to CSV
python3 scripts/query.py --category cybersecurity --export csv > cyber_grants.csv
```

Or query the SQLite file directly:

```bash
sqlite3 grants.db "SELECT name, provider, funding_amount_text FROM grants WHERE primary_category = 'cybersecurity_protection';"
```

## Adding / updating grants

Edit `data/seed_data.json` (one JSON object per grant, matching the `grants` table columns plus an optional `tags` array), then rerun `python3 scripts/build_database.py` to rebuild `grants.db`.

## Coverage notes (as of 2026-08-11)

- 24 programs seeded: 4 cybersecurity R&D/innovation, 9 cybersecurity protection/compliance, 11 general small-business grants.
- Several federal programs (SLCGP, PRIME, FAST, STEP) are **pass-through**: they fund state agencies or nonprofits, which then deliver services or sub-awards to small businesses. This is noted in each record's `notes` field — check the linked `source_url` for how to access the sub-award or service in your state.
- Grant programs, deadlines, and amounts change frequently. Each record has a `last_verified` date and a `source_url` citation — **verify current details on the official site before applying**, especially for anything with an older `last_verified` date after edits.
- This is a snapshot, not a live feed. Re-run web research periodically (or add new records to `seed_data.json`) to keep it current. `Grants.gov` is included as a discovery/alerting tool for ongoing monitoring of new federal opportunities.
