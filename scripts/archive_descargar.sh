#!/usr/bin/env bash
# Descarga audio de dominio público / licencia libre desde Internet Archive.
# Requiere: pip install internetarchive
# Uso: scripts/archive_descargar.sh <identificador-del-item>
set -euo pipefail
[ $# -ge 1 ] || { echo "Uso: $0 <identificador>"; exit 1; }
DEST="$(dirname "$0")/../music/gratis/archive"
mkdir -p "$DEST"
command -v ia >/dev/null || { echo "No se encuentra 'ia' en el PATH. Instala con: pip install internetarchive (puede quedar en ~/.local/bin; agrégalo al PATH)"; exit 1; }
ia download "$1" --glob='*.mp3' --glob='*.flac' --destdir="$DEST"
