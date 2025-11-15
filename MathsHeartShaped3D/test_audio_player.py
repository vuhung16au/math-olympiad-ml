"""
Debug script for MathHeart Player audio loading
Tests MP3 loading and conversion with progress reporting
"""

import sys
import os

# Add parent directory to path
parent_dir = os.path.dirname(os.path.abspath(__file__))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from mathheart_player.player.audio_player import AudioPlayer

def test_audio_loading(filepath):
    """Test audio loading with progress reporting."""
    print(f"\n{'='*60}")
    print(f"Testing audio loading: {filepath}")
    print(f"{'='*60}\n")
    
    if not os.path.exists(filepath):
        print(f"ERROR: File not found: {filepath}")
        return False
    
    player = AudioPlayer()
    
    # Progress callback for testing
    def progress_callback(message, progress):
        progress_pct = int(progress * 100)
        bar_length = 40
        filled = int(bar_length * progress)
        bar = '█' * filled + '░' * (bar_length - filled)
        print(f"\r[{bar}] {progress_pct:3d}% - {message}", end='', flush=True)
    
    print("Starting load...")
    try:
        success = player.load_file(filepath, progress_callback=progress_callback)
        print("\n")  # New line after progress
        
        if success:
            print(f"✓ SUCCESS: File loaded")
            print(f"  Duration: {player.get_duration():.2f} seconds")
            print(f"  Using mixer.music: {player.use_music}")
            if player.temp_wav_file:
                print(f"  Temp WAV file: {player.temp_wav_file}")
            return True
        else:
            print(f"✗ FAILED: Could not load file")
            return False
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        player.cleanup()

if __name__ == "__main__":
    # Test with a file if provided, otherwise use default
    if len(sys.argv) > 1:
        test_file = sys.argv[1]
    else:
        # Try to find a test file
        test_file = "inputs/Etherreal60.mp3"
        if not os.path.exists(test_file):
            test_file = "inputs/EtherealHorizons.mp3"
    
    if os.path.exists(test_file):
        test_audio_loading(test_file)
    else:
        print(f"Usage: python test_audio_player.py <audio_file>")
        print(f"Or place a test file in inputs/ directory")
        print(f"\nLooking for: {test_file}")

