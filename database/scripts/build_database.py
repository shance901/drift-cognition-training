#!/usr/bin/env python3
"""Builds grants.db (SQLite) from schema.sql and data/seed_data.json."""
import json
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = ROOT / "schema.sql"
SEED_PATH = ROOT / "data" / "seed_data.json"
DB_PATH = ROOT / "grants.db"

GRANT_COLUMNS = [
    "name", "provider", "provider_type", "primary_category", "description",
    "eligibility", "funding_amount_text", "funding_amount_min", "funding_amount_max",
    "geographic_scope", "application_status", "how_to_apply", "application_url",
    "source_url", "last_verified", "notes",
]


def build():
    DB_PATH.unlink(missing_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.executescript(SCHEMA_PATH.read_text())

    records = json.loads(SEED_PATH.read_text())
    placeholders = ", ".join("?" for _ in GRANT_COLUMNS)
    insert_sql = f"INSERT INTO grants ({', '.join(GRANT_COLUMNS)}) VALUES ({placeholders})"

    for record in records:
        values = [record.get(col) for col in GRANT_COLUMNS]
        cursor = conn.execute(insert_sql, values)
        grant_id = cursor.lastrowid
        for tag in record.get("tags", []):
            conn.execute(
                "INSERT OR IGNORE INTO grant_tags (grant_id, tag) VALUES (?, ?)",
                (grant_id, tag),
            )

    conn.commit()
    count = conn.execute("SELECT COUNT(*) FROM grants").fetchone()[0]
    print(f"Built {DB_PATH} with {count} grant records.")
    conn.close()


if __name__ == "__main__":
    build()
