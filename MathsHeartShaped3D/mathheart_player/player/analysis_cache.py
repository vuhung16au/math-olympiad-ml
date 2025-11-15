"""
Analysis Cache Module for MathHeart Player
Manages caching of pre-analyzed audio features to disk.
"""

import os
import json
import hashlib
import platform
from pathlib import Path


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
    cache_path = get_cache_path(filepath)
    if cache_path is None or not cache_path.exists():
        return None
    
    try:
        # Verify cache is still valid (file hasn't changed)
        current_key = get_cache_key(filepath)
        if current_key is None:
            return None
        
        # Check if cache file matches current file
        expected_cache_path = get_cache_path(filepath)
        if cache_path != expected_cache_path:
            # File has changed, cache is invalid
            return None
        
        # Load cache
        with open(cache_path, 'r') as f:
            features = json.load(f)
        
        return features
    except (json.JSONDecodeError, IOError, OSError):
        # Cache file is corrupted or unreadable
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
    cache_path = get_cache_path(filepath)
    if cache_path is None:
        return False
    
    try:
        # Ensure cache directory exists
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Save features to cache
        with open(cache_path, 'w') as f:
            json.dump(features, f, indent=2)
        
        return True
    except (IOError, OSError):
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
            for cache_file in cache_dir.glob("*.json"):
                cache_file.unlink()
            return True
        else:
            # Clear specific file cache
            cache_path = get_cache_path(filepath)
            if cache_path and cache_path.exists():
                cache_path.unlink()
                return True
            return False
    except (IOError, OSError):
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

