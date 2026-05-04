#!/usr/bin/env python3
"""
History API Endpoints for Token Manager

Provides REST endpoints for usage history.
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List, Annotated
from pydantic import BaseModel, field_validator
import re

from api.database import db, log_usage


router = APIRouter(prefix="/api", tags=["history"])

DATE_PATTERN = re.compile(r'^\d{4}-\d{2}-\d{2}$')


class UsageLogRequest(BaseModel):
    provider: str
    metric_type: str
    value: float
    metadata: Optional[dict] = None
    timestamp: Optional[str] = None

    @field_validator('value')
    @classmethod
    def validate_value(cls, v):
        if v < 0:
            raise ValueError('Value must be non-negative')
        return v


@router.post("/history")
async def create_history_entry(entry: UsageLogRequest):
    """
    Log a new usage entry.
    
    Required fields:
    - provider: Service provider (elevenlabs, brave, openclaw)
    - metric_type: Type of metric (characters, tokens, api_calls)
    - value: Numeric value
    """
    try:
        row_id = log_usage(
            provider=entry.provider,
            metric_type=entry.metric_type,
            value=entry.value,
            metadata=entry.metadata,
            timestamp=entry.timestamp
        )
        return {"id": row_id, "status": "logged"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/history")
async def get_history(
    start: Annotated[Optional[str], Query(None, description="Start date (ISO format)")] = None,
    end: Annotated[Optional[str], Query(None, description="End date (ISO format)")] = None,
    provider: Annotated[Optional[str], Query(None, description="Filter by provider")] = None,
    limit: Annotated[int, Query(100, ge=1, le=1000)] = 100
):
    """
    Get usage history with optional date filtering.
    
    Query parameters:
    - start: Start date in ISO format (e.g., 2026-01-01)
    - end: End date in ISO format (e.g., 2026-01-31)
    - provider: Filter by provider name
    - limit: Maximum number of records (default 100)
    """
    try:
        history = db.get_history(start=start, end=end, provider=provider, limit=limit)
        return {"history": history, "count": len(history)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/history/aggregate")
async def get_history_aggregate(
    start: Annotated[Optional[str], Query(None)] = None,
    end: Annotated[Optional[str], Query(None)] = None
):
    """Get aggregated usage statistics."""
    try:
        aggregate = db.get_usage_aggregate(start=start, end=end)
        return {"aggregate": aggregate}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
