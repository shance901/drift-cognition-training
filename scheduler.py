"""
Daily pipeline scheduler.

Runs the full pipeline on a configurable cron-style schedule.
Default: every day at 06:00 local time.

Usage:
    python scheduler.py                  # run every day at 06:00
    python scheduler.py --run-now        # execute immediately then exit
    python scheduler.py --time 08:30     # custom daily time (HH:MM)
"""

import argparse
import logging
import sys
import time

import schedule

from pipeline import run_pipeline

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(name)s — %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    stream=sys.stdout,
)
logger = logging.getLogger("scheduler")


def _job():
    try:
        run_pipeline()
    except Exception:
        logger.exception("Pipeline run failed — will retry at next scheduled interval")


def main():
    parser = argparse.ArgumentParser(description="Municipal Surplus Land Platform Scheduler")
    parser.add_argument(
        "--time",
        default="06:00",
        help="Daily run time in HH:MM (24h) format (default: 06:00)",
    )
    parser.add_argument(
        "--run-now",
        action="store_true",
        help="Execute one pipeline run immediately then exit",
    )
    args = parser.parse_args()

    if args.run_now:
        logger.info("--run-now flag set; executing pipeline immediately")
        _job()
        return

    schedule.every().day.at(args.time).do(_job)
    logger.info("Scheduler started — pipeline will run daily at %s", args.time)
    logger.info("Press Ctrl+C to stop")

    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == "__main__":
    main()
