#!/usr/bin/env python3
"""
ElevenLabs API Client

Fetches token usage data from ElevenLabs API.
"""

import requests
from pathlib import Path
import json


class ElevenLabsClient:
    def __init__(self):
        self.api_url = "https://api.elevenlabs.io/v1"
        
    def get_api_key(self):
        """Load ElevenLabs API key from credentials or OpenClaw config."""
        # Try workspace credentials first
        creds_file = Path.home() / ".openclaw" / "workspace" / ".credentials" / "elevenlabs.json"
        if creds_file.exists():
            with open(creds_file) as f:
                return json.load(f).get("api_key")
        
        # Try OpenClaw config
        config_file = Path.home() / ".openclaw" / "openclaw.json"
        if config_file.exists():
            with open(config_file) as f:
                config = json.load(f)
                return config.get("elevenlabs", {}).get("api_key")
        
        return None
    
    def get_usage(self):
        """
        Get current ElevenLabs usage statistics.
        
        Returns dict with character counts, requests, etc.
        """
        api_key = self.get_api_key()
        if not api_key:
            return {"error": "ElevenLabs API key not configured"}
        
        headers = {
            "xi-api-key": api_key,
            "Content-Type": "application/json"
        }
        
        try:
            # Get character usage (approximate token count for TTS)
            response = requests.get(
                f"{self.api_url}/user/subscription",
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "characters_used": data.get("character_count", 0),
                    "characters_limit": data.get("character_limit", 0),
                    "tier": data.get("tier", "unknown"),
                    "next_character_reset_unix": data.get("next_character_reset_unix", 0)
                }
            else:
                return {"error": f"API error: {response.status_code}"}
                
        except requests.RequestException as e:
            return {"error": str(e)}
    
    def get_voices(self):
        """Get list of available voices."""
        api_key = self.get_api_key()
        if not api_key:
            return {"error": "ElevenLabs API key not configured"}
        
        headers = {
            "xi-api-key": api_key,
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.get(
                f"{self.api_url}/voices",
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json().get("voices", [])
            else:
                return {"error": f"API error: {response.status_code}"}
                
        except requests.RequestException as e:
            return {"error": str(e)}
