"""
Analysis Cache Module for MathHeart Player
Manages caching of pre-analyzed audio features to disk.
"""

import os
import json
import hashlib
import logging
import platform
from pathlib import Path

from mathheart_player.utils.logger import sanitize_path

logger = logging.getLogger(__name__)


def get_cache_directory():
    """
    Get OS-specific cache directory for MathHeart Player.
    
    Returns:
        Path to cache directory
    """
    system = platform.system()
    
    if system == "Windows":
        cache_dir = Path(os.getenv("APPDATA", "")) / "MathHeartPlayer" / "cache"
    elif system == "Darwin":  # macOS
        cache_dir = Path.home() / "Library" / "Caches" / "mathheart_player"
    else:  # Linux and others
        cache_dir = Path.home() / ".cache" / "mathheart_player"
    
    # Create directory if it doesn't exist
    cache_dir.mkdir(parents=True, exist_ok=True)
    
    return cache_dir


def get_cache_key(filepath):
    """
    Generate cache key from file path, modification time, and size.
    
    Parameters:
        filepath: Path to audio file
        
    Returns:
        Cache key string
    """
    try:
        stat = os.stat(filepath)
        mtime = stat.st_mtime
        size = stat.st_size
        # Create hash from filepath, mtime, and size
        key_string = f"{filepath}_{mtime}_{size}"
        return hashlib.md5(key_string.encode()).hexdigest()
    except OSError:
        return None


def get_cache_path(filepath):
    """
    Get cache file path for given audio file.
    
    Parameters:
        filepath: Path to audio file
        
    Returns:
        Path to cache file
    """
    cache_key = get_cache_key(filepath)
    if cache_key is None:
        return None
    
    cache_dir = get_cache_directory()
    return cache_dir / f"{cache_key}.json"


def load_from_cache(filepath):
    """
    Load pre-analyzed features from cache if available and valid.
    
    Parameters:
        filepath: Path to audio file
        
    Returns:
        Dictionary with audio features if cache hit, None otherwise
    """
    file_name = sanitize_path(filepath)
    cache_path = get_cache_path(filepath)
    if cache_path is None or not cache_path.exists():
        logger.debug(f"Cache miss: No cache file found for {file_name}")
        return None
    
    try:
        # Verify cache is still valid (file hasn't changed)
        current_key = get_cache_key(filepath)
        if current_key is None:
            logger.warning(f"Cache miss: Cannot generate cache key for {file_name}")
            return None
        
        # Check if cache file matches current file
        expected_cache_path = get_cache_path(filepath)
        if cache_path != expected_cache_path:
            # File has changed, cache is invalid
            logger.debug(f"Cache miss: File changed, cache invalid for {file_name}")
            return None
        
        # Load cache
        with open(cache_path, 'r') as f:
            features = json.load(f)
        
        cache_size_kb = cache_path.stat().st_size / 1024
        logger.debug(f"Cache hit: Loaded {cache_size_kb:.2f}KB from cache for {file_name}")
        return features
    except (json.JSONDecodeError, IOError, OSError) as e:
        # Cache file is corrupted or unreadable
        logger.warning(f"Cache error: Corrupted or unreadable cache file for {file_name}: {e}")
        # Try to remove corrupted cache
        try:
            if cache_path and cache_path.exists():
                cache_path.unlink()
                logger.debug(f"Removed corrupted cache file: {file_name}")
        except Exception:
            pass
        return None


def save_to_cache(filepath, features):
    """
    Save pre-analyzed features to cache.
    
    Parameters:
        filepath: Path to audio file
        features: Dictionary with audio features (from analyze_audio.py format)
        
    Returns:
        True if successful, False otherwise
    """
    file_name = sanitize_path(filepath)
    cache_path = get_cache_path(filepath)
    if cache_path is None:
        logger.warning(f"Cache save failed: Cannot generate cache path for {file_name}")
        return False
    
    try:
        # Ensure cache directory exists
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Save features to cache
        with open(cache_path, 'w') as f:
            json.dump(features, f, indent=2)
        
        cache_size_kb = cache_path.stat().st_size / 1024
        logger.debug(f"Cache saved: {cache_size_kb:.2f}KB to cache for {file_name}")
        return True
    except (IOError, OSError) as e:
        logger.error(f"Cache save failed: {file_name} - {e}", exc_info=True)
        return False


def clear_cache(filepath=None):
    """
    Clear cache for specific file or entire cache directory.
    
    Parameters:
        filepath: Path to audio file (if None, clears entire cache)
        
    Returns:
        True if successful, False otherwise
    """
    try:
        if filepath is None:
            # Clear entire cache
            cache_dir = get_cache_directory()
            count = 0
            for cache_file in cache_dir.glob("*.json"):
                cache_file.unlink()
                count += 1
            logger.info(f"Cache cleared: Removed {count} cache file(s)")
            return True
        else:
            # Clear specific file cache
            file_name = sanitize_path(filepath)
            cache_path = get_cache_path(filepath)
            if cache_path and cache_path.exists():
                cache_path.unlink()
                logger.info(f"Cache cleared for: {file_name}")
                return True
            logger.debug(f"No cache to clear for: {file_name}")
            return False
    except (IOError, OSError) as e:
        logger.error(f"Cache clear failed: {e}", exc_info=True)
        return False


def get_cache_size():
    """
    Get total size of cache directory in bytes.
    
    Returns:
        Total cache size in bytes
    """
    cache_dir = get_cache_directory()
    total_size = 0
    
    try:
        for cache_file in cache_dir.glob("*.json"):
            total_size += cache_file.stat().st_size
    except (IOError, OSError):
        pass
    
    return total_size

