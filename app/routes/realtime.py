"""
/api/realtime-data
==================
Appends live records to a persistent CSV stream. The normal analysis and
forecasting routes can then consume that stream by passing its dataset name.
"""

import re

import pandas as pd
from fastapi import APIRouter, HTTPException

from app.utils import REALTIME_DIR

router = APIRouter()


def _safe_dataset_name(name: str) -> str:
    safe_name = re.sub(r"[^A-Za-z0-9_.-]+", "_", name.strip())
    if not safe_name:
        raise HTTPException(status_code=422, detail="dataset_name is required")
    return safe_name if safe_name.lower().endswith(".csv") else f"{safe_name}.csv"


@router.post("/realtime-data")
def append_realtime_data(payload: dict):
    dataset_name = _safe_dataset_name(str(payload.get("dataset_name", "")))
    record = payload.get("data")
    if not isinstance(record, dict) or not record:
        raise HTTPException(status_code=422, detail="data must be a non-empty object")

    path = REALTIME_DIR / dataset_name
    incoming = pd.DataFrame([record])
    if path.exists():
        current = pd.read_csv(path)
        incoming = pd.concat([current, incoming], ignore_index=True, sort=False)
    incoming.to_csv(path, index=False)

    return {
        "status": "accepted",
        "dataset": dataset_name,
        "rows": int(len(incoming)),
        "columns": list(incoming.columns),
        "source": "realtime",
    }