"""
Audio Player Module for MathHeart Player
Handles audio playback using pygame.mixer with MP3 support via pydub
"""

import os
import time
import threading
import pygame
import tempfile
from typing import Optional, Callable
from pydub import AudioSegment


class AudioPlayer:
    """Audio player with play/pause/stop/seek functionality."""
    
    def __init__(self):
        """Initialize audio player."""
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        self.current_file: Optional[str] = None
        self.sound: Optional[pygame.mixer.Sound] = None
        self.channel: Optional[pygame.mixer.Channel] = None
        self.temp_wav_file: Optional[str] = None  # For MP3 conversion
        self.use_music = False  # Use mixer.music for MP3 files
        self.is_playing = False
        self.is_paused = False
        self.start_time = 0.0
        self.pause_position = 0.0
        self.duration = 0.0
        self._lock = threading.Lock()
        
    def load_file(self, filepath: str, progress_callback: Optional[Callable[[str, float], None]] = None) -> bool:
        """
        Load audio file for playback.
        Converts MP3 to WAV if needed (pygame doesn't support MP3 on Windows).
        
        Parameters:
            filepath: Path to audio file (.wav, .mp3, .m4a, .flac)
            
        Returns:
            True if successful, False otherwise
        """
        if not os.path.exists(filepath):
            return False
        
        try:
            with self._lock:
                # Stop current playback if any
                self.stop()
                
                # Clean up old temp file if exists
                if self.temp_wav_file and os.path.exists(self.temp_wav_file):
                    try:
                        os.remove(self.temp_wav_file)
                    except:
                        pass
                self.temp_wav_file = None
                
                # Check file extension
                file_ext = os.path.splitext(filepath)[1].lower()
                
                # Try pygame.mixer.music for MP3 files first (much faster, no conversion)
                if file_ext == '.mp3':
                    try:
                        if progress_callback:
                            progress_callback("Loading MP3 file...", 0.1)
                        
                        # Try using mixer.music which supports MP3 natively
                        pygame.mixer.music.load(filepath)
                        
                        if progress_callback:
                            progress_callback("Reading MP3 metadata...", 0.3)
                        
                        # Get duration using pydub (fast, just reads metadata)
                        try:
                            audio = AudioSegment.from_mp3(filepath)
                            self.duration = len(audio) / 1000.0
                        except:
                            # Fallback: estimate from file size if metadata read fails
                            file_size = os.path.getsize(filepath)
                            # Rough estimate: ~1MB per minute for 128kbps MP3
                            self.duration = (file_size / 1024 / 1024) * 60
                        
                        if progress_callback:
                            progress_callback("MP3 file loaded", 1.0)
                        
                        self.use_music = True
                        self.sound = None
                        self.current_file = filepath
                        self.pause_position = 0.0
                        self.is_paused = False
                        return True
                    except Exception as e:
                        print(f"Error loading MP3 with mixer.music, trying conversion: {e}")
                        if progress_callback:
                            progress_callback("MP3 direct load failed, converting to WAV...", 0.1)
                        # Fall back to conversion if mixer.music doesn't work
                        pass
                
                # For MP3 (if mixer.music failed) and other formats, convert to WAV
                if file_ext in ['.mp3', '.m4a', '.flac', '.ogg']:
                    try:
                        if progress_callback:
                            progress_callback("Loading audio file for conversion...", 0.1)
                        
                        # Use lower quality for faster conversion
                        audio = AudioSegment.from_file(filepath)
                        self.duration = len(audio) / 1000.0
                        
                        if progress_callback:
                            progress_callback("Processing audio (downsampling)...", 0.3)
                        
                        # Downsample to 22050 Hz for faster conversion and smaller file
                        audio = audio.set_frame_rate(22050)
                        
                        if progress_callback:
                            progress_callback("Converting to mono...", 0.4)
                        
                        # Convert to mono for smaller file
                        audio = audio.set_channels(1)
                        
                        # Create temporary WAV file
                        self.temp_wav_file = os.path.join(
                            tempfile.gettempdir(),
                            f"mathheart_temp_{os.getpid()}_{int(time.time())}.wav"
                        )
                        
                        if progress_callback:
                            progress_callback("Converting to WAV format...", 0.5)
                        
                        # Export as WAV with lower quality for speed
                        # Use threading to monitor progress during export
                        import threading
                        conversion_done = threading.Event()
                        conversion_error = [None]
                        
                        def do_export():
                            try:
                                audio.export(self.temp_wav_file, format="wav", parameters=["-acodec", "pcm_s16le"])
                                conversion_done.set()
                            except Exception as e:
                                conversion_error[0] = e
                                conversion_done.set()
                        
                        export_thread = threading.Thread(target=do_export, daemon=True)
                        export_thread.start()
                        
                        # Simulate progress during conversion (estimate based on duration)
                        start_time = time.time()
                        estimated_time = self.duration * 0.1  # Rough estimate: 10% of audio duration
                        
                        while not conversion_done.is_set():
                            elapsed = time.time() - start_time
                            if estimated_time > 0:
                                progress = min(0.5 + (elapsed / estimated_time) * 0.4, 0.9)
                            else:
                                progress = min(0.5 + elapsed * 0.1, 0.9)
                            
                            if progress_callback:
                                progress_callback(f"Converting to WAV... ({int(progress * 100)}%)", progress)
                            
                            if elapsed > 60:  # Timeout after 60 seconds
                                break
                            
                            time.sleep(0.1)  # Update every 100ms
                        
                        export_thread.join(timeout=1)
                        
                        if conversion_error[0]:
                            raise conversion_error[0]
                        
                        if progress_callback:
                            progress_callback("Loading converted WAV file...", 0.95)
                        
                        # Load with pygame
                        self.sound = pygame.mixer.Sound(self.temp_wav_file)
                        self.use_music = False
                        self.current_file = filepath
                        self.pause_position = 0.0
                        self.is_paused = False
                        
                        if progress_callback:
                            progress_callback("Audio file loaded", 1.0)
                        
                        return True
                    except Exception as e:
                        print(f"Error converting audio file: {e}")
                        import traceback
                        traceback.print_exc()
                        if progress_callback:
                            progress_callback("Conversion failed", 0.0)
                        return False
                else:
                    # For WAV files, load directly
                    try:
                        if progress_callback:
                            progress_callback("Loading WAV file...", 0.5)
                        
                        self.sound = pygame.mixer.Sound(filepath)
                        self.use_music = False
                        self.current_file = filepath
                        self.duration = self.sound.get_length()
                        self.pause_position = 0.0
                        self.is_paused = False
                        
                        if progress_callback:
                            progress_callback("WAV file loaded", 1.0)
                        
                        return True
                    except Exception as e:
                        print(f"Error loading audio file: {e}")
                        if progress_callback:
                            progress_callback("Failed to load file", 0.0)
                        return False
        except Exception as e:
            print(f"Error loading audio file: {e}")
            return False
    
    def play(self) -> bool:
        """
        Start or resume playback.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            with self._lock:
                if self.use_music:
                    # Use mixer.music for MP3 files
                    if self.is_paused:
                        # Resume from pause position (track manually since mixer.music doesn't support seeking)
                        pygame.mixer.music.play()
                        self.start_time = time.time() - self.pause_position
                        self.is_paused = False
                    else:
                        # Start new playback
                        pygame.mixer.music.play()
                        self.start_time = time.time()
                        self.pause_position = 0.0
                    
                    self.is_playing = True
                    return True
                elif self.sound is None:
                    return False
                else:
                    # Use Sound object for WAV files
                    if self.is_paused:
                        # Resume from pause position
                        self.channel = self.sound.play()
                        self.start_time = time.time() - self.pause_position
                        self.is_paused = False
                    else:
                        # Start new playback
                        self.channel = self.sound.play()
                        self.start_time = time.time()
                        self.pause_position = 0.0
                    
                    self.is_playing = True
                    return True
        except Exception as e:
            print(f"Error playing audio: {e}")
            return False
    
    def pause(self):
        """Pause playback."""
        with self._lock:
            if self.is_playing and not self.is_paused:
                self.pause_position = self.get_current_time()
                if self.use_music:
                    pygame.mixer.music.pause()
                elif self.channel:
                    self.channel.pause()
                self.is_paused = True
                self.is_playing = False
    
    def stop(self):
        """Stop playback."""
        with self._lock:
            if self.use_music:
                pygame.mixer.music.stop()
            elif self.channel:
                self.channel.stop()
            self.is_playing = False
            self.is_paused = False
            self.pause_position = 0.0
            self.start_time = 0.0
    
    def seek(self, position: float) -> bool:
        """
        Seek to specific position in audio.
        
        Note: pygame.mixer has limited seeking support. This implementation
        tracks position manually but cannot actually seek within the audio stream.
        For better seeking, consider using pydub with simpleaudio.
        
        Parameters:
            position: Time position in seconds
            
        Returns:
            True if successful, False otherwise
        """
        if position < 0 or position > self.duration:
            return False
        
        try:
            with self._lock:
                was_playing = self.is_playing and not self.is_paused
                
                # Stop current playback
                if self.use_music:
                    pygame.mixer.music.stop()
                elif self.channel:
                    self.channel.stop()
                
                # Update position
                self.pause_position = position
                
                # Resume if was playing
                if was_playing:
                    if self.use_music:
                        # For mixer.music, restart from beginning and track offset
                        # Note: mixer.music doesn't support seeking, so we track manually
                        pygame.mixer.music.play()
                        self.start_time = time.time() - position
                    elif self.sound:
                        # Note: pygame doesn't support seeking, so we restart from beginning
                        # and track time offset manually
                        self.channel = self.sound.play()
                        self.start_time = time.time() - position
                    self.is_playing = True
                    self.is_paused = False
                else:
                    self.is_playing = False
                    self.is_paused = True
                
                return True
        except Exception as e:
            print(f"Error seeking audio: {e}")
            return False
    
    def get_current_time(self) -> float:
        """
        Get current playback time in seconds.
        
        Returns:
            Current playback time
        """
        with self._lock:
            if self.use_music:
                # For mixer.music, track time manually
                if self.is_paused:
                    return self.pause_position
                if self.is_playing:
                    elapsed = time.time() - self.start_time
                    if elapsed >= self.duration or not pygame.mixer.music.get_busy():
                        # Playback finished
                        self.is_playing = False
                        return self.duration
                    return min(elapsed, self.duration)
                return 0.0
            
            if self.sound is None:
                return 0.0
            
            if self.is_paused:
                return self.pause_position
            
            if self.is_playing and self.channel:
                # Check if channel is still playing
                if self.channel.get_busy():
                    elapsed = time.time() - self.start_time
                    return min(elapsed, self.duration)
                else:
                    # Playback finished
                    self.is_playing = False
                    return self.duration
            
            return 0.0
    
    def get_duration(self) -> float:
        """
        Get total duration of loaded audio file.
        
        Returns:
            Duration in seconds
        """
        return self.duration
    
    def set_volume(self, volume: float):
        """
        Set playback volume.
        
        Parameters:
            volume: Volume level (0.0 to 1.0)
        """
        volume = max(0.0, min(1.0, volume))
        with self._lock:
            if self.use_music:
                pygame.mixer.music.set_volume(volume)
            elif self.channel:
                self.channel.set_volume(volume)
    
    def get_volume(self) -> float:
        """
        Get current playback volume.
        
        Returns:
            Volume level (0.0 to 1.0)
        """
        if self.channel:
            return self.channel.get_volume()
        return 1.0
    
    def is_playing_audio(self) -> bool:
        """
        Check if audio is currently playing.
        
        Returns:
            True if playing, False otherwise
        """
        with self._lock:
            if self.is_playing:
                if self.use_music:
                    return pygame.mixer.music.get_busy()
                elif self.channel:
                    return self.channel.get_busy()
            return False
    
    def cleanup(self):
        """Clean up resources."""
        self.stop()
        
        # Clean up temp file
        if self.temp_wav_file and os.path.exists(self.temp_wav_file):
            try:
                os.remove(self.temp_wav_file)
            except:
                pass
        
        pygame.mixer.quit()

