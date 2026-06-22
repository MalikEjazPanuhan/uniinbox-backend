import redis
import json
from src.core.config import settings

redis_client = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)

class RedisClient:
    @staticmethod
    def set_key(key: str, value: str, expire: int = 3600):
        redis_client.setex(key, expire, value)
    
    @staticmethod
    def get_key(key: str) -> str:
        return redis_client.get(key)
    
    @staticmethod
    def delete_key(key: str):
        redis_client.delete(key)
    
    @staticmethod
    def set_json(key: str, data: dict, expire: int = 3600):
        redis_client.setex(key, expire, json.dumps(data))
    
    @staticmethod
    def get_json(key: str) -> dict:
        data = redis_client.get(key)
        return json.loads(data) if data else None
    
    @staticmethod
    def exists(key: str) -> bool:
        return redis_client.exists(key) > 0
    
    