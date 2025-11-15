"""
Main Window for MathHeart Player
"""

import os
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QSlider, QLabel, QFileDialog, QComboBox,
    QStatusBar, QProgressBar, QMessageBox
)
from PyQt6.QtCore import QTimer, Qt, pyqtSignal, QThread
from PyQt6.QtGui import QAction

from mathheart_player.player.audio_player import AudioPlayer
from mathheart_player.player.audio_analyzer import AudioAnalyzer
from mathheart_player.ui.visualization_panel import VisualizationPanel


class AudioLoadWorker(QThread):
    """Worker thread for loading audio file (MP3 conversion can be slow)."""
    
    progress = pyqtSignal(str, float)  # message, progress (0-1)
    finished = pyqtSignal(bool, str, object)  # success, filepath, audio_player
    
    def __init__(self, filepath: str, audio_player):
        """Initialize worker thread."""
        super().__init__()
        self.filepath = filepath
        self.audio_player = audio_player
    
    def run(self):
        """Load audio file in background thread."""
        try:
            # Pass progress callback to audio player
            def on_progress(message: str, progress: float):
                self.progress.emit(message, progress)
            
            success = self.audio_player.load_file(self.filepath, progress_callback=on_progress)
            if success:
                self.progress.emit("Audio file loaded successfully", 1.0)
            else:
                self.progress.emit("Failed to load audio file", 0.0)
            self.finished.emit(success, self.filepath, self.audio_player)
        except Exception as e:
            print(f"Error in audio load thread: {e}")
            import traceback
            traceback.print_exc()
            self.progress.emit(f"Error: {str(e)}", 0.0)
            self.finished.emit(False, self.filepath, self.audio_player)


class AudioAnalysisWorker(QThread):
    """Worker thread for audio analysis to prevent UI blocking."""
    
    progress = pyqtSignal(str, float)  # message, progress (0-1)
    finished = pyqtSignal(bool, str)  # success, filepath
    
    def __init__(self, filepath: str, use_cache: bool = True):
        """Initialize worker thread."""
        super().__init__()
        self.filepath = filepath
        self.use_cache = use_cache
        self.analyzer = AudioAnalyzer(progress_callback=self.on_progress)
    
    def on_progress(self, message: str, progress: float):
        """Forward progress updates to main thread."""
        self.progress.emit(message, progress)
    
    def run(self):
        """Run audio analysis in background thread."""
        try:
            success = self.analyzer.load_file(self.filepath, self.use_cache)
            self.finished.emit(success, self.filepath)
        except Exception as e:
            print(f"Error in analysis thread: {e}")
            import traceback
            traceback.print_exc()
            self.finished.emit(False, self.filepath)


class MainWindow(QMainWindow):
    """Main application window."""
    
    def __init__(self):
        """Initialize main window."""
        super().__init__()
        
        self.setWindowTitle("MathHeart Player")
        self.setGeometry(100, 100, 1200, 800)
        
        # Initialize components
        self.audio_player = AudioPlayer()
        self.audio_analyzer = AudioAnalyzer(progress_callback=self.on_analysis_progress)
        self.current_file = None
        self.load_worker = None  # Background thread for loading audio
        self.analysis_worker = None  # Background thread for analysis
        
        # Setup UI
        self.setup_ui()
        self.setup_menu()
        
        # Setup update timer for visualization (30 FPS)
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_visualization)
        self.update_timer.setInterval(33)  # ~30 FPS
        
        # Setup seek timer
        self.seek_timer = QTimer()
        self.seek_timer.timeout.connect(self.update_seek_bar)
        self.seek_timer.setInterval(100)  # Update every 100ms
        
    def setup_ui(self):
        """Setup user interface."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # Visualization panel
        self.visualization_panel = VisualizationPanel()
        layout.addWidget(self.visualization_panel, stretch=1)
        
        # Controls panel
        controls_layout = QVBoxLayout()
        
        # File selection
        file_layout = QHBoxLayout()
        self.file_label = QLabel("No file loaded")
        self.browse_button = QPushButton("Browse...")
        self.browse_button.clicked.connect(self.browse_file)
        file_layout.addWidget(self.file_label)
        file_layout.addWidget(self.browse_button)
        controls_layout.addLayout(file_layout)
        
        # Effect selector
        effect_layout = QHBoxLayout()
        effect_layout.addWidget(QLabel("Effect:"))
        self.effect_combo = QComboBox()
        self.effect_combo.addItems(["Auto-select", "H8sync", "H9", "H10"])
        self.effect_combo.currentTextChanged.connect(self.on_effect_changed)
        effect_layout.addWidget(self.effect_combo)
        controls_layout.addLayout(effect_layout)
        
        # Playback controls
        playback_layout = QHBoxLayout()
        self.play_button = QPushButton("Play")
        self.play_button.clicked.connect(self.toggle_playback)
        self.pause_button = QPushButton("Pause")
        self.pause_button.clicked.connect(self.pause_playback)
        self.stop_button = QPushButton("Stop")
        self.stop_button.clicked.connect(self.stop_playback)
        playback_layout.addWidget(self.play_button)
        playback_layout.addWidget(self.pause_button)
        playback_layout.addWidget(self.stop_button)
        controls_layout.addLayout(playback_layout)
        
        # Seek bar
        seek_layout = QHBoxLayout()
        self.time_label = QLabel("00:00 / 00:00")
        self.seek_slider = QSlider(Qt.Orientation.Horizontal)
        self.seek_slider.setMinimum(0)
        self.seek_slider.setMaximum(1000)
        self.seek_slider.valueChanged.connect(self.on_seek_changed)
        self.seek_slider.sliderPressed.connect(lambda: self.seek_timer.stop())
        self.seek_slider.sliderReleased.connect(lambda: self.seek_timer.start())
        seek_layout.addWidget(self.time_label)
        seek_layout.addWidget(self.seek_slider)
        controls_layout.addLayout(seek_layout)
        
        # Volume control
        volume_layout = QHBoxLayout()
        volume_layout.addWidget(QLabel("Volume:"))
        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setMinimum(0)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setValue(100)
        self.volume_slider.valueChanged.connect(self.on_volume_changed)
        volume_layout.addWidget(self.volume_slider)
        controls_layout.addLayout(volume_layout)
        
        layout.addLayout(controls_layout)
        
        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
        
        # Progress bar for analysis
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.status_bar.addPermanentWidget(self.progress_bar)
    
    def setup_menu(self):
        """Setup menu bar."""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("File")
        open_action = QAction("Open...", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.browse_file)
        file_menu.addAction(open_action)
        
        file_menu.addSeparator()
        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Help menu
        help_menu = menubar.addMenu("Help")
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def browse_file(self):
        """Browse for audio file."""
        filepath, _ = QFileDialog.getOpenFileName(
            self,
            "Open Audio File",
            "",
            "Audio Files (*.mp3 *.wav *.m4a *.flac);;All Files (*)"
        )
        
        if filepath:
            self.load_file(filepath)
    
    def load_file(self, filepath: str):
        """Load audio file."""
        # Cancel any ongoing operations
        if self.load_worker and self.load_worker.isRunning():
            self.load_worker.terminate()
            self.load_worker.wait()
        if self.analysis_worker and self.analysis_worker.isRunning():
            self.analysis_worker.terminate()
            self.analysis_worker.wait()
        
        self.current_file = filepath
        self.file_label.setText(f"Loading: {os.path.basename(filepath)}...")
        self.status_bar.showMessage("Loading file...")
        
        # Show progress bar
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        
        # Disable controls during loading
        self.browse_button.setEnabled(False)
        self.play_button.setEnabled(False)
        
        # Load audio file in background thread (MP3 conversion can be slow)
        self.load_worker = AudioLoadWorker(filepath, self.audio_player)
        self.load_worker.progress.connect(self.on_analysis_progress)
        self.load_worker.finished.connect(self.on_audio_load_finished)
        self.load_worker.start()
    
    def on_audio_load_finished(self, success: bool, filepath: str, audio_player):
        """Handle completion of audio file loading."""
        if not success or filepath != self.current_file:
            # Loading failed or user selected different file
            self.browse_button.setEnabled(True)
            self.play_button.setEnabled(False)
            self.progress_bar.setVisible(False)
            if not success:
                QMessageBox.warning(
                    self, 
                    "Error", 
                    f"Failed to load audio file.\n\n"
                    f"Make sure:\n"
                    f"- The file is not corrupted\n"
                    f"- For MP3 files, ffmpeg must be installed and in PATH\n"
                    f"- Try a WAV file if MP3 doesn't work"
                )
                self.file_label.setText("No file loaded")
                self.status_bar.showMessage("Failed to load audio file")
            return
        
        # File loaded successfully, update label
        self.file_label.setText(f"✓ {os.path.basename(filepath)}")
        self.status_bar.showMessage("Starting analysis...")
        
        # Now start analysis in background thread
        self.analysis_worker = AudioAnalysisWorker(filepath, use_cache=True)
        self.analysis_worker.progress.connect(self.on_analysis_progress)
        self.analysis_worker.finished.connect(self.on_analysis_finished)
        self.analysis_worker.start()
    
    def on_analysis_finished(self, success: bool, filepath: str):
        """Handle completion of audio analysis."""
        # Re-enable controls
        self.browse_button.setEnabled(True)
        self.play_button.setEnabled(True)
        self.progress_bar.setVisible(False)
        
        if success and filepath == self.current_file:
            # Get analyzer from worker thread
            self.audio_analyzer = self.analysis_worker.analyzer
            
            # Load features into visualizer
            self.visualization_panel.load_audio_features(self.audio_analyzer)
            
            # Update seek bar range
            duration = self.audio_analyzer.get_duration()
            if duration > 0:
                self.seek_slider.setMaximum(int(duration * 10))  # 0.1s precision
            else:
                # Fallback to audio player duration if analyzer doesn't have it
                duration = self.audio_player.get_duration()
                if duration > 0:
                    self.seek_slider.setMaximum(int(duration * 10))
            
            # Auto-select effect if needed
            if self.effect_combo.currentText() == "Auto-select" and duration > 0:
                self.auto_select_effect(duration)
            
            # Update file label to show it's loaded
            self.file_label.setText(f"✓ {os.path.basename(filepath)}")
            self.status_bar.showMessage("File loaded successfully")
        else:
            if not success:
                error_msg = "Failed to analyze audio file"
                QMessageBox.warning(self, "Error", error_msg)
                self.status_bar.showMessage("Analysis failed")
                self.file_label.setText(f"✗ {os.path.basename(filepath) if filepath else 'No file loaded'}")
            # If filepath changed, user loaded a different file, ignore this result
    
    def auto_select_effect(self, duration: float):
        """Auto-select effect based on duration."""
        # Reuse logic from visualise_audio.py
        if duration < 30:
            effect = 'H8sync'
        elif duration < 120:
            effect = 'H8sync'
        elif duration < 300:
            effect = 'H8sync'  # Could use H8sync3min if available
        else:
            effect = 'H9'
        
        # Find and set effect in combo
        index = self.effect_combo.findText(effect)
        if index >= 0:
            self.effect_combo.setCurrentIndex(index)
    
    def on_effect_changed(self, effect_name: str):
        """Handle effect selection change."""
        if effect_name != "Auto-select":
            self.visualization_panel.set_effect(effect_name)
    
    def toggle_playback(self):
        """Toggle play/pause."""
        if self.audio_player.is_playing_audio():
            self.pause_playback()
        else:
            # Resume or start playback
            if self.audio_player.play():
                self.update_timer.start()
                self.seek_timer.start()
                self.status_bar.showMessage("Playing")
            else:
                self.status_bar.showMessage("Failed to play audio")
    
    def pause_playback(self):
        """Pause playback."""
        self.audio_player.pause()
        self.update_timer.stop()
        self.seek_timer.stop()
        self.status_bar.showMessage("Paused")
    
    def stop_playback(self):
        """Stop playback."""
        self.audio_player.stop()
        self.update_timer.stop()
        self.seek_timer.stop()
        self.seek_slider.setValue(0)
        self.time_label.setText("00:00 / 00:00")
        self.status_bar.showMessage("Stopped")
    
    def on_seek_changed(self, value: int):
        """Handle seek bar change."""
        position = value / 10.0  # Convert to seconds (0.1s precision)
        self.audio_player.seek(position)
        self.update_time_display()
    
    def update_seek_bar(self):
        """Update seek bar position."""
        if self.audio_player.is_playing_audio():
            current_time = self.audio_player.get_current_time()
            self.seek_slider.setValue(int(current_time * 10))
            self.update_time_display()
    
    def update_time_display(self):
        """Update time display label."""
        current = self.audio_player.get_current_time()
        total = self.audio_player.get_duration()
        
        current_str = self.format_time(current)
        total_str = self.format_time(total)
        self.time_label.setText(f"{current_str} / {total_str}")
    
    def format_time(self, seconds: float) -> str:
        """Format time in MM:SS format."""
        mins = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{mins:02d}:{secs:02d}"
    
    def on_volume_changed(self, value: int):
        """Handle volume change."""
        volume = value / 100.0
        self.audio_player.set_volume(volume)
    
    def update_visualization(self):
        """Update visualization based on current playback time."""
        if self.audio_player.is_playing_audio():
            current_time = self.audio_player.get_current_time()
            self.visualization_panel.update_visualization(current_time)
    
    def on_analysis_progress(self, message: str, progress: float):
        """Handle analysis progress updates."""
        self.progress_bar.setValue(int(progress * 100))
        self.status_bar.showMessage(message)
    
    def show_about(self):
        """Show about dialog."""
        QMessageBox.about(
            self,
            "About MathHeart Player",
            "MathHeart Player\n\n"
            "Where mathematics meets music\n\n"
            "A media player that visualizes music through mathematical 3D heart shapes, "
            "synchronized in real-time with audio analysis.\n\n"
            "Version 0.1.0"
        )
    
    def closeEvent(self, event):
        """Handle window close event."""
        # Stop any ongoing operations
        if self.load_worker and self.load_worker.isRunning():
            self.load_worker.terminate()
            self.load_worker.wait()
        if self.analysis_worker and self.analysis_worker.isRunning():
            self.analysis_worker.terminate()
            self.analysis_worker.wait()
        
        # Cleanup audio player
        self.audio_player.cleanup()
        event.accept()

