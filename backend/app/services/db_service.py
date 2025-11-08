# backend/app/services/db_service.py
import os
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Text, DateTime, Float, JSON
from sqlalchemy.sql import select
from datetime import datetime
from app.config import Settings

settings = Settings()

DATABASE_URL = os.getenv("DATABASE_URL", settings.DATABASE_URL)

connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, future=True, echo=False, connect_args=connect_args)
metadata = MetaData()

# complaints table
complaints = Table(
    "complaints", metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("reference_id", String(128), unique=True, nullable=False),
    Column("portal_case_id", String(128), nullable=True),
    Column("name", String(256)),
    Column("phone", String(64), nullable=False),
    Column("language", String(16)),
    Column("incident_type", String(128)),
    Column("description", Text),
    Column("date_of_incident", DateTime),
    Column("amount", Float),
    Column("platform", String(128)),
    Column("txn_id", String(128)),
    Column("attachments", JSON),
    Column("status", String(64), default="registered"),
    Column("created_at", DateTime, default=datetime.utcnow),
    Column("updated_at", DateTime, default=datetime.utcnow),
)

def init_db():
    """Create tables if not exist."""
    metadata.create_all(engine)

def create_complaint(payload: dict) -> dict:
    """Insert complaint and return record as dict."""
    import uuid
    if "reference_id" not in payload or not payload.get("reference_id"):
        payload["reference_id"] = str(uuid.uuid4())

    now = datetime.utcnow()
    payload["created_at"] = now
    payload["updated_at"] = now

    with engine.begin() as conn:
        res = conn.execute(complaints.insert().values(**payload))
        # get inserted row
        pk = res.inserted_primary_key[0]
        row = conn.execute(select(complaints).where(complaints.c.id == pk)).first()
        if row:
            return dict(row._mapping)
    return {}

def get_complaint_by_reference(ref: str) -> dict:
    with engine.connect() as conn:
        row = conn.execute(select(complaints).where(complaints.c.reference_id == ref)).first()
        if row:
            return dict(row._mapping)
    return {}

def get_all_complaints(limit: int = 100) -> list:
    with engine.connect() as conn:
        rows = conn.execute(select(complaints).order_by(complaints.c.created_at.desc()).limit(limit)).fetchall()
        return [dict(r._mapping) for r in rows]

def link_portal_case(reference_id: str, portal_case_id: str) -> bool:
    with engine.begin() as conn:
        res = conn.execute(
            complaints.update().where(complaints.c.reference_id == reference_id).values(portal_case_id=portal_case_id, updated_at=datetime.utcnow())
        )
        return res.rowcount > 0
