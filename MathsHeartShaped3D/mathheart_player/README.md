# MathHeart Player

**Tagline:** "Where mathematics meets music"

## Description

MathHeart Player is a cross-platform media player that visualizes music through mathematical 3D heart shapes, synchronized in real-time with audio analysis. It supports multiple audio formats (.wav, .mp3, .midi) and provides stunning visualizations that react to the music's beats, tempo, loudness, and bass.

## Features

- Real-time 3D heart visualization synchronized to audio
- Multiple visualization effects (H8sync, H9, H10)
- Hybrid audio analysis (pre-analyze with caching + streaming fallback)
- Support for .wav, .mp3, and .midi formats
- Cross-platform (Windows, Linux, macOS)

## Installation

### Using Virtual Environment (Recommended)

1. **Create a virtual environment:**

   On Windows:
   ```powershell
   python -m venv venv
   ```

   On Linux/macOS:
   ```bash
   python3 -m venv venv
   ```

2. **Activate the virtual environment:**

   On Windows (PowerShell):
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

   On Windows (Command Prompt):
   ```cmd
   venv\Scripts\activate.bat
   ```

   On Linux/macOS:
   ```bash
   source venv/bin/activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r mathheart_player/requirements.txt
   ```

   Or if you're in the `mathheart_player` directory:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the Application

#### Option 1: Using the Run Scripts (Easiest)

**Windows (PowerShell):**
```powershell
.\run_mathheart_player.ps1
```

**Linux/macOS:**
```bash
chmod +x run_mathheart_player.sh
./run_mathheart_player.sh
```

The script will automatically create the virtual environment and install dependencies if needed.

#### Option 2: Manual Activation

Make sure your virtual environment is activated, then:

From the project root directory:
```bash
python mathheart_player/main.py
```

Or using the module syntax:
```bash
python -m mathheart_player.main
```

**Note:** On Windows, use `.\venv\Scripts\python.exe` if the virtual environment is not activated in your current shell.

### First Run

1. Click "Browse..." or use File → Open (Ctrl+O) to select an audio file
2. The application will automatically analyze the audio (first time may take a moment)
3. Analysis results are cached for instant loading on subsequent runs
4. Select a visualization effect (H8sync, H9, H10, or Auto-select)
5. Click "Play" to start playback and see the 3D heart visualization

### Controls

- **Play/Pause:** Toggle playback
- **Stop:** Stop playback and reset to beginning
- **Seek Bar:** Drag to jump to any position in the audio
- **Volume:** Adjust playback volume
- **Effect Selector:** Choose visualization effect or use Auto-select

## Architecture

- **Audio Playback:** pygame.mixer
- **GUI:** PyQt6
- **Visualization:** Matplotlib with Qt5Agg backend
- **Audio Analysis:** librosa with hybrid approach (pre-analyze + streaming)

## Cache

Audio analysis results are cached in:
- **Windows:** `%APPDATA%\MathHeartPlayer\cache\`
- **Linux:** `~/.cache/mathheart_player/`
- **macOS:** `~/Library/Caches/mathheart_player/`

Cached files are automatically invalidated when the source audio file changes.

## Troubleshooting

### PyQt6 Installation Issues

If you encounter issues installing PyQt6, try:

```bash
pip install --upgrade pip
pip install PyQt6
```

### Audio Playback Issues

- Ensure pygame is properly installed: `pip install pygame`
- **For MP3 support:** pydub requires ffmpeg to be installed on your system
  - **Windows:** Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH, or use: `choco install ffmpeg` (if using Chocolatey)
  - **Linux:** `sudo apt install ffmpeg` (Ubuntu/Debian) or `sudo yum install ffmpeg` (RHEL/CentOS)
  - **macOS:** `brew install ffmpeg` (if using Homebrew)
- If MP3 files don't load, try converting to WAV first or install ffmpeg
- MIDI support requires additional setup (mido + fluidsynth)

### Visualization Not Updating

- Check that audio analysis completed successfully (see status bar)
- Try selecting a different effect
- Ensure matplotlib backend is working: `python -c "import matplotlib; print(matplotlib.get_backend())"`

## Development

To contribute or modify the code:

1. Clone the repository
2. Set up virtual environment (see Installation)
3. Install dependencies
4. Make your changes
5. Test with: `python mathheart_player/main.py`

## License

[Your License Here]
