#!/usr/bin/env python3
"""Descarga música gratuita y legal de Jamendo (licencias Creative Commons).

Uso:
  export JAMENDO_CLIENT_ID=tu_clave
  python3 scripts/jamendo_descargar.py --buscar "jazz" --cantidad 10
  python3 scripts/jamendo_descargar.py --genero lofi --cantidad 20

Guarda en music/gratis/jamendo/<Artista>/<Álbum>/ y anota la licencia de cada
pista en ATRIBUCION.txt. Respeta la licencia de cada canción (algunas piden atribución).
"""
import argparse, json, os, re, sys, urllib.parse, urllib.request

API = "https://api.jamendo.com/v3.0/tracks/"
DESTINO = os.path.join(os.path.dirname(__file__), "..", "music", "gratis", "jamendo")


def limpio(texto):
    return re.sub(r'[\\/:*?"<>|]', "_", texto or "desconocido").strip()[:80]


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--buscar", default="")
    p.add_argument("--genero", default="")
    p.add_argument("--cantidad", type=int, default=10)
    a = p.parse_args()
    cid = os.environ.get("JAMENDO_CLIENT_ID")
    if not cid:
        sys.exit("Falta JAMENDO_CLIENT_ID (clave gratuita en devportal.jamendo.com)")
    q = {"client_id": cid, "format": "json", "limit": a.cantidad,
         "audiodownload_allowed": "true", "order": "popularity_total"}
    if a.buscar:
        q["search"] = a.buscar
    if a.genero:
        q["tags"] = a.genero
    with urllib.request.urlopen(API + "?" + urllib.parse.urlencode(q)) as r:
        pistas = json.load(r)["results"]
    for t in pistas:
        carpeta = os.path.join(DESTINO, limpio(t["artist_name"]), limpio(t["album_name"]))
        os.makedirs(carpeta, exist_ok=True)
        archivo = os.path.join(carpeta, limpio(t["name"]) + ".mp3")
        if not os.path.exists(archivo):
            print("Descargando:", t["artist_name"], "-", t["name"])
            urllib.request.urlretrieve(t["audiodownload"], archivo)
        with open(os.path.join(DESTINO, "ATRIBUCION.txt"), "a", encoding="utf-8") as f:
            f.write(f'{t["artist_name"]} - {t["name"]} | {t.get("license_ccurl", "")} | {t.get("shareurl", "")}\n')


if __name__ == "__main__":
    main()
