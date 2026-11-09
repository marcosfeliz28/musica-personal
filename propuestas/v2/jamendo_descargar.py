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
import sys
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import (USER_AGENT, cargar_env, descargar, limpio, raiz_repo,  # noqa: E402
                   registrar, una_linea)

API = "https://api.jamendo.com/v3.0/tracks/"
TIMEOUT_SEGUNDOS = 30
MAX_POR_PAGINA = 200  # máximo documentado por Jamendo
MAX_BYTES = 200 * 1024 * 1024


def consultar(params):
    url = API + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=TIMEOUT_SEGUNDOS) as r:
        datos = json.load(r)
    cab = datos.get("headers", {})
    if cab.get("status") != "success":
        raise RuntimeError(f"Jamendo devolvió error ({cab.get('code')}): {cab.get('error_message')}")
    return datos.get("results", [])


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

    raiz = raiz_repo()
    cargar_env(os.path.join(raiz, ".env"))
    cid = os.environ.get("JAMENDO_CLIENT_ID", "").strip()
    if not cid:
        sys.exit("Falta JAMENDO_CLIENT_ID en el entorno o en .env.")
    destino = os.path.join(raiz, "music", "gratis", "jamendo")

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

    atrib = os.path.join(destino, "ATRIBUCION.txt")
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
            tid = una_linea(t.get("id"), "")
            if not tid or tid in vistos:
                continue
            vistos.add(tid)
            lic = una_linea(t.get("license_ccurl"), "")
            url = t.get("audiodownload")
            etiqueta = una_linea(f"{t.get('artist_name', '')} - {t.get('name', '')} (ID {tid}) | {lic or 'SIN LICENCIA'}")
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
            carpeta = os.path.join(destino, limpio(t.get("artist_name"), "Artista_Desconocido"),
                                   limpio(t.get("album_name"), "Singles"))
            os.makedirs(carpeta, exist_ok=True)
            archivo = os.path.join(carpeta, f"{limpio(t.get('name'), 'pista')} [{limpio(tid, 'id')}].mp3")
            linea = f"{etiqueta} | {una_linea(t.get('shareurl'), '')}"
            if os.path.exists(archivo):
                registrar(atrib, linea)
                continue
            print("Descargando:", etiqueta)
            try:
                descargar(url, archivo, TIMEOUT_SEGUNDOS, MAX_BYTES)
            except Exception as e:
                print("  Error, se omite:", e)
                continue
            registrar(atrib, linea)
        if len(pistas) < lote:
            break
    print(f"Pistas procesadas: {procesadas}")


if __name__ == "__main__":
    main()
