#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

PYTHON_BIN="$PROJECT_ROOT/.venv/bin/python"
AUDIO_FILE="$PROJECT_ROOT/inputs/Trend-Music-Music-Music-x4.mp3"
FEATURES_FILE="${AUDIO_FILE%.mp3}_features.json"
SYNCED_VIDEO="$PROJECT_ROOT/outputs/i3_TwoHearts_video.mp4"
FINAL_OUTPUT="$PROJECT_ROOT/outputs/i3-TwoHearts.mp4"

MPL_DIR="$PROJECT_ROOT/tmp/mplconfig"
CACHE_DIR="$PROJECT_ROOT/tmp/cache"

mkdir -p "$PROJECT_ROOT/outputs" "$MPL_DIR" "$CACHE_DIR"

export MPLBACKEND=Agg
export MPLCONFIGDIR="$MPL_DIR"
export XDG_CACHE_HOME="$CACHE_DIR"

if [[ ! -x "$PYTHON_BIN" ]]; then
  echo "[ERROR] Virtual environment python not found at $PYTHON_BIN" >&2
  exit 1
fi

if ! command -v ffmpeg >/dev/null 2>&1; then
  echo "[ERROR] ffmpeg is required but not found in PATH." >&2
  exit 1
fi

echo "============================================================"
echo "I3 Two Hearts Builder"
echo "Audio: $AUDIO_FILE"
echo "Output: $FINAL_OUTPUT"
echo "============================================================"

if [[ -f "$FEATURES_FILE" ]]; then
  echo "[1/3] Audio features already exist at $FEATURES_FILE (skipping analysis)."
else
  echo "[1/3] Analyzing audio to create feature file ..."
  "$PYTHON_BIN" "$PROJECT_ROOT/analyze_audio.py" "$AUDIO_FILE" -o "$FEATURES_FILE"
fi

echo "[2/3] Rendering beat-synced video with heart_animation.py (effect I3) ..."
"$PYTHON_BIN" "$PROJECT_ROOT/heart_animation.py" \
  --effect I3 \
  --resolution 4k \
  --density lower \
  --bitrate 20000 \
  --audio-features "$FEATURES_FILE" \
  --output "$SYNCED_VIDEO"

echo "[3/3] Combining synced video with original audio via ffmpeg ..."
ffmpeg -y \
  -i "$SYNCED_VIDEO" \
  -i "$AUDIO_FILE" \
  -c:v copy \
  -c:a aac \
  -b:a 192k \
  -shortest \
  "$FINAL_OUTPUT"

echo "============================================================"
echo "Completed! Final video with audio: $FINAL_OUTPUT"
echo "============================================================"

