import os, logging

logger = logging.getLogger("uvicorn")
# .getLogger must be "uvicorn", not "__name__"
logger.setLevel(os.getenv("FASTAPI_LOG_LEVEL", logging.INFO))