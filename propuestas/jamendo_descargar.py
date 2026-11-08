#!/usr/bin/env python3
"""Descarga música gratuita y legal de Jamendo (licencias Creative Commons).

Uso:
  python3 scripts/jamendo_descargar.py --buscar "jazz" --cantidad 10
  python3 scripts/jamendo_descargar.py --genero lofi --cantidad 20
  python3 scripts/jamendo_descargar.py --genero rock --cantidad 10 --solo-comercial --permitir-derivadas

Mejoras aplicadas (Auditoría G05 / A02 / A10):
- Carga automática de JAMENDO_CLIENT_ID desde .env si no está en el entorno.
- Sanitización completa para Windows (incluye barra invertida '\\', caracteres de control y nombres reservados CON/PRN/AUX/NUL/COM/LPT).
- Uso de 'boost=popularity_total' en búsquedas para no perder la relevancia en la API v3.0 de Jamendo.
- Soporte para singles ('type=single+albumtrack') con carpeta 'Singles' cuando no hay álbum.
- Filtro explícito de licencias Creative Commons (--solo-comercial, --permitir-derivadas, --compartir-igual) e 'include=licenses'.
- Timeout de red (30 s) y verificación de duplicados en ATRIBUCION.txt.
"""
import argparse
import json
import os
import re
import shutil
import sys
import urllib.parse
import urllib.request

API = "https://api.jamendo.com/v3.0/tracks/"
RAIZ_REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DESTINO = os.path.join(RAIZ_REPO, "music", "gratis", "jamendo")
TIMEOUT_SEGUNDOS = 30

NOMBRES_RESERVADOS_WIN = {
    "CON", "PRN", "AUX", "NUL",
    *(f"COM{i}" for i in range(1, 10)),
    *(f"LPT{i}" for i in range(1, 10)),
}


def cargar_env(ruta_env):
    """Carga variables clave=valor desde .env si no están definidas en os.environ."""
    if not os.path.isfile(ruta_env):
        return
    with open(ruta_env, "r", encoding="utf-8") as f:
        for linea in f:
            linea = linea.strip()
            if not linea or linea.startswith("#") or "=" not in linea:
                continue
            clave, valor = linea.split("=", 1)
            clave = clave.strip()
            valor = valor.strip().strip('"').strip("'")
            if clave and clave not in os.environ:
                os.environ[clave] = valor


def limpio(texto, por_defecto="desconocido"):
    """Limpia un nombre para que sea seguro en sistemas de archivos Windows y POSIX."""
    t = re.sub(r'[\\/:*?"<>|\x00-\x1f]', "_", texto or "").strip().strip(".").strip()
    t = t[:80].strip().strip(".")
    if not t:
        return por_defecto
    if t.upper() in NOMBRES_RESERVADOS_WIN:
        t = f"_{t}_"
    return t


def registrar_atribucion(ruta_atribucion, linea):
    """Agrega una línea a ATRIBUCION.txt evitando duplicados exactos."""
    os.makedirs(os.path.dirname(ruta_atribucion), exist_ok=True)
    existentes = set()
    if os.path.isfile(ruta_atribucion):
        with open(ruta_atribucion, "r", encoding="utf-8") as f:
            existentes = {l.rstrip("\r\n") for l in f}
    if linea not in existentes:
        with open(ruta_atribucion, "a", encoding="utf-8") as f:
            f.write(linea + "\n")


def descargar_archivo(url, destino_final):
    """Descarga con timeout hacia un archivo temporal .part y renombra al finalizar."""
    parcial = destino_final + ".part"
    req = urllib.request.Request(url, headers={"User-Agent": "musica-personal/1.1"})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT_SEGUNDOS) as resp, open(parcial, "wb") as out:
            shutil.copyfileobj(resp, out)
        os.replace(parcial, destino_final)
    except Exception:
        if os.path.exists(parcial):
            os.remove(parcial)
        raise


def main():
    p = argparse.ArgumentParser(description="Descarga pistas con licencia Creative Commons desde Jamendo API v3.0.")
    p.add_argument("--buscar", default="", help="Texto libre a buscar (artista, pista, etiqueta)")
    p.add_argument("--genero", default="", help="Etiqueta o género musical (ej. rock, jazz, lofi)")
    p.add_argument("--cantidad", type=int, default=10, help="Cantidad máxima de pistas a consultar (1-200)")
    p.add_argument("--solo-comercial", action="store_true", help="Excluye licencias No Comerciales (filtra ccnc=false)")
    p.add_argument("--permitir-derivadas", action="store_true", help="Excluye licencias Sin Obra Derivada (filtra ccnd=false)")
    p.add_argument("--compartir-igual", action="store_true", help="Exige licencias ShareAlike (filtra ccsa=true)")
    a = p.parse_args()

    cargar_env(os.path.join(RAIZ_REPO, ".env"))
    cid = os.environ.get("JAMENDO_CLIENT_ID", "").strip()
    if not cid:
        sys.exit("Falta JAMENDO_CLIENT_ID. Defínelo en tu archivo .env o variable de entorno (clave gratuita en devportal.jamendo.com).")

    limite = max(1, min(200, a.cantidad))
    q = {
        "client_id": cid,
        "format": "json",
        "limit": limite,
        "audiodownload_allowed": "true",
        "audiodlformat": "mp32",
        "type": "single albumtrack",
        "include": "licenses",
    }

    if a.buscar:
        q["search"] = a.buscar
    if a.genero:
        q["tags"] = a.genero

    # Si hay búsqueda o género, usar boost para no destruir la relevancia (documentación Jamendo v3.0)
    if a.buscar or a.genero:
        q["boost"] = "popularity_total"
    else:
        q["order"] = "popularity_total"

    if a.solo_comercial:
        q["ccnc"] = "false"
    if a.permitir_derivadas:
        q["ccnd"] = "false"
    if a.compartir_igual:
        q["ccsa"] = "true"

    url_consulta = API + "?" + urllib.parse.urlencode(q)
    req = urllib.request.Request(url_consulta, headers={"User-Agent": "musica-personal/1.1"})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT_SEGUNDOS) as r:
            datos = json.load(r)
    except Exception as e:
        sys.exit(f"Error consultando la API de Jamendo: {e}")

    cabecera = datos.get("headers", {})
    if cabecera.get("status") != "success":
        sys.exit(f"La API de Jamendo devolvió un error ({cabecera.get('code')}): {cabecera.get('error_message')}")

    pistas = datos.get("results", [])
    ruta_atribucion = os.path.join(DESTINO, "ATRIBUCION.txt")

    for t in pistas:
        if not t.get("audiodownload_allowed") or not t.get("audiodownload"):
            continue

        artista = limpio(t.get("artist_name"), "Artista_Desconocido")
        album = limpio(t.get("album_name"), "Singles")
        nombre_pista = limpio(t.get("name"), f"pista_{t.get('id', '0')}")
        track_id = str(t.get("id", "")).strip()

        carpeta = os.path.join(DESTINO, artista, album)
        os.makedirs(carpeta, exist_ok=True)
        nombre_archivo = f"{nombre_pista} [{track_id}].mp3" if track_id else f"{nombre_pista}.mp3"
        archivo = os.path.join(carpeta, nombre_archivo)

        licencia_url = t.get("license_ccurl", "")
        share_url = t.get("shareurl", "")
        linea_atrib = f"{t.get('artist_name', '')} - {t.get('name', '')} (ID: {track_id}) | {licencia_url} | {share_url}"

        if os.path.exists(archivo):
            registrar_atribucion(ruta_atribucion, linea_atrib)
            continue

        print("Descargando:", t.get("artist_name"), "-", t.get("name"))
        try:
            descargar_archivo(t["audiodownload"], archivo)
        except Exception as e:
            print("  Error, se omite:", e)
            continue

        registrar_atribucion(ruta_atribucion, linea_atrib)


if __name__ == "__main__":
    main()