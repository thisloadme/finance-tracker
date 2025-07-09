from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
import time
from collections import defaultdict
import asyncio
from typing import Dict, Tuple
import logging

logger = logging.getLogger(__name__)

class RateLimiter:
    def __init__(self, requests_per_minute: int = 60):
        self.requests_per_minute = requests_per_minute
        self.requests: Dict[str, list] = defaultdict(list)
        self.lock = asyncio.Lock()
    
    async def is_allowed(self, client_id: str) -> bool:
        async with self.lock:
            now = time.time()
            # Remove requests older than 1 minute
            self.requests[client_id] = [
                req_time for req_time in self.requests[client_id]
                if now - req_time < 60
            ]
            
            # Check if limit exceeded
            if len(self.requests[client_id]) >= self.requests_per_minute:
                return False
            
            # Add current request
            self.requests[client_id].append(now)
            return True

# Global rate limiter instance
rate_limiter = RateLimiter()

def get_client_id(request: Request) -> str:
    """Get client identifier for rate limiting"""
    # Use IP address as client ID
    client_ip = request.client.host
    # For production, you might want to use API key or user ID
    return client_ip

async def rate_limit_middleware(request: Request, call_next):
    """Rate limiting middleware"""
    client_id = get_client_id(request)
    
    if not await rate_limiter.is_allowed(client_id):
        logger.warning(f"Rate limit exceeded for client: {client_id}")
        return JSONResponse(
            status_code=429,
            content={
                "detail": "Rate limit exceeded. Please try again later.",
                "retry_after": 60
            }
        )
    
    response = await call_next(request)
    return response 