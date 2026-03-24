#!/usr/bin/env python3
"""
SQLite Database for Token Manager

Handles data persistence for usage history.
"""

import sqlite3
import json
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any


class Database:
    def __init__(self, db_path: Optional[str] = None):
        if db_path is None:
            data_dir = Path(__file__).parent.parent / "data"
            data_dir.mkdir(exist_ok=True)
            db_path = data_dir / "usage_history.db"
        
        self.db_path = str(db_path)
        self._init_db()
    
    def _init_db(self):
        """Initialize database schema."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usage_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                provider TEXT NOT NULL,
                metric_type TEXT NOT NULL,
                value REAL NOT NULL,
                metadata TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_usage_timestamp 
            ON usage_history(timestamp)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_usage_provider 
            ON usage_history(provider)
        """)
        
        conn.commit()
        conn.close()
    
    def log_usage(
        self,
        provider: str,
        metric_type: str,
        value: float,
        metadata: Optional[Dict[str, Any]] = None,
        timestamp: Optional[str] = None
    ) -> int:
        """Log a usage entry."""
        if timestamp is None:
            timestamp = datetime.now().isoformat()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            """
            INSERT INTO usage_history (timestamp, provider, metric_type, value, metadata)
            VALUES (?, ?, ?, ?, ?)
            """,
            (timestamp, provider, metric_type, value, json.dumps(metadata) if metadata else None)
        )
        
        row_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return row_id
    
    def get_history(
        self,
        start: Optional[str] = None,
        end: Optional[str] = None,
        provider: Optional[str] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """Get usage history with optional filtering."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        query = "SELECT * FROM usage_history WHERE 1=1"
        params = []
        
        if start:
            query += " AND timestamp >= ?"
            params.append(start)
        
        if end:
            query += " AND timestamp <= ?"
            params.append(end)
        
        if provider:
            query += " AND provider = ?"
            params.append(provider)
        
        query += " ORDER BY timestamp DESC LIMIT ?"
        params.append(limit)
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        
        return [
            {
                "id": row["id"],
                "timestamp": row["timestamp"],
                "provider": row["provider"],
                "metric_type": row["metric_type"],
                "value": row["value"],
                "metadata": json.loads(row["metadata"]) if row["metadata"] else None
            }
            for row in rows
        ]
    
    def get_usage_aggregate(
        self,
        start: Optional[str] = None,
        end: Optional[str] = None,
        group_by: str = "provider"
    ) -> List[Dict[str, Any]]:
        """Get aggregated usage statistics."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        query = "SELECT provider, metric_type, SUM(value) as total FROM usage_history WHERE 1=1"
        params = []
        
        if start:
            query += " AND timestamp >= ?"
            params.append(start)
        
        if end:
            query += " AND timestamp <= ?"
            params.append(end)
        
        query += f" GROUP BY {group_by}, metric_type"
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        
        return [
            {
                "provider": row["provider"],
                "metric_type": row["metric_type"],
                "total": row["total"]
            }
            for row in rows
        ]


db = Database()


def log_usage(
    provider: str,
    metric_type: str,
    value: float,
    metadata: Optional[Dict[str, Any]] = None,
    timestamp: Optional[str] = None
) -> int:
    """Convenience function to log usage."""
    return db.log_usage(provider, metric_type, value, metadata, timestamp)


def get_history(
    start: Optional[str] = None,
    end: Optional[str] = None,
    provider: Optional[str] = None,
    limit: int = 100
) -> List[Dict[str, Any]]:
    """Convenience function to get history."""
    return db.get_history(start, end, provider, limit)
