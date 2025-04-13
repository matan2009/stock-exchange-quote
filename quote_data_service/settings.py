import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
ALPHAVANTAGE_URL = os.getenv("ALPHAVANTAGE_URL", "")
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
SECRET_KEY = os.getenv("SECRET_KEY", "")
PORT = 8001
GLOBAL_QUOTE = "GLOBAL_QUOTE"
RATIO_THRESHOLD = 1.03
ONE_HOUR = 3600
TEN_MINUTES = 600
TWENTY_MINUTES = 1200
COST_KEY = "COST"
QUERY_COST = 0.1
ALGORITHM = "HS256"
