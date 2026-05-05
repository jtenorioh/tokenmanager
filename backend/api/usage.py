#!/usr/bin/env python3
"""
API Endpoints for Token Manager

Provides REST endpoints for token usage tracking.
"""

from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/api", tags=["usage"])


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


@router.get("/usage/tokens")
async def get_total_tokens():
    """
    Get total tokens used across all services.
    
    Returns combined count from ElevenLabs, Brave, and OpenClaw models.
    """
    # Import clients here to avoid import issues
    try:
        from services.elevenlabs_client import ElevenLabsClient
        from services.brave_client import BraveClient
        from services.openclaw_client import OpenClawClient
        
        elevenlabs = ElevenLabsClient()
        brave = BraveClient()
        openclaw = OpenClawClient()
        
        total_tokens = {
            "elevenlabs": {"characters_used": 0},
            "brave": {"api_calls": 0},
            "openclaw_primary": {"tokens_used": 0},
            "openclaw_vision": {"tokens_used": 0}
        }
        
        # Get ElevenLabs usage
        el_usage = elevenlabs.get_usage()
        if "error" not in el_usage:
            total_tokens["elevenlabs"]["characters_used"] = el_usage.get("characters_used", 0)
        
        # Get Brave usage
        brave_usage = brave.get_usage()
        if "error" not in brave_usage:
            total_tokens["brave"]["api_calls"] = brave_usage.get("daily_usage_estimate", 0)
        
        # Get OpenClaw usage
        oc_usage = openclaw.get_model_usage()
        total_tokens["openclaw_primary"]["tokens_used"] = oc_usage.get("primary", {}).get("tokens_used", 0)
        total_tokens["openclaw_vision"]["tokens_used"] = oc_usage.get("vision", {}).get("tokens_used", 0)
        
        # Calculate totals
        total_characters = total_tokens["elevenlabs"]["characters_used"]
        total_brave_calls = total_tokens["brave"]["api_calls"]
        total_primary_tokens = total_tokens["openclaw_primary"]["tokens_used"]
        total_vision_tokens = total_tokens["openclaw_vision"]["tokens_used"]
        
        return {
            "total_characters": total_characters,
            "total_brave_api_calls": total_brave_calls,
            "total_primary_model_tokens": total_primary_tokens,
            "total_vision_model_tokens": total_vision_tokens,
            "total_combined_estimate": total_characters + total_brave_calls * 100 + total_primary_tokens + total_vision_tokens,
            "by_provider": total_tokens
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e), description="Internal server error while fetching token usage")


@router.get("/usage/by-provider")
async def get_usage_by_provider():
    """Get usage breakdown by service provider."""
    try:
        from services.elevenlabs_client import ElevenLabsClient
        from services.brave_client import BraveClient
        
        elevenlabs = ElevenLabsClient()
        brave = BraveClient()
        
        return {
            "elevenlabs": elevenlabs.get_usage(),
            "brave": brave.get_usage()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e), description="Internal server error while fetching provider usage")


@router.get("/models/primary")
async def get_primary_model_usage():
    """Get primary model (Qwen3.5) usage statistics."""
    try:
        from services.openclaw_client import OpenClawClient
        
        openclaw = OpenClawClient()
        
        return {
            "model": "qwen3-coder-next",
            "usage": openclaw.get_model_usage().get("primary", {}),
            "session_history": openclaw.get_session_usage()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e), description="Internal server error while fetching primary model usage")


@router.get("/models/vision")
async def get_vision_model_usage():
    """Get vision model usage statistics."""
    try:
        from services.openclaw_client import OpenClawClient
        
        openclaw = OpenClawClient()
        
        return {
            "model": "qwen2.5-vl-7b-instruct",
            "usage": openclaw.get_model_usage().get("vision", {}),
            "session_history": openclaw.get_session_usage()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e), description="Internal server error while fetching vision model usage")


@router.get("/api-consumption")
async def get_api_consumption():
    """Get overall API consumption statistics."""
    try:
        from services.elevenlabs_client import ElevenLabsClient
        from services.brave_client import BraveClient
        
        elevenlabs = ElevenLabsClient()
        brave = BraveClient()
        
        return {
            "elevenlabs": {
                "status": "active" if "error" not in elevenlabs.get_usage() else "inactive",
                "last_update": None
            },
            "brave": {
                "status": "active" if "error" not in brave.get_usage() else "inactive",
                "daily_limit": 1000,
                "estimate_used": brave.get_usage().get("daily_usage_estimate", 0)
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e), description="Internal server error while fetching API consumption stats")
