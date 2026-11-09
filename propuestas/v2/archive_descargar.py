#!/usr/bin/env python3
"""Internet Archive -> biblioteca local. PROPUESTA v2, no activa.

Falla cerrado: solo descarga si el ítem declara una licencia libre en `licenseurl`
(Creative Commons o dominio público). Pertenecer a una colección (etree, georgeblood,
78rpm, etc.) NO cuenta como licencia. Para un ítem sin licencia explícita que revisaste
a mano en https://archive.org/details/<id>, usa --forzar-licencia: queda anotado como
FORZADO en ATRIBUCION.txt.

Uso:
  python3 archive_descargar.py <identificador> --dry-run
  python3 archive_descargar.py <identificador> --formato mp3 --max-pistas 5
"""
import argparse
import json
import os
import re
import sys
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import (USER_AGENT, descargar, limpio, nombre_archivo, raiz_repo,  # noqa: E402
                   registrar, una_linea)

METADATA_API = "https://archive.org/metadata/"
DOWNLOAD_BASE = "https://archive.org/download/"
TIMEOUT_SEGUNDOS = 60
MAX_BYTES = 2 * 1024 * 1024 * 1024
PATRONES_LICENCIA = ("creativecommons.org/publicdomain/", "creativecommons.org/licenses/")


def destino():
    return os.path.join(raiz_repo(), "music", "gratis", "archive")


def licencia_declarada(meta):
    """Devuelve (True, texto) si `licenseurl` apunta a Creative Commons o dominio público."""
    lic = meta.get("licenseurl", "")
    if isinstance(lic, list):
        lic = " ".join(str(x) for x in lic)
    lic = str(lic or "").strip()
    if any(p in lic.lower() for p in PATRONES_LICENCIA):
        return True, lic
    return False, lic or "SIN_LICENCIA_EXPLICITA"


def ruta_segura(nombre_remoto):
    """Conserva subcarpetas del ítem saneadas, descarta '..' y mantiene la extensión del archivo."""
    partes = [p for p in nombre_remoto.replace("\\", "/").split("/") if p not in ("", ".", "..")]
    if not partes:
        return "audio"
    carpetas = [limpio(p, "x") for p in partes[:-1]]
    return os.path.join(*carpetas, nombre_archivo(partes[-1]))


def seleccionar(archivos, preferido="mp3"):
    """Un solo archivo por pista. Prefiere originales; descarta derivados _vbr/_64kb.
    Agrupa por ruta sin extensión; elige el formato pedido, y si falta, el otro."""
    grupos = {}
    for f in archivos:
        n = f.get("name")
        if not isinstance(n, str) or str(f.get("private", "")).lower() == "true":
            continue
        base, ext = os.path.splitext(n)
        ext = ext.lower().lstrip(".")
        if ext not in ("mp3", "flac"):
            continue
        if re.search(r"(_vbr|_64kb|_128kb)$", base, re.I):
            continue
        grupos.setdefault(base, {}).setdefault(ext, []).append(f)
    orden = ("mp3", "flac") if preferido == "mp3" else ("flac", "mp3")
    elegidos = []
    for base in sorted(grupos):
        for fmt in orden:
            if fmt in grupos[base]:
                cands = grupos[base][fmt]
                cands.sort(key=lambda f: 0 if f.get("source") == "original" else 1)
                elegidos.append(cands[0])
                break
    return elegidos


def main():
    p = argparse.ArgumentParser(description="Descarga un ítem de Internet Archive con licencia libre declarada.")
    p.add_argument("identificador")
    p.add_argument("--formato", choices=["mp3", "flac"], default="mp3")
    p.add_argument("--max-pistas", type=int, default=0, help="0 = todas")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--forzar-licencia", action="store_true",
                   help="Descargar sin licenseurl libre, tras revisar los derechos a mano (queda anotado)")
    a = p.parse_args()

    item = a.identificador.strip()
    req = urllib.request.Request(METADATA_API + urllib.parse.quote(item), headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT_SEGUNDOS) as r:
            datos = json.load(r)
    except Exception as e:
        sys.exit(f"Error consultando metadatos de '{item}': {e}")
    meta = datos.get("metadata") or {}
    if not meta:
        sys.exit(f"No se encontró el ítem '{item}'.")

    if str(meta.get("access-restricted-item", "")).lower() == "true":
        sys.exit(f"Cancelado: '{item}' es de acceso restringido en Internet Archive (requiere cuenta o permiso); "
                 "sus archivos no se pueden descargar de forma pública.")
    libre, lic = licencia_declarada(meta)
    if not libre and not a.forzar_licencia:
        sys.exit(f"Cancelado: '{item}' no declara licencia libre (detectado: '{lic}'). "
                 f"Revisa https://archive.org/details/{item}; si confirmas los derechos, usa --forzar-licencia.")
    estado = lic if libre else f"FORZADO por el usuario ({lic})"

    archivos = seleccionar(datos.get("files", []), a.formato)
    if a.max_pistas > 0:
        archivos = archivos[:a.max_pistas]
    if not archivos:
        sys.exit("El ítem no tiene archivos MP3 ni FLAC utilizables.")

    creador = meta.get("creator", "")
    if isinstance(creador, list):
        creador = ", ".join(str(x) for x in creador)
    titulo = meta.get("title", item)
    if isinstance(titulo, list):
        titulo = " / ".join(str(x) for x in titulo)
    creador, titulo = una_linea(creador), una_linea(titulo, item)

    base = destino()
    carpeta = os.path.join(base, limpio(item, "item"))
    atrib = os.path.join(base, "ATRIBUCION.txt")

    for f in archivos:
        nombre = f["name"]
        linea = f"{creador} - {titulo} ({una_linea(nombre)}) | {una_linea(estado)} | https://archive.org/details/{item}"
        if a.dry_run:
            print("[dry-run]", linea)
            continue
        final = os.path.join(carpeta, ruta_segura(nombre))
        os.makedirs(os.path.dirname(final), exist_ok=True)
        if os.path.exists(final):
            registrar(atrib, linea)
            continue
        print("Descargando:", nombre)
        try:
            descargar(DOWNLOAD_BASE + urllib.parse.quote(item) + "/" + urllib.parse.quote(nombre),
                      final, TIMEOUT_SEGUNDOS, MAX_BYTES)
        except Exception as e:
            print("  Error, se omite:", e)
            continue
        registrar(atrib, linea)


if __name__ == "__main__":
    main()
