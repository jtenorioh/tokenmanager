#!/usr/bin/env python3
"""
OpenClaw Model Usage Client

Fetches usage data from OpenClaw sessions and QMD memory.
"""

import json
import os
from pathlib import Path
from datetime import datetime, timedelta

class OpenClawClient:
    def __init__(self):
        self.workspace_path = Path.home() / ".openclaw" / "workspace"
        self.credentials_file = self.workspace_path / ".credentials" / "microsoft-graph-tokens.json"
        
    def get_model_usage(self, days=7):
        """
        Get model usage statistics from OpenClaw session history.
        
        Returns dict with primary and vision model token counts.
        """
        # Read session status to get token usage
        usage = {
            "primary": {"tokens_used": 0, "calls": 0},
            "vision": {"tokens_used": 0, "calls": 0}
        }
        
        try:
            # Try reading QMD statistics if available
            qmd_stats_file = self.workspace_path / ".qmd" / "stats.json"
            if qmd_stats_file.exists():
                with open(qmd_stats_file) as f:
                    stats = json.load(f)
                    usage["primary"]["tokens_used"] = stats.get("total_tokens", 0)
        except Exception as e:
            pass
        
        return usage
    
    def get_session_usage(self, session_key=None):
        """Get specific session usage details."""
        # Read session files from workspace if available
        sessions_dir = self.workspace_path / "sessions"
        
        if not sessions_dir.exists():
            return {"sessions": [], "total_tokens": 0}
        
        sessions = []
        total_tokens = 0
        
        try:
            for session_file in sessions_dir.glob("*.json"):
                with open(session_file) as f:
                    data = json.load(f)
                    sessions.append({
                        "id": session_file.stem,
                        "model": data.get("model", "unknown"),
                        "tokens_used": data.get("tokens_used", 0),
                        "timestamp": data.get("created_at", "")
                    })
                    total_tokens += data.get("tokens_used", 0)
        except Exception as e:
            pass
        
        return {"sessions": sessions, "total_tokens": total_tokens}
    
    def get_openclaw_config(self):
        """Load OpenClaw configuration for API keys."""
        config_file = Path.home() / ".openclaw" / "openclaw.json"
        
        if not config_file.exists():
            return None
        
        with open(config_file) as f:
            return json.load(f)
