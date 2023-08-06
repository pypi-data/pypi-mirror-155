"""
Configuration settings for the cli
"""
from pathlib import Path

RESOURCES = ["text"]
LOGGER_NAME = "fidescls_cli"
LOG_FILENAME = Path(__file__).parent / "logs/cli.log"
