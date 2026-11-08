#!/usr/bin/env python3
"""Descarga audio de dominio público o licencia libre desde Internet Archive.

Reemplaza a scripts/archive_descargar.sh para funcionar de forma nativa tanto en
Windows (Programador de tareas / PowerShell) como en Linux/macOS, sin depender de Bash.

Mejoras aplicadas (Auditoría G04 / R6 / R15):
- Consulta previamente https://archive.org/metadata/<identificador> y verifica que
  'licenseurl' o 'collection' corresponda a Dominio Público, Creative Commons o
  Live Music Archive ('etree') antes de descargar (salvo que se pase --forzar-licencia).
- Evita descargar por duplicado el archivo .flac y su derivado .mp3 para una misma
  pista: prioriza los archivos originales (.flac o .mp3) y, si elige .flac para una
  pista base, omite el derivado .mp3 equivalente.
- Registra automáticamente el autor, título, identificador, licencia y enlace en
  music/gratis/archive/ATRIBUCION.txt sin duplicar líneas.
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
RAIZ_REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DESTINO = os.path.join(RAIZ_REPO, "music", "gratis", "archive")
TIMEOUT_SEGUNDOS = 60

LICENCIAS_PERMITIDAS = (
    "creativecommons.org/publicdomain/",
    "creativecommons.org/licenses/",
    "publicdomain",
)
COLECCIONES_AUTORIZADAS = {"etree", "georgeblood", "freemusicarchive", "78rpm"}


def limpio(texto, por_defecto="item"):
    t = re.sub(r'[\\/:*?"<>|\x00-\x1f]', "_", texto or "").strip().strip(".").strip()
    return t[:80] or por_defecto


def es_licencia_libre(meta):
    """Comprueba si los metadatos del ítem declaran una licencia CC, Dominio Público o colección autorizada."""
    licencia = str(meta.get("licenseurl", "") or meta.get(" licenseurl", "") or "").lower()
    rights = str(meta.get("rights", "") or "").lower()
    colecciones = meta.get("collection", [])
    if isinstance(colecciones, str):
        colecciones = [colecciones]
    colecciones_set = {c.lower() for c in colecciones}

    if any(pat in licencia for pat in LICENCIAS_PERMITIDAS):
        return True, licencia
    if "public domain" in rights or "creative commons" in rights or "cc0" in rights:
        return True, rights
    interseccion = colecciones_set.intersection(COLECCIONES_AUTORIZADAS)
    if interseccion:
        return True, f"coleccion:{','.join(sorted(interseccion))}"
    return False, licencia or rights or "SIN_LICENCIA_EXPLICITA"


def seleccionar_archivos_audio(archivos, preferir_formato="flac"):
    """Selecciona un único archivo de audio por pista para no duplicar .flac y .mp3 derivados."""
    candidatos = [
        f for f in archivos
        if isinstance(f.get("name"), str)
        and f["name"].lower().endswith((".flac", ".mp3"))
        and not f["name"].lower().endswith("_vbr.mp3")
    ]
    # Agrupar por nombre base (sin extensión)
    por_base = {}
    for f in candidatos:
        base, ext = os.path.splitext(f["name"])
        ext = ext.lower().lstrip(".")
        por_base.setdefault(base, {})[ext] = f

    seleccionados = []
    orden = ("flac", "mp3") if preferir_formato == "flac" else ("mp3", "flac")
    for base in sorted(por_base.keys()):
        disponibles = por_base[base]
        for fmt in orden:
            if fmt in disponibles:
                seleccionados.append(disponibles[fmt])
                break
    return seleccionados


def registrar_atribucion(ruta_atribucion, linea):
    os.makedirs(os.path.dirname(ruta_atribucion), exist_ok=True)
    existentes = set()
    if os.path.isfile(ruta_atribucion):
        with open(ruta_atribucion, "r", encoding="utf-8") as f:
            existentes = {l.rstrip("\r\n") for l in f}
    if linea not in existentes:
        with open(ruta_atribucion, "a", encoding="utf-8") as f:
            f.write(linea + "\n")


def main():
    p = argparse.ArgumentParser(description="Descarga un ítem de audio libre desde Internet Archive verificando su licencia.")
    p.add_argument("identificador", help="Identificador del ítem en archive.org")
    p.add_argument("--formato", choices=["flac", "mp3"], default="mp3", help="Formato preferido cuando existen ambos (por defecto: mp3)")
    p.add_argument("--max-pistas", type=int, default=0, help="Límite opcional de pistas a descargar del ítem (0 = todas)")
    p.add_argument("--forzar-licencia", action="store_true", help="Descargar aunque el ítem no declare licenseurl estándar (bajo responsabilidad del usuario)")
    a = p.parse_args()

    item_id = a.identificador.strip()
    url_meta = METADATA_API + urllib.parse.quote(item_id)
    req = urllib.request.Request(url_meta, headers={"User-Agent": "musica-personal/1.1"})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT_SEGUNDOS) as r:
            datos = json.load(r)
    except Exception as e:
        sys.exit(f"Error al consultar metadatos de '{item_id}' en Internet Archive: {e}")

    meta = datos.get("metadata", {})
    if not meta:
        sys.exit(f"No se encontró el ítem '{item_id}' en Internet Archive.")

    permitido, detalle_licencia = es_licencia_libre(meta)
    if not permitido and not a.forzar_licencia:
        sys.exit(
            f"Descarga cancelada por seguridad legal: el ítem '{item_id}' no declara una licencia libre reconocida "
            f"(detectado: '{detalle_licencia}'). Verifica https://archive.org/details/{item_id} antes de usar --forzar-licencia."
        )

    archivos = seleccionar_archivos_audio(datos.get("files", []), preferir_formato=a.formato)
    if not archivos:
        sys.exit(f"El ítem '{item_id}' no contiene archivos .mp3 ni .flac descargables.")

    if a.max_pistas > 0:
        archivos = archivos[: a.max_pistas]

    carpeta_item = os.path.join(DESTINO, limpio(item_id))
    os.makedirs(carpeta_item, exist_ok=True)
    ruta_atribucion = os.path.join(DESTINO, "ATRIBUCION.txt")

    creador = meta.get("creator", "Autor desconocido")
    if isinstance(creador, list):
        creador = ", ".join(str(x) for x in creador)
    titulo_item = meta.get("title", item_id)
    url_item = f"https://archive.org/details/{item_id}"

    for f in archivos:
        nombre_remoto = f["name"]
        nombre_local = limpio(os.path.basename(nombre_remoto))
        ruta_final = os.path.join(carpeta_item, nombre_local)
        parcial = ruta_final + ".part"

        linea_atrib = f"{creador} - {titulo_item} ({nombre_local}) | {detalle_licencia} | {url_item}"
        if os.path.exists(ruta_final):
            registrar_atribucion(ruta_atribucion, linea_atrib)
            continue

        url_descarga = DOWNLOAD_BASE + urllib.parse.quote(item_id) + "/" + urllib.parse.quote(nombre_remoto)
        print(f"Descargando [{a.formato.upper()}]: {nombre_remoto}")
        try:
            req_dl = urllib.request.Request(url_descarga, headers={"User-Agent": "musica-personal/1.1"})
            with urllib.request.urlopen(req_dl, timeout=TIMEOUT_SEGUNDOS) as resp, open(parcial, "wb") as out:
                shutil.copyfileobj(resp, out)
            os.replace(parcial, ruta_final)
        except Exception as e:
            print("  Error descargando archivo, se omite:", e)
            if os.path.exists(parcial):
                os.remove(parcial)
            continue

        registrar_atribucion(ruta_atribucion, linea_atrib)


if __name__ == "__main__":
    main()