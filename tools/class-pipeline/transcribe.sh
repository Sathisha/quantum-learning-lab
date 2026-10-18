#!/usr/bin/env bash
# Transcribe a class recording (or every new recording in a folder) with Docker.
#   ./transcribe.sh "class material/week-02/lecture.mp4" [--notes] [--cpu] [--rebuild] [-- extra pipeline options]
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
[ $# -ge 1 ] || { echo "Usage: $0 <video file or folder> [--notes] [--cpu] [--rebuild] [-- options]"; exit 1; }

path="$1"; shift
service=transcribe; args=(); rebuild=0
while [ $# -gt 0 ]; do
  case "$1" in
    --cpu) service=transcribe-cpu ;;
    --rebuild) rebuild=1 ;;
    --) shift; args+=("$@"); break ;;
    *) args+=("$1") ;;
  esac
  shift
done

if [ -d "$path" ]; then
  export MEDIA_DIR="$(cd "$path" && pwd)"; target=/data
elif [ -f "$path" ]; then
  export MEDIA_DIR="$(cd "$(dirname "$path")" && pwd)"; target="/data/$(basename "$path")"
else
  echo "Not found: $path"; exit 1
fi

[ "$rebuild" = 1 ] && docker compose -f "$here/docker-compose.yml" build
echo "Processing $path ($service)..."
exec docker compose -f "$here/docker-compose.yml" run --rm "$service" "$target" ${args[@]+"${args[@]}"}
