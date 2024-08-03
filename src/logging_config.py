import logging
import os
from uvicorn.config import LOGGING_CONFIG as uvicorn_log_config

# Ensure the logs directory exists
logs_root_path = os.path.join(os.path.dirname(__file__), "../logs")
os.makedirs(logs_root_path, exist_ok=True)

# Default log formatter
log_formatter = logging.Formatter(
    "[%(levelname)s] %(asctime)s \"%(message)s\"",
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Stream handler
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(log_formatter)

# File handler for application logs
file_handler = logging.FileHandler(os.path.join(logs_root_path, "app.log"))
file_handler.setFormatter(log_formatter)

# Configure Uvicorn logging
uvicorn_log_config['formatters']['default']['fmt'] = log_formatter._fmt
uvicorn_log_config['formatters']['default']['datefmt'] = log_formatter.datefmt

# File handler for Uvicorn logs
uvicorn_file_handler = logging.FileHandler(os.path.join(logs_root_path, "uvicorn.log"))
uvicorn_file_handler.setFormatter(log_formatter)
logging.getLogger("uvicorn").addHandler(uvicorn_file_handler)

# Configure the root logger
logging.basicConfig(
    level=logging.INFO,
    handlers=[file_handler, stream_handler]
)

logger = logging.getLogger(__name__)
logger.info("Logging is set up.")
