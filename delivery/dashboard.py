"""
Rich terminal dashboard for reviewing enriched parcel results.
Run directly: python -m delivery.dashboard
"""

import json
import sys
from datetime import datetime, timezone

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box
from rich.text import Text

from .database import get_top_parcels, ParcelRecord

console = Console()


def _tier_style(tier: str) -> str:
    if "Tier 1" in tier:
        return "bold green"
    if "Tier 2" in tier:
        return "bold yellow"
    if "Tier 3" in tier:
        return "cyan"
    return "dim"


def _score_color(score: int) -> str:
    if score >= 80:
        return "green"
    if score >= 60:
        return "yellow"
    if score >= 40:
        return "orange3"
    return "red"


def render_summary_table(parcels: list[ParcelRecord]) -> None:
    table = Table(
        title="Escambia County — Surplus Land Intelligence Dashboard",
        box=box.ROUNDED,
        show_lines=True,
        header_style="bold white on dark_blue",
        title_style="bold white",
    )
    table.add_column("Score", justify="center", width=7)
    table.add_column("Parcel ID", style="bold")
    table.add_column("Address", max_width=30)
    table.add_column("Sqft", justify="right", width=8)
    table.add_column("Zone", justify="center", width=6)
    table.add_column("Flood", justify="center", width=7)
    table.add_column("Tier", min_width=22)
    table.add_column("Source", width=18)
    table.add_column("Seen", width=12)

    for p in parcels:
        score = p.composite_score or 0
        score_text = Text(str(score), style=_score_color(score))
        tier_text = Text(p.investment_tier or "—", style=_tier_style(p.investment_tier or ""))
        seen = p.first_seen.strftime("%Y-%m-%d") if p.first_seen else "—"
        sqft = f"{p.lot_sqft:,}" if p.lot_sqft else "—"
        table.add_row(
            score_text,
            p.parcel_id,
            p.address or "—",
            sqft,
            p.zoning_code or "—",
            p.flood_zone or "—",
            tier_text,
            p.source or "—",
            seen,
        )

    console.print(table)


def render_parcel_detail(record: ParcelRecord) -> None:
    """Print a detailed panel for a single parcel."""
    headline = record.alert_headline or "No headline"
    body = record.alert_body or ""

    summary_data = json.loads(record.summary_json or "{}")
    zoning_data = json.loads(record.zoning_analysis_json or "{}")
    env_data = json.loads(record.environmental_analysis_json or "{}")
    comp_data = json.loads(record.compliance_analysis_json or "{}")

    console.print(
        Panel(
            f"[bold]{headline}[/bold]\n\n{body}",
            title=f"[white]{record.parcel_id}[/white]",
            subtitle=f"Score: {record.composite_score}/100  |  {record.investment_tier}",
            border_style="green" if (record.composite_score or 0) >= 70 else "yellow",
        )
    )

    # Zoning
    by_right = ", ".join(zoning_data.get("by_right_uses", []))
    quadplex = "Yes" if zoning_data.get("quadplex_eligible") else "No"
    console.print(f"  [bold]Zoning:[/bold] {record.zoning_code}  |  By-Right: {by_right}")
    console.print(f"  [bold]Quadplex Eligible:[/bold] {quadplex}  |  "
                  f"Max Units: {zoning_data.get('max_density_units', '—')}")

    # Environmental
    flood_risk = env_data.get("flood_risk", "—")
    env_score = env_data.get("environmental_score", "—")
    console.print(f"  [bold]Flood Risk:[/bold] {flood_risk}  |  "
                  f"Env Score: {env_score}/100  |  "
                  f"Pervious Space: {env_data.get('estimated_pervious_space_pct', '—')}%")

    # Compliance
    acq_rec = comp_data.get("acquisition_recommendation", "—")
    comp_score = comp_data.get("compliance_score", "—")
    console.print(f"  [bold]Compliance:[/bold] {acq_rec}  |  Score: {comp_score}/100")

    flags = comp_data.get("title_concerns", []) + comp_data.get("easement_flags", [])
    if flags:
        for flag in flags:
            console.print(f"    [yellow]⚠ {flag}[/yellow]")

    console.print(f"  [bold]Next Step:[/bold] {summary_data.get('recommended_next_step', '—')}")
    console.print(f"  [dim]{record.url}[/dim]\n")


def run_dashboard(min_score: int = 0, limit: int = 100, detail_id: str = None) -> None:
    console.print(
        f"\n[bold blue]Municipal Surplus Land Platform[/bold blue]  "
        f"[dim]{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}[/dim]\n"
    )

    parcels = get_top_parcels(min_score=min_score, limit=limit)
    if not parcels:
        console.print("[yellow]No parcels in the database yet. Run the pipeline first.[/yellow]")
        return

    if detail_id:
        match = next((p for p in parcels if p.parcel_id == detail_id), None)
        if match:
            render_parcel_detail(match)
        else:
            console.print(f"[red]Parcel {detail_id} not found.[/red]")
    else:
        render_summary_table(parcels)
        console.print(
            f"\n[dim]Showing {len(parcels)} parcel(s) with score ≥ {min_score}. "
            "Run with --detail <parcel_id> for full analysis.[/dim]\n"
        )


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Surplus Land Dashboard")
    parser.add_argument("--min-score", type=int, default=0)
    parser.add_argument("--limit", type=int, default=100)
    parser.add_argument("--detail", type=str, default=None)
    args = parser.parse_args()
    run_dashboard(min_score=args.min_score, limit=args.limit, detail_id=args.detail)
