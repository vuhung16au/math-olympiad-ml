"""
Logging Configuration for MathHeart Player
Handles console and file logging with rotation
"""

import logging
import logging.handlers
import os
import platform
from pathlib import Path
from datetime import datetime
from typing import Optional


def get_log_directory() -> Path:
    """
    Get the log directory based on the operating system.
    
    Returns:
        Path to the log directory
    """
    system = platform.system()
    
    if system == "Windows":
        appdata = os.getenv("APPDATA")
        if appdata:
            log_dir = Path(appdata) / "MathHeartPlayer" / "logs"
        else:
            # Fallback to user home
            log_dir = Path.home() / ".mathheart_player" / "logs"
    elif system == "Darwin":  # macOS
        log_dir = Path.home() / "Library" / "Logs" / "mathheart_player"
    else:  # Linux and other Unix-like systems
        log_dir = Path.home() / ".cache" / "mathheart_player" / "logs"
    
    # Create directory if it doesn't exist
    log_dir.mkdir(parents=True, exist_ok=True)
    
    return log_dir


def get_log_file_path() -> Path:
    """
    Get the log file path with date-based naming.
    
    Returns:
        Path to today's log file
    """
    log_dir = get_log_directory()
    date_str = datetime.now().strftime("%Y-%m-%d")
    return log_dir / f"mathheart_player_{date_str}.log"


def sanitize_path(filepath: str) -> str:
    """
    Sanitize file paths for logging (remove user home directory).
    
    Parameters:
        filepath: Full file path
        
    Returns:
        Sanitized path (relative or filename only)
    """
    try:
        path = Path(filepath)
        home = Path.home()
        
        # Try to make path relative to home
        try:
            return str(path.relative_to(home))
        except ValueError:
            # Not under home, return just filename
            return path.name
    except Exception:
        # If anything fails, return just the filename
        return os.path.basename(filepath) if filepath else "unknown"


def setup_logging(
    console_level: int = logging.INFO,
    file_level: int = logging.DEBUG,
    debug_mode: bool = False,
    verbose_mode: bool = False
) -> None:
    """
    Setup logging configuration for MathHeart Player.
    
    Parameters:
        console_level: Logging level for console output
        file_level: Logging level for file output
        debug_mode: If True, enable DEBUG level for console
        verbose_mode: If True, enable more detailed INFO messages
    """
    # Adjust console level based on flags
    if debug_mode:
        console_level = logging.DEBUG
    elif verbose_mode:
        console_level = logging.INFO  # Already INFO, but can be more verbose
    
    # Get root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)  # Set to lowest level, handlers filter
    
    # Clear any existing handlers
    root_logger.handlers.clear()
    
    # Create formatter
    formatter = logging.Formatter(
        '[%(asctime)s.%(msecs)03d] [%(levelname)s] [%(name)s] - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(console_level)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # File handler with rotation (one file per day)
    log_file = get_log_file_path()
    file_handler = logging.handlers.TimedRotatingFileHandler(
        filename=str(log_file),
        when='midnight',
        interval=1,
        backupCount=7,  # Keep last 7 days
        encoding='utf-8'
    )
    file_handler.setLevel(file_level)
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)
    
    # Log startup message
    logger = logging.getLogger(__name__)
    logger.info("=" * 60)
    logger.info("MathHeart Player - Logging initialized")
    logger.info(f"Console log level: {logging.getLevelName(console_level)}")
    logger.info(f"File log level: {logging.getLevelName(file_level)}")
    logger.info(f"Log file: {log_file}")
    logger.info("=" * 60)
    
    # Clean up old log files (older than 30 days)
    cleanup_old_logs(days=30)


def cleanup_old_logs(days: int = 30) -> None:
    """
    Clean up log files older than specified days.
    
    Parameters:
        days: Number of days to keep logs (default: 30)
    """
    try:
        log_dir = get_log_directory()
        if not log_dir.exists():
            return
        
        cutoff_time = datetime.now().timestamp() - (days * 24 * 60 * 60)
        deleted_count = 0
        
        for log_file in log_dir.glob("mathheart_player_*.log*"):
            try:
                if log_file.stat().st_mtime < cutoff_time:
                    log_file.unlink()
                    deleted_count += 1
            except Exception:
                pass  # Skip files that can't be deleted
        
        if deleted_count > 0:
            logger = logging.getLogger(__name__)
            logger.debug(f"Cleaned up {deleted_count} old log file(s)")
    except Exception as e:
        # Don't fail if cleanup fails
        pass

