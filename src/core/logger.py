"""
MarketHelm - Logging Configuration

Sets up logging with both console and file output, with different log levels.
"""

import logging
import os
from pathlib import Path
from datetime import datetime


def _rename_legacy_log_files(log_path: Path) -> None:
    """Rename stock_tracker_*.log files left from older releases to market_helm_*.log."""
    for old in sorted(log_path.glob("stock_tracker_*.log")):
        if old.name.startswith("stock_tracker_errors_"):
            continue
        suffix = old.name.removeprefix("stock_tracker_")
        new = log_path / f"market_helm_{suffix}"
        if not new.exists():
            try:
                old.rename(new)
            except OSError:
                pass
    for old in sorted(log_path.glob("stock_tracker_errors_*.log")):
        suffix = old.name.removeprefix("stock_tracker_errors_")
        new = log_path / f"market_helm_errors_{suffix}"
        if not new.exists():
            try:
                old.rename(new)
            except OSError:
                pass


def setup_logger(name: str = "market_helm", log_dir: str = "logs") -> logging.Logger:
    """
    Set up logger with console and file handlers.
    
    Args:
        name: Logger name
        log_dir: Directory to store log files
    
    Returns:
        Configured logger instance
    """
    # Create logs directory if it doesn't exist
    log_path = Path(log_dir)
    log_path.mkdir(exist_ok=True)
    _rename_legacy_log_files(log_path)

    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # Capture all levels
    
    # Remove existing handlers to avoid duplicates
    logger.handlers.clear()
    
    # Create formatters
    detailed_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_formatter = logging.Formatter(
        '%(levelname)s - %(message)s'
    )
    
    # Console handler - INFO level and above
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    # File handler - DEBUG level and above (all logs)
    today = datetime.now().strftime('%Y-%m-%d')
    log_file = log_path / f"market_helm_{today}.log"
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(detailed_formatter)
    logger.addHandler(file_handler)
    
    # Error file handler - ERROR level and above
    error_log_file = log_path / f"market_helm_errors_{today}.log"
    error_handler = logging.FileHandler(error_log_file, encoding='utf-8')
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(detailed_formatter)
    logger.addHandler(error_handler)
    
    return logger

