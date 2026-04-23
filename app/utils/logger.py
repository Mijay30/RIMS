import logging
import time
from datetime import datetime
from functools import wraps
from typing import Dict

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("config/rims_audit.log"), logging.StreamHandler()]
)

logger = logging.getLogger("RIMS_Core")

def create_fingerprint(user_id: str) -> Dict:
    return {
        "userId": user_id,
        "timestamp": datetime.now().isoformat(),
        "action": "modification"
    }

def monitor_performance(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        try:
            result = func(*args, **kwargs)
            duration = time.perf_counter() - start_time
            if duration > 2.0:
                logger.warning(f"Slow Query: {func.__name__} took {duration:.2f}s")
            return result
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {str(e)}")
            raise e
    return wrapper