"""
Municipal Surplus Land Platform — Main Orchestration Pipeline

Executes the four stages sequentially:
  1. Data Ingestion    (all configured scrapers)
  2. Structural Parse  (parcel ID normalisation + GIS lookup)
  3. AI Enrichment     (compliance pre-filter + Claude analysis)
  4. Action Delivery   (database upsert + alert dispatch + dashboard)

Run directly:  python pipeline.py
"""

import logging
import sys
from datetime import datetime, timezone

from ingestion import ALL_SCRAPERS
from parsing import enrich_raw_listing, fetch_parcel_data_safe
from enrichment import pre_filter_parcels, enrich_parcels
from delivery import upsert_parcel, send_alert, send_daily_digest, mark_alert_sent

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(name)s — %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    stream=sys.stdout,
)
logger = logging.getLogger("pipeline")


def run_pipeline() -> list[dict]:
    """
    Execute the complete pipeline end-to-end.
    Returns the list of enriched parcel dicts produced during this run.
    """
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    logger.info("══════════ Pipeline run started  %s ══════════", run_id)

    # ──────────────────────────────────────────────────────────────
    # Stage 1 — Data Ingestion
    # ──────────────────────────────────────────────────────────────
    logger.info("Stage 1: Ingesting from %d sources", len(ALL_SCRAPERS))
    raw_listings: list[dict] = []
    for ScraperClass in ALL_SCRAPERS:
        scraper = ScraperClass()
        raw_listings.extend(scraper.run())

    logger.info("Stage 1 complete: %d raw listings", len(raw_listings))
    if not raw_listings:
        logger.warning("No listings ingested; exiting pipeline early")
        return []

    # ──────────────────────────────────────────────────────────────
    # Stage 2 — Structural Parsing and GIS Mapping
    # ──────────────────────────────────────────────────────────────
    logger.info("Stage 2: Parsing and GIS enrichment")
    parsed_parcels: list[dict] = []
    for listing in raw_listings:
        enriched = enrich_raw_listing(listing)
        if not enriched.get("parcel_id"):
            logger.debug("Skipping listing with no extractable parcel ID: %s", listing.get("title", ""))
            continue
        # GIS overlay
        gis_data = fetch_parcel_data_safe(enriched["parcel_id"])
        enriched.update(gis_data)
        parsed_parcels.append(enriched)

    logger.info("Stage 2 complete: %d parseable parcels", len(parsed_parcels))
    if not parsed_parcels:
        logger.warning("No parseable parcels after Stage 2; exiting pipeline early")
        return []

    # ──────────────────────────────────────────────────────────────
    # Stage 3 — AI Enrichment (with FR 4.0 compliance pre-filter)
    # ──────────────────────────────────────────────────────────────
    logger.info("Stage 3: Compliance pre-filter")
    ai_queue, filter_results = pre_filter_parcels(parsed_parcels)
    logger.info(
        "Stage 3: %d/%d parcels queued for AI enrichment",
        len(ai_queue),
        len(parsed_parcels),
    )

    enriched_results: list[dict] = []
    if ai_queue:
        logger.info("Stage 3: Running AI enrichment on %d parcels", len(ai_queue))
        enriched_results = enrich_parcels(ai_queue)
        logger.info("Stage 3 complete: %d parcels enriched", len(enriched_results))
    else:
        logger.warning("No parcels passed compliance filter; Stage 3 skipped")

    # ──────────────────────────────────────────────────────────────
    # Stage 4 — Action Delivery
    # ──────────────────────────────────────────────────────────────
    logger.info("Stage 4: Persisting and delivering alerts")
    alert_count = 0
    for result in enriched_results:
        record = upsert_parcel(result)
        if not record.alert_sent:
            delivered = send_alert(result)
            if delivered:
                mark_alert_sent(result["parcel_id"])
                alert_count += 1

    send_daily_digest(enriched_results)
    logger.info("Stage 4 complete: %d alert(s) sent", alert_count)
    logger.info("══════════ Pipeline run complete %s ══════════", run_id)

    return enriched_results


if __name__ == "__main__":
    results = run_pipeline()
    print(f"\nPipeline finished. Processed {len(results)} enriched parcel(s).")
    print("Run 'python -m delivery.dashboard' to view the dashboard.")
