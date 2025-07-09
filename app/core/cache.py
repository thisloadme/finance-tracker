import redis
import json
import pickle
from typing import Any, Optional
from app.config import settings
import logging

logger = logging.getLogger(__name__)

class Cache:
    def __init__(self):
        try:
            self.redis_client = redis.from_url(settings.REDIS_URL)
            self.redis_client.ping()  # Test connection
        except Exception as e:
            logger.warning(f"Redis connection failed: {e}")
            self.redis_client = None
    
    def _get_key(self, prefix: str, identifier: str) -> str:
        return f"{prefix}:{identifier}"
    
    def set(self, key: str, value: Any, expire: int = 300) -> bool:
        """Set cache value with expiration (default 5 minutes)"""
        if not self.redis_client:
            return False
        
        try:
            serialized_value = pickle.dumps(value)
            return self.redis_client.setex(key, expire, serialized_value)
        except Exception as e:
            logger.error(f"Cache set error: {e}")
            return False
    
    def get(self, key: str) -> Optional[Any]:
        """Get cache value"""
        if not self.redis_client:
            return None
        
        try:
            value = self.redis_client.get(key)
            if value:
                return pickle.loads(value)
            return None
        except Exception as e:
            logger.error(f"Cache get error: {e}")
            return None
    
    def delete(self, key: str) -> bool:
        """Delete cache value"""
        if not self.redis_client:
            return False
        
        try:
            return bool(self.redis_client.delete(key))
        except Exception as e:
            logger.error(f"Cache delete error: {e}")
            return False
    
    def invalidate_pattern(self, pattern: str) -> bool:
        """Invalidate all keys matching pattern"""
        if not self.redis_client:
            return False
        
        try:
            keys = self.redis_client.keys(pattern)
            if keys:
                return bool(self.redis_client.delete(*keys))
            return True
        except Exception as e:
            logger.error(f"Cache invalidate pattern error: {e}")
            return False

# Global cache instance
cache = Cache()

def cache_user_data(user_id: int, data: Any, expire: int = 300):
    """Cache user-specific data"""
    key = cache._get_key("user", str(user_id))
    return cache.set(key, data, expire)

def get_cached_user_data(user_id: int) -> Optional[Any]:
    """Get cached user-specific data"""
    key = cache._get_key("user", str(user_id))
    return cache.get(key)

def invalidate_user_cache(user_id: int):
    """Invalidate all cache for specific user"""
    pattern = f"user:{user_id}:*"
    return cache.invalidate_pattern(pattern) 