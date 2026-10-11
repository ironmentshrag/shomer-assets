#!/bin/sh
# Downloads the ivrit-ai Hebrew model mirrored in this repo's release (Hugging Face is blocked in the sandbox).
set -e; M=${1:-/home/claude/stt/ivrit}; [ -f "$M/model.bin" ] && exit 0
mkdir -p "$M"; ID=$(gh api repos/ironmentshrag/shomer-assets/releases/tags/models-ivrit -q '.assets[0].id')
gh api -H "Accept: application/octet-stream" repos/ironmentshrag/shomer-assets/releases/assets/$ID | tar x -C "$M"
pip install -q --break-system-packages faster-whisper >/dev/null 2>&1
