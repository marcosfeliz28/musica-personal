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
import shutil
import sys
import urllib.parse
import urllib.request

METADATA_API = "https://archive.org/metadata/"
DOWNLOAD_BASE = "https://archive.org/download/"
RAIZ_REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DESTINO = os.path.join(RAIZ_REPO, "music", "gratis", "archive")
TIMEOUT_SEGUNDOS = 60
MAX_BYTES = 2 * 1024 * 1024 * 1024
PATRONES_LICENCIA = ("creativecommons.org/publicdomain/", "creativecommons.org/licenses/")
RESERVADOS_WIN = {"CON", "PRN", "AUX", "NUL",
                  *(f"COM{i}" for i in range(1, 10)), *(f"LPT{i}" for i in range(1, 10))}


def limpio(texto, por_defecto="item"):
    t = re.sub(r'[\\/:*?"<>|\x00-\x1f]', "_", texto or "").strip().strip(".").strip()[:80].strip().strip(".")
    if not t:
        return por_defecto
    return f"_{t}_" if t.upper() in RESERVADOS_WIN else t


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
    """Conserva subcarpetas del ítem, saneando cada parte y descartando '..'."""
    partes = [limpio(p, "x") for p in nombre_remoto.replace("\\", "/").split("/") if p not in ("", ".", "..")]
    return os.path.join(*partes) if partes else "audio"


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


def registrar(ruta, linea):
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    previas = set()
    if os.path.isfile(ruta):
        with open(ruta, "r", encoding="utf-8") as f:
            previas = {x.rstrip("\r\n") for x in f}
    if linea not in previas:
        with open(ruta, "a", encoding="utf-8") as f:
            f.write(linea + "\n")


def parece_audio(ruta):
    with open(ruta, "rb") as f:
        c = f.read(4)
    return c[:3] == b"ID3" or c == b"fLaC" or (len(c) >= 2 and c[0] == 0xFF and (c[1] & 0xE0) == 0xE0)


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
    req = urllib.request.Request(METADATA_API + urllib.parse.quote(item), headers={"User-Agent": "musica-personal/2.0"})
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

    creador = meta.get("creator", "desconocido")
    if isinstance(creador, list):
        creador = ", ".join(str(x) for x in creador)
    titulo = meta.get("title", item)
    if isinstance(titulo, list):
        titulo = " / ".join(str(x) for x in titulo)
    carpeta = os.path.join(DESTINO, limpio(item))
    atrib = os.path.join(DESTINO, "ATRIBUCION.txt")

    for f in archivos:
        nombre = f["name"]
        linea = f"{creador} - {titulo} ({nombre}) | {estado} | https://archive.org/details/{item}"
        if a.dry_run:
            print("[dry-run]", linea)
            continue
        final = os.path.join(carpeta, ruta_segura(nombre))
        os.makedirs(os.path.dirname(final), exist_ok=True)
        if os.path.exists(final):
            registrar(atrib, linea)
            continue
        parcial = final + ".part"
        print("Descargando:", nombre)
        try:
            rq = urllib.request.Request(DOWNLOAD_BASE + urllib.parse.quote(item) + "/" + urllib.parse.quote(nombre),
                                        headers={"User-Agent": "musica-personal/2.0"})
            with urllib.request.urlopen(rq, timeout=TIMEOUT_SEGUNDOS) as resp, open(parcial, "wb") as out:
                tam = resp.headers.get("Content-Length")
                if tam and int(tam) > MAX_BYTES:
                    raise RuntimeError("archivo demasiado grande")
                shutil.copyfileobj(resp, out)
            if not parece_audio(parcial):
                raise RuntimeError("el archivo recibido no parece audio")
            os.replace(parcial, final)
        except Exception as e:
            print("  Error, se omite:", e)
            if os.path.exists(parcial):
                os.remove(parcial)
            continue
        registrar(atrib, linea)


if __name__ == "__main__":
    main()
