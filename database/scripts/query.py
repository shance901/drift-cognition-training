#!/usr/bin/env python3
"""Query the small-business grants database.

Examples:
  python3 query.py --list
  python3 query.py --category cybersecurity
  python3 query.py --keyword "penetration test"
  python3 query.py --provider-type federal
  python3 query.py --tag women-owned
  python3 query.py --export csv > grants.csv
"""
import argparse
import csv
import sqlite3
import sys
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "grants.db"


def connect():
    if not DB_PATH.exists():
        sys.exit(f"Database not found at {DB_PATH}. Run build_database.py first.")
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def run_query(conn, category=None, keyword=None, provider_type=None, tag=None):
    sql = "SELECT DISTINCT g.* FROM grants g LEFT JOIN grant_tags t ON t.grant_id = g.id WHERE 1=1"
    params = []

    if category:
        sql += " AND g.primary_category = ?"
        params.append(category)
    if provider_type:
        sql += " AND g.provider_type = ?"
        params.append(provider_type)
    if tag:
        sql += " AND t.tag = ?"
        params.append(tag)
    if keyword:
        sql += " AND (g.name LIKE ? OR g.description LIKE ? OR g.notes LIKE ?)"
        like = f"%{keyword}%"
        params.extend([like, like, like])

    sql += " ORDER BY g.primary_category, g.name"
    return conn.execute(sql, params).fetchall()


def print_table(rows):
    if not rows:
        print("No matching grants found.")
        return
    for r in rows:
        print(f"[{r['id']}] {r['name']}  ({r['primary_category']} / {r['provider_type']})")
        print(f"    Provider: {r['provider']}")
        print(f"    Amount:   {r['funding_amount_text']}")
        print(f"    Scope:    {r['geographic_scope']}   Status: {r['application_status']}")
        print(f"    Apply:    {r['application_url']}")
        print(f"    Verified: {r['last_verified']}")
        print()
    print(f"{len(rows)} result(s).")


def export_csv(rows):
    if not rows:
        return
    writer = csv.writer(sys.stdout)
    writer.writerow(rows[0].keys())
    for r in rows:
        writer.writerow([r[k] for k in r.keys()])


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--list", action="store_true", help="List all grants")
    parser.add_argument("--category", choices=["cybersecurity", "cybersecurity_protection", "small_business_general"])
    parser.add_argument("--keyword", help="Search name/description/notes")
    parser.add_argument("--provider-type", choices=["federal", "state", "private", "nonprofit", "portal"])
    parser.add_argument("--tag", help="Filter by exact tag, e.g. women-owned, SBIR, rolling")
    parser.add_argument("--export", choices=["csv"], help="Export results as CSV to stdout")
    args = parser.parse_args()

    conn = connect()
    rows = run_query(
        conn,
        category=args.category,
        keyword=args.keyword,
        provider_type=args.provider_type,
        tag=args.tag,
    )

    if args.export == "csv":
        export_csv(rows)
    else:
        print_table(rows)


if __name__ == "__main__":
    main()
