"""
SQLAlchemy ORM models and storage layer.
Stores every enriched parcel result for historical querying and deduplication.
"""

import json
import logging
from datetime import datetime, timezone

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    Integer,
    String,
    Text,
    create_engine,
    event,
)
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from config import DB

logger = logging.getLogger(__name__)


class Base(DeclarativeBase):
    pass


class ParcelRecord(Base):
    __tablename__ = "parcel_records"

    id = Column(Integer, primary_key=True, autoincrement=True)
    parcel_id = Column(String(20), index=True, nullable=False)
    source = Column(String(50))
    title = Column(String(255))
    url = Column(Text)
    address = Column(String(255))
    lot_sqft = Column(Integer)
    zoning_code = Column(String(20))
    flood_zone = Column(String(10))
    just_value = Column(Float)

    # AI analysis outputs
    composite_score = Column(Integer)
    investment_tier = Column(String(60))
    alert_headline = Column(String(255))
    alert_body = Column(Text)
    priority_rating = Column(String(20))
    quadplex_eligible = Column(Boolean)

    # Full JSON blobs for the sub-analyses
    zoning_analysis_json = Column(Text)
    environmental_analysis_json = Column(Text)
    compliance_analysis_json = Column(Text)
    summary_json = Column(Text)

    # Tracking
    alert_sent = Column(Boolean, default=False)
    first_seen = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    last_updated = Column(DateTime, default=lambda: datetime.now(timezone.utc))


engine = create_engine(DB.url, echo=False, future=True)

if "sqlite" in DB.url:
    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(dbapi_conn, _):
        dbapi_conn.execute("PRAGMA journal_mode=WAL")
        dbapi_conn.execute("PRAGMA foreign_keys=ON")

Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def upsert_parcel(enriched: dict) -> ParcelRecord:
    """Insert or update a parcel record. Returns the persisted record."""
    with SessionLocal() as session:
        record = (
            session.query(ParcelRecord)
            .filter_by(parcel_id=enriched["parcel_id"])
            .first()
        )
        if record is None:
            record = ParcelRecord(parcel_id=enriched["parcel_id"])
            session.add(record)

        record.source = enriched.get("source")
        record.title = enriched.get("title")
        record.url = enriched.get("url")
        record.address = enriched.get("address")
        record.lot_sqft = enriched.get("lot_sqft")
        record.zoning_code = enriched.get("zoning_code")
        record.flood_zone = enriched.get("flood_zone")
        record.just_value = _safe_float(enriched.get("just_value"))

        record.composite_score = enriched.get("composite_score")
        record.investment_tier = enriched.get("investment_tier")
        record.alert_headline = enriched.get("alert_headline")
        record.alert_body = enriched.get("alert_body")

        za = enriched.get("zoning_analysis", {})
        record.priority_rating = za.get("priority_rating")
        record.quadplex_eligible = za.get("quadplex_eligible")
        record.zoning_analysis_json = json.dumps(za)
        record.environmental_analysis_json = json.dumps(
            enriched.get("environmental_analysis", {})
        )
        record.compliance_analysis_json = json.dumps(
            enriched.get("compliance_analysis", {})
        )
        record.summary_json = json.dumps(enriched.get("summary", {}))

        record.last_updated = datetime.now(timezone.utc)
        session.commit()
        session.refresh(record)
        return record


def get_top_parcels(min_score: int = 0, limit: int = 50) -> list[ParcelRecord]:
    with SessionLocal() as session:
        return (
            session.query(ParcelRecord)
            .filter(ParcelRecord.composite_score >= min_score)
            .order_by(ParcelRecord.composite_score.desc())
            .limit(limit)
            .all()
        )


def mark_alert_sent(parcel_id: str) -> None:
    with SessionLocal() as session:
        record = session.query(ParcelRecord).filter_by(parcel_id=parcel_id).first()
        if record:
            record.alert_sent = True
            session.commit()


def _safe_float(val) -> float | None:
    try:
        return float(str(val).replace(",", "").replace("$", ""))
    except (TypeError, ValueError):
        return None
