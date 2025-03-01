import os
import dotenv
import redis.asyncio as redis

dotenv.load_dotenv()

REDIS_CONFIG = {
    'REDIS_HOST': os.getenv('REDIS_HOST', 'db_redis'),
    'REDIS_PORT': int(os.getenv('REDIS_PORT', 6379)),
    'REDIS_PASSWORD': os.getenv('REDIS_PASSWORD', 'redis_password'),
}

redis_client = redis.Redis(
    host=REDIS_CONFIG['REDIS_HOST'],
    port=REDIS_CONFIG['REDIS_PORT'],
    password=REDIS_CONFIG['REDIS_PASSWORD'],
    decode_responses=True,
)
