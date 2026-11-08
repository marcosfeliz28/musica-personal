#!/usr/bin/env bash
# Descarga audio de dominio público / licencia libre desde Internet Archive.
# Requiere: pip install internetarchive
# Uso: scripts/archive_descargar.sh <identificador-del-item>
set -euo pipefail
[ $# -ge 1 ] || { echo "Uso: $0 <identificador>"; exit 1; }
DEST="$(dirname "$0")/../music/gratis/archive"
mkdir -p "$DEST"
ia download "$1" --glob='*.mp3' --glob='*.flac' --destdir="$DEST"
