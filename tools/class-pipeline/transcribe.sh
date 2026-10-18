#!/usr/bin/env bash
# Transcribe a class recording, or every recording in a folder that isn't done yet, with Docker.
#   ./transcribe.sh ["class-material/week-02/lecture.mp4" | folder] [--notes] [--cpu] [--rebuild] [-- extra pipeline options]
# With no path (or an option first), processes everything under the repo's "class-material" folder.
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
if [ $# -ge 1 ] && [ "${1#-}" = "$1" ]; then path="$1"; shift; else path="$here/../../class-material"; fi
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
echo "Processing $MEDIA_DIR${target#/data} ($service)..."
exec docker compose -f "$here/docker-compose.yml" run --rm "$service" "$target" ${args[@]+"${args[@]}"}
