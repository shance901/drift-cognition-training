"""
Scraper for the Escambia County Surplus Real Property portal.
The county posts surplus property lists as HTML tables and PDF attachments.
"""

import io
import logging
import re
from typing import Any

import PyPDF2
from bs4 import BeautifulSoup

from config import SOURCES
from .base_scraper import BaseScraper

logger = logging.getLogger(__name__)

_PARCEL_RE = re.compile(r"\b\d{2}[- ]\d{4}[- ]\d{3}[- ]\d{3}\b")


class EscambiaSurplusScraper(BaseScraper):
    source_name = "EscambiaCountySurplus"

    def fetch_listings(self) -> list[dict[str, Any]]:
        response = self.get(SOURCES.escambia_surplus)
        soup = BeautifulSoup(response.text, "lxml")

        listings: list[dict[str, Any]] = []

        # 1. Parse HTML tables directly on the page
        listings.extend(self._parse_html_tables(soup))

        # 2. Follow any PDF links and extract text from them
        pdf_links = soup.find_all(
            "a",
            href=re.compile(r"\.pdf$", re.I),
        )
        for link in pdf_links:
            href = link.get("href", "")
            if not href.startswith("http"):
                href = "https://www.myescambia.com" + href
            listings.extend(self._parse_pdf_link(href))

        return listings

    def _parse_html_tables(self, soup: BeautifulSoup) -> list[dict[str, Any]]:
        listings = []
        for table in soup.select("table"):
            headers = [th.get_text(strip=True).lower() for th in table.select("th")]
            for row in table.select("tr"):
                cells = [td.get_text(strip=True) for td in row.select("td")]
                if not cells:
                    continue
                row_text = " ".join(cells)
                parcel_match = _PARCEL_RE.search(row_text)
                raw_parcel_id = (
                    parcel_match.group(0).replace(" ", "-") if parcel_match else None
                )
                raw_data = dict(zip(headers, cells)) if headers else {"cells": cells}
                raw_data["text_snippet"] = row_text[:500]
                listings.append(
                    {
                        "source": self.source_name,
                        "raw_parcel_id": raw_parcel_id,
                        "title": f"County Surplus – {raw_parcel_id or cells[0][:60]}",
                        "url": SOURCES.escambia_surplus,
                        "raw_data": raw_data,
                    }
                )
        return listings

    def _parse_pdf_link(self, pdf_url: str) -> list[dict[str, Any]]:
        try:
            response = self.get(pdf_url)
            reader = PyPDF2.PdfReader(io.BytesIO(response.content))
            full_text = "\n".join(
                page.extract_text() or "" for page in reader.pages
            )
        except Exception:
            logger.warning("Could not parse PDF: %s", pdf_url)
            return []

        listings = []
        for match in _PARCEL_RE.finditer(full_text):
            parcel_id = match.group(0).replace(" ", "-")
            # Grab surrounding context
            start = max(0, match.start() - 100)
            end = min(len(full_text), match.end() + 200)
            snippet = full_text[start:end].replace("\n", " ").strip()

            listings.append(
                {
                    "source": self.source_name,
                    "raw_parcel_id": parcel_id,
                    "title": f"County Surplus PDF – {parcel_id}",
                    "url": pdf_url,
                    "raw_data": {"text_snippet": snippet, "pdf_url": pdf_url},
                }
            )

        logger.debug(
            "EscambiaSurplus PDF extracted %d parcels from %s",
            len(listings),
            pdf_url,
        )
        return listings
