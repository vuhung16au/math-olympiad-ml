#!/usr/bin/env bash
set -euo pipefail

# Absolute paths
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

PYTHON_BIN="$PROJECT_ROOT/.venv/bin/python"
AUDIO_FILE="$PROJECT_ROOT/inputs/WomanInLove.mp3"
FEATURES_FILE="${AUDIO_FILE%.mp3}_features.json"
VISUALISE_OUTPUT="$PROJECT_ROOT/outputs/i2-TwoHearts-WomanInLove_visualise.mp4"
SYNCED_VIDEO="$PROJECT_ROOT/outputs/i2-TwoHearts-WomanInLove_synced.mp4"
FINAL_OUTPUT="$PROJECT_ROOT/outputs/i2-TwoHearts-WomanInLove.mp4"

MPL_DIR="$PROJECT_ROOT/tmp/mplconfig"
CACHE_DIR="$PROJECT_ROOT/tmp/cache"

mkdir -p "$PROJECT_ROOT/outputs" "$MPL_DIR" "$CACHE_DIR"

export MPLBACKEND=Agg
export MPLCONFIGDIR="$MPL_DIR"
export XDG_CACHE_HOME="$CACHE_DIR"

if [[ ! -x "$PYTHON_BIN" ]]; then
  echo "[ERROR] Virtual environment python not found at $PYTHON_BIN" >&2
  echo "Run scripts/setup-env.ps1 or equivalent to set up .venv." >&2
  exit 1
fi

if ! command -v ffmpeg >/dev/null 2>&1; then
  echo "[ERROR] ffmpeg is required but not found in PATH." >&2
  exit 1
fi

echo "============================================================"
echo "I2 Two Hearts WomanInLove Builder (bash)"
echo "Audio: $AUDIO_FILE"
echo "Output: $FINAL_OUTPUT"
echo "============================================================"

echo "[1/4] Visualising audio with visualise_audio.py ..."
"$PYTHON_BIN" "$PROJECT_ROOT/visualise_audio.py" "$AUDIO_FILE" \
  --effect I2-TwoHearts-WomanInLove \
  --resolution 4k \
  --density lower \
  --bitrate 20000 \
  --output "$VISUALISE_OUTPUT" \
  --overwrite

echo "[2/4] Analyzing audio for beat features ..."
"$PYTHON_BIN" "$PROJECT_ROOT/analyze_audio.py" "$AUDIO_FILE" -o "$FEATURES_FILE"

echo "[3/4] Rendering beat-synced video with heart_animation.py ..."
"$PYTHON_BIN" "$PROJECT_ROOT/heart_animation.py" \
  --effect I2-TwoHearts-WomanInLove \
  --resolution 4k \
  --density lower \
  --bitrate 20000 \
  --audio-features "$FEATURES_FILE" \
  --output "$SYNCED_VIDEO"

echo "[4/4] Combining synced video with original audio via ffmpeg ..."
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

