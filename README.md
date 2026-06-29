# Municipal Surplus Land Platform

An automated, AI-powered pipeline for sourcing and evaluating Escambia County
(Pensacola, FL) municipal surplus land and tax deed clearing lots.

## Architecture

```
┌─────────────────┐      ┌──────────────────┐      ┌──────────────────┐      ┌─────────────────┐
│  Data Ingestion │ ───> │ Structural Parse │ ───> │   AI Enrichment  │ ───> │ Action Delivery │
│ (Target Sites)  │      │  (GIS & Parcel)  │      │ (FR 4.0 Checks)  │      │(Dashboard/Alert)│
└─────────────────┘      └──────────────────┘      └──────────────────┘      └─────────────────┘
```

## Stage 1 — Data Ingestion

Five scrapers run daily against hyper-local government sources:

| Scraper | Source | Data |
|---|---|---|
| `BidEscambiaScraper` | BidEscambia | Active tax deed & surplus auctions |
| `LienHubScraper` | LienHub | Tax lien certificates (FL) |
| `GovDealsScraper` | GovDeals | Government surplus real property |
| `EscambiaSurplusScraper` | myescambia.com | County surplus property lists + PDFs |
| `FlDepScraper` | FL DEP Division of State Lands | State parcel releases, NW Florida |

## Stage 2 — Structural Parsing & GIS

- Parcel ID extracted and normalised to `XX-XXXX-XXX-XXX` canonical form
- Escambia County ArcGIS REST API queried for ownership, lot dimensions,
  zoning, FEMA flood zone, and wetland designations
- Square footage, address, and assessed value extracted from raw text

## Stage 3 — AI Enrichment (FR 4.0)

Each parcel passes through four sequential Claude API prompts:

1. **Zoning Analysis** — by-right uses, density, quadplex eligibility, setbacks
2. **Environmental Analysis** — flood risk, wetland proximity, pervious space
3. **Compliance Filter** — title concerns, access issues, municipal liens, unpermitted structures
4. **Composite Summary** — investment tier, composite score (0–100), alert text

Before calling the AI, a deterministic pre-filter (`compliance_filter.py`) applies
hard-coded Escambia County regulatory rules to cheaply reject obviously unbuildable
or high-liability parcels.

**High-priority zoning codes:** `RM-1`, `RM-2`, `RM-3`, `MU-U`, `MU-S`, `HC`

**Alert example:**
```
SURPLUS LAND ALERT — Escambia County
Parcel: 00-0000-000-000
Address: 1401 Cervantes St, Pensacola FL 32501
Score: 82/100  |  Tier 1 — Immediate Action

Parcel 00-0000-000-000 has entered the Tax Deed Clearing list.
Location: Urban Pensacola boundary. Zoning: RM-2.
By-Right Capacity: High. Estimated Pervious Space Margin: 38%.
```

## Stage 4 — Action Delivery

- **SQLite / PostgreSQL** — all enriched parcels persisted with full JSON blobs
- **Slack** — formatted alert posted to configurable channel
- **Twilio SMS** — alert text delivered to configured phone number
- **Webhook** — JSON payload to Zapier, n8n, Make, or any HTTP endpoint
- **Rich Terminal Dashboard** — interactive table with drill-down

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env
# Edit .env — add ANTHROPIC_API_KEY at minimum
```

## Usage

```bash
# Run the pipeline once immediately
python pipeline.py

# Run on a daily schedule (default 06:00)
python scheduler.py
python scheduler.py --time 08:00
python scheduler.py --run-now    # immediate one-shot execution

# View the dashboard
python -m delivery.dashboard
python -m delivery.dashboard --min-score 60
python -m delivery.dashboard --detail 12-3456-789-012

# Run tests
python -m pytest tests/ -v
```

## Project Structure

```
├── config/
│   └── settings.py          # All config: thresholds, zoning codes, URLs
├── ingestion/
│   ├── base_scraper.py      # Base class with retry/rate-limit logic
│   ├── bidescambia.py
│   ├── lienhub.py
│   ├── govdeals.py
│   ├── escambia_surplus.py  # HTML tables + PDF extraction
│   └── fl_dep.py
├── parsing/
│   ├── parcel_extractor.py  # ID normalisation, field extraction
│   └── gis_client.py        # ArcGIS REST queries
├── enrichment/
│   ├── prompt_matrix.py     # Four-stage Claude prompt templates
│   ├── ai_analyst.py        # Anthropic API calls
│   └── compliance_filter.py # FR 4.0 deterministic pre-filter
├── delivery/
│   ├── database.py          # SQLAlchemy ORM + upsert logic
│   ├── notifier.py          # Slack / Twilio / Webhook dispatch
│   └── dashboard.py         # Rich terminal dashboard
├── pipeline.py              # Main orchestrator (Stages 1–4)
├── scheduler.py             # Daily cron wrapper
└── tests/
    ├── test_parcel_extractor.py
    ├── test_compliance_filter.py
    └── test_notifier.py
```

## Configuration

All thresholds are set in `config/settings.py` and override-able via `.env`:

| Setting | Default | Description |
|---|---|---|
| `min_lot_sqft` | 4,000 | Reject undersized lots |
| `quadplex_threshold_sqft` | 7,200 | By-right quadplex minimum |
| `high_risk_flood_zones` | AE, AH, AO, VE, V | Auto-caution FEMA zones |
| `min_alert_score` | 60 | Minimum composite score to trigger alert |
| `AI.model` | `claude-sonnet-4-6` | Claude model for enrichment |
