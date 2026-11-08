#!/usr/bin/env python3
"""Jamendo (CC) -> biblioteca local. PROPUESTA v2, no activa.

BLOQUEADO POR DEFECTO. Los términos de la API de Jamendo dicen que las aplicaciones
"must not be specifically designed to cache the content nor offering an offline access
to the content". Este script guarda archivos de forma permanente, así que NO se ejecuta
sin --acepto-terminos-api, que significa: "ya consulté a Jamendo y tengo su visto bueno
o asumo el riesgo". Sin esa bandera solo sirve --dry-run (lista pistas, no descarga).

Uso:
  python3 jamendo_descargar.py --genero lofi --cantidad 20 --dry-run
  python3 jamendo_descargar.py --genero lofi --cantidad 20 --acepto-terminos-api

Clave: JAMENDO_CLIENT_ID en el entorno o en .env de la raíz del repo (nunca por línea de comandos).
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
RAIZ_REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DESTINO = os.path.join(RAIZ_REPO, "music", "gratis", "jamendo")
TIMEOUT_SEGUNDOS = 30
MAX_POR_PAGINA = 200  # máximo documentado por Jamendo
MAX_BYTES = 200 * 1024 * 1024
RESERVADOS_WIN = {"CON", "PRN", "AUX", "NUL",
                  *(f"COM{i}" for i in range(1, 10)), *(f"LPT{i}" for i in range(1, 10))}


def cargar_env(ruta):
    if not os.path.isfile(ruta):
        return
    with open(ruta, "r", encoding="utf-8") as f:
        for linea in f:
            linea = linea.strip()
            if not linea or linea.startswith("#") or "=" not in linea:
                continue
            k, v = linea.split("=", 1)
            k = k.strip()
            if k and k not in os.environ:
                os.environ[k] = v.strip().strip('"').strip("'")


def limpio(texto, por_defecto="desconocido"):
    t = re.sub(r'[\\/:*?"<>|\x00-\x1f]', "_", texto or "").strip().strip(".").strip()
    t = t[:80].strip().strip(".")
    if not t:
        return por_defecto
    return f"_{t}_" if t.upper() in RESERVADOS_WIN else t


def parece_mp3(ruta):
    with open(ruta, "rb") as f:
        c = f.read(3)
    return c == b"ID3" or (len(c) >= 2 and c[0] == 0xFF and (c[1] & 0xE0) == 0xE0)


def registrar(ruta, linea):
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    previas = set()
    if os.path.isfile(ruta):
        with open(ruta, "r", encoding="utf-8") as f:
            previas = {x.rstrip("\r\n") for x in f}
    if linea not in previas:
        with open(ruta, "a", encoding="utf-8") as f:
            f.write(linea + "\n")


def consultar(params):
    url = API + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": "musica-personal/2.0"})
    with urllib.request.urlopen(req, timeout=TIMEOUT_SEGUNDOS) as r:
        datos = json.load(r)
    cab = datos.get("headers", {})
    if cab.get("status") != "success":
        raise RuntimeError(f"Jamendo devolvió error ({cab.get('code')}): {cab.get('error_message')}")
    return datos.get("results", [])


def descargar(url, final):
    parcial = final + ".part"
    req = urllib.request.Request(url, headers={"User-Agent": "musica-personal/2.0"})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT_SEGUNDOS) as resp, open(parcial, "wb") as out:
            tam = resp.headers.get("Content-Length")
            if tam and int(tam) > MAX_BYTES:
                raise RuntimeError("archivo demasiado grande")
            shutil.copyfileobj(resp, out)
        if not parece_mp3(parcial):
            raise RuntimeError("el archivo recibido no parece un MP3")
        os.replace(parcial, final)
    except Exception:
        if os.path.exists(parcial):
            os.remove(parcial)
        raise


def main():
    p = argparse.ArgumentParser(description="Pistas CC de Jamendo (bloqueado salvo --dry-run o --acepto-terminos-api).")
    p.add_argument("--buscar", default="")
    p.add_argument("--genero", default="")
    p.add_argument("--cantidad", type=int, default=10, help="Pistas a procesar (mínimo 1)")
    p.add_argument("--solo-comercial", action="store_true", help="Excluye licencias NC (ccnc=false)")
    p.add_argument("--sin-nd", action="store_true", help="Excluye licencias ND (ccnd=false)")
    p.add_argument("--compartir-igual", action="store_true", help="Exige SA (ccsa=true)")
    p.add_argument("--dry-run", action="store_true", help="Lista las pistas y su licencia; no descarga nada")
    p.add_argument("--acepto-terminos-api", action="store_true",
                   help="Confirmo que revisé los términos de la API de Jamendo (ver cabecera)")
    a = p.parse_args()

    if not a.dry_run and not a.acepto_terminos_api:
        sys.exit("Descarga bloqueada: los términos de la API de Jamendo restringen guardar contenido de forma "
                 "permanente. Usa --dry-run, o --acepto-terminos-api si ya lo aclaraste con Jamendo.")

    cargar_env(os.path.join(RAIZ_REPO, ".env"))
    cid = os.environ.get("JAMENDO_CLIENT_ID", "").strip()
    if not cid:
        sys.exit("Falta JAMENDO_CLIENT_ID en el entorno o en .env.")

    total = max(1, a.cantidad)
    base = {"client_id": cid, "format": "json", "audiodownload_allowed": "true",
            "audiodlformat": "mp32", "type": "single albumtrack", "include": "licenses"}
    if a.buscar:
        base["search"] = a.buscar
    if a.genero:
        base["tags"] = a.genero
    base["boost" if (a.buscar or a.genero) else "order"] = "popularity_total"
    if a.solo_comercial:
        base["ccnc"] = "false"
    if a.sin_nd:
        base["ccnd"] = "false"
    if a.compartir_igual:
        base["ccsa"] = "true"

    atrib = os.path.join(DESTINO, "ATRIBUCION.txt")
    vistos, procesadas, offset = set(), 0, 0
    while procesadas < total:
        lote = min(MAX_POR_PAGINA, total - procesadas)
        try:
            pistas = consultar({**base, "limit": lote, "offset": offset})
        except Exception as e:
            sys.exit(f"Error consultando Jamendo: {e}")
        if not pistas:
            break
        offset += len(pistas)
        for t in pistas:
            if procesadas >= total:
                break
            tid = str(t.get("id", "")).strip()
            if not tid or tid in vistos:
                continue
            vistos.add(tid)
            lic = (t.get("license_ccurl") or "").strip()
            url = t.get("audiodownload")
            etiqueta = f"{t.get('artist_name', '')} - {t.get('name', '')} (ID {tid}) | {lic or 'SIN LICENCIA'}"
            if not lic:
                print("[omitida, sin licencia declarada]", etiqueta)
                continue
            if not t.get("audiodownload_allowed") or not url:
                print("[omitida, sin descarga permitida]", etiqueta)
                continue
            procesadas += 1
            if a.dry_run:
                print("[dry-run]", etiqueta)
                continue
            carpeta = os.path.join(DESTINO, limpio(t.get("artist_name"), "Artista_Desconocido"),
                                   limpio(t.get("album_name"), "Singles"))
            os.makedirs(carpeta, exist_ok=True)
            archivo = os.path.join(carpeta, f"{limpio(t.get('name'), 'pista')} [{tid}].mp3")
            linea = f"{etiqueta} | {t.get('shareurl', '')}"
            if os.path.exists(archivo):
                registrar(atrib, linea)
                continue
            print("Descargando:", etiqueta)
            try:
                descargar(url, archivo)
            except Exception as e:
                print("  Error, se omite:", e)
                continue
            registrar(atrib, linea)
        if len(pistas) < lote:
            break
    print(f"Pistas procesadas: {procesadas}")


if __name__ == "__main__":
    main()
