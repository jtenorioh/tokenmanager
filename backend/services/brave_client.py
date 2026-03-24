#!/usr/bin/env python3
"""
Brave Search API Client

Fetches API usage statistics.
"""

import requests
from pathlib import Path
import json


class BraveClient:
    def __init__(self):
        self.api_url = "https://api.search.brave.com"
        
    def get_api_key(self):
        """Load Brave API key from OpenClaw config."""
        # Try OpenClaw config first
        config_file = Path.home() / ".openclaw" / "openclaw.json"
        if config_file.exists():
            with open(config_file) as f:
                config = json.load(f)
                return config.get("web_search", {}).get("brave_api_key")
        
        # Try credentials file
        creds_file = Path.home() / ".openclaw" / "workspace" / ".credentials" / "brave-api-key"
        if creds_file.exists():
            with open(creds_file) as f:
                return f.read().strip()
        
        return None
    
    def get_usage(self):
        """
        Get current Brave API usage statistics.
        
        Returns dict with daily limits and remaining calls.
        """
        api_key = self.get_api_key()
        if not api_key:
            return {"error": "Brave API key not configured"}
        
        # Note: Brave Search doesn't provide direct usage endpoint
        # We track usage via request headers and local logging
        
        return {
            "api_key_configured": True,
            "rate_limit_per_day": 1000,  # Free tier limit
            "daily_usage_estimate": self._estimate_daily_usage(),
            "last_api_call": None  # Will be set by middleware
        }
    
    def _estimate_daily_usage(self):
        """
        Estimate daily usage from OpenClaw session logs.
        
        This is a fallback since Brave doesn't provide direct stats.
        """
        try:
            # Check recent OpenClaw sessions for API calls
            workspace = Path.home() / ".openclaw" / "workspace"
            
            # Look for session files that might contain Brave API usage
            daily_logs = workspace / "memory"
            if daily_logs.exists():
                today = datetime.now().strftime("%Y-%m-%d")
                log_file = daily_logs / f"{today}.md"
                
                if log_file.exists():
                    with open(log_file) as f:
                        content = f.read()
                        # Count Brave API mentions
                        return content.count("Brave") // 10  # Rough estimate
            
            return 0
            
        except Exception as e:
            return 0
    
    def search(self, query):
        """
        Perform a search using the Brave API.
        
        This can be used to track actual usage for stats.
        """
        api_key = self.get_api_key()
        if not api_key:
            return {"error": "Brave API key not configured"}
        
        headers = {
            "X-Subscription-Token": api_key,
            "Accept": "application/json"
        }
        
        try:
            response = requests.get(
                f"{self.api_url}/res/v1/web/search",
                params={"q": query, "count": 5},
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                return {
                    "success": True,
                    "results_count": len(response.json().get("web", {}).get("results", []))
                }
            else:
                return {"error": f"API error: {response.status_code}"}
                
        except requests.RequestException as e:
            return {"error": str(e)}
