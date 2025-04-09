import os

from dotenv import load_dotenv

load_dotenv()

PORT = 8000
QUOTE_DATA_SERVICE_URL = os.getenv("QUOTE_DATA_SERVICE_URL", "")
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
LIMIT = 10   # max requests in TIME_FRAME
TIME_FRAME = 60  # seconds

