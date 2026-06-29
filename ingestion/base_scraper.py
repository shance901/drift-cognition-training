"""
Base scraper with retry logic, rate-limiting, and shared session management.
All source-specific scrapers inherit from BaseScraper.
"""

import time
import logging
from abc import ABC, abstractmethod
from typing import Any

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from config import SCRAPER

logger = logging.getLogger(__name__)


class BaseScraper(ABC):
    source_name: str = "base"

    def __init__(self):
        self.session = self._build_session()

    def _build_session(self) -> requests.Session:
        session = requests.Session()
        retry = Retry(
            total=SCRAPER.max_retries,
            backoff_factor=SCRAPER.backoff_factor,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET", "POST"],
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount("https://", adapter)
        session.mount("http://", adapter)
        session.headers.update({"User-Agent": SCRAPER.user_agent})
        return session

    def get(self, url: str, **kwargs) -> requests.Response:
        time.sleep(SCRAPER.request_delay_seconds)
        response = self.session.get(url, timeout=SCRAPER.timeout_seconds, **kwargs)
        response.raise_for_status()
        return response

    def post(self, url: str, **kwargs) -> requests.Response:
        time.sleep(SCRAPER.request_delay_seconds)
        response = self.session.post(url, timeout=SCRAPER.timeout_seconds, **kwargs)
        response.raise_for_status()
        return response

    @abstractmethod
    def fetch_listings(self) -> list[dict[str, Any]]:
        """
        Return a list of raw parcel dicts with at minimum:
          - source (str)
          - raw_parcel_id (str | None)
          - title (str)
          - url (str)
          - raw_data (dict)
        """
        ...

    def run(self) -> list[dict[str, Any]]:
        logger.info("Starting ingestion: %s", self.source_name)
        try:
            listings = self.fetch_listings()
            logger.info("%s: collected %d listings", self.source_name, len(listings))
            return listings
        except Exception:
            logger.exception("Ingestion failed for %s", self.source_name)
            return []
