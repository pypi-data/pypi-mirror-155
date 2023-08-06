"""
Configuration settings for the api
"""
from pathlib import Path

PORT = 8765
RESOURCES = ["text"]
CLASSIFY_ENDPOINT = "classify"
LOGGER_NAME = "fidescls_api"
LOG_FILENAME = Path(__file__).parent / "logs/api.log"

PII_DEFAULT_THRESHOLD = 0.3
