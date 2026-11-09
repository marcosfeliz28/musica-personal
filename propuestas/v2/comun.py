"""Funciones compartidas por los descargadores. PROPUESTA v2, no activa.

Vive junto a los scripts: si se mueven a scripts/, mover también este archivo.
"""
import hashlib
import os
import re
import sys
import urllib.request

RESERVADOS_WIN = {"CON", "PRN", "AUX", "NUL",
                  *(f"COM{i}" for i in range(1, 10)), *(f"LPT{i}" for i in range(1, 10))}
USER_AGENT = "musica-personal/2.1"
TROZO = 64 * 1024


def raiz_repo():
    """Raíz del repo: variable MUSICA_RAIZ, o la primera carpeta hacia arriba con .git, o con docker-compose.yml y .env.example."""
    env = os.environ.get("MUSICA_RAIZ", "").strip()
    if env:
        return os.path.abspath(env)
    actual = os.path.dirname(os.path.abspath(__file__))
    while True:
        tiene = lambda n: os.path.exists(os.path.join(actual, n))
        if tiene(".git") or (tiene("docker-compose.yml") and tiene(".env.example")):
            return actual
        padre = os.path.dirname(actual)
        if padre == actual:
            sys.exit("No encuentro la raíz del repo (.git, o docker-compose.yml y .env.example). Define MUSICA_RAIZ.")
        actual = padre


def cargar_env(ruta):
    """Lee .env sin pisar variables ya definidas. Admite BOM, 'export ', comillas y comentarios al final."""
    if not os.path.isfile(ruta):
        return
    with open(ruta, "r", encoding="utf-8-sig") as f:
        for linea in f:
            linea = linea.strip()
            if not linea or linea.startswith("#"):
                continue
            if linea.startswith("export "):
                linea = linea[7:].lstrip()
            if "=" not in linea:
                continue
            clave, valor = linea.split("=", 1)
            clave, valor = clave.strip(), valor.strip()
            if valor[:1] in ("'", '"') and valor.count(valor[0]) >= 2:
                valor = valor[1:valor.index(valor[0], 1)]
            else:
                valor = re.split(r"\s+#", valor, maxsplit=1)[0].strip()
            if clave and clave not in os.environ:
                os.environ[clave] = valor


def una_linea(texto, por_defecto="desconocido"):
    """Colapsa saltos de línea y espacios; si queda vacío, devuelve por_defecto."""
    t = " ".join(str(texto if texto is not None else "").split())
    return t or por_defecto


def _protegido(stem):
    """En Windows CON, AUX, NUL, COM1... están reservados aunque lleven extensión."""
    return f"_{stem}" if stem.split(".")[0].upper() in RESERVADOS_WIN else stem


def limpio(texto, por_defecto="desconocido", max_len=80):
    """Nombre seguro para una carpeta o un título (sin extensión)."""
    t = re.sub(r'[\\/:*?"<>|\x00-\x1f]', "_", texto or "").strip().strip(".").strip()
    t = t[:max_len].strip().strip(".")
    return _protegido(t) if t else por_defecto


def nombre_archivo(nombre, por_defecto="audio", max_total=120):
    """Nombre de archivo seguro que CONSERVA la extensión. Si hay que acortarlo, añade un hash
    corto del nombre original para que dos nombres largos no colisionen."""
    base = os.path.basename((nombre or "").replace("\\", "/"))
    stem, ext = os.path.splitext(base)
    ext = re.sub(r'[^A-Za-z0-9.]', "", ext)[:10]
    limpio_stem = re.sub(r'[\\/:*?"<>|\x00-\x1f]', "_", stem).strip().strip(".").strip()
    if not limpio_stem:
        limpio_stem = por_defecto
    limite = max_total - len(ext)
    if len(limpio_stem) > limite:
        h = hashlib.sha1(base.encode("utf-8", "replace")).hexdigest()[:6]
        limpio_stem = limpio_stem[:limite - 7].rstrip() + "-" + h
    return _protegido(limpio_stem) + ext


def registrar(ruta, linea):
    """Añade una línea a ATRIBUCION.txt sin duplicar. La línea debe ser de una sola línea."""
    linea = una_linea(linea, "")
    if not linea:
        return
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    previas = set()
    if os.path.isfile(ruta):
        with open(ruta, "r", encoding="utf-8") as f:
            previas = {x.rstrip("\r\n") for x in f}
    if linea not in previas:
        with open(ruta, "a", encoding="utf-8") as f:
            f.write(linea + "\n")


def parece_audio(ruta):
    """Comprueba la cabecera: ID3, sincronía MP3 o FLAC."""
    with open(ruta, "rb") as f:
        c = f.read(4)
    return c[:3] == b"ID3" or c == b"fLaC" or (len(c) >= 2 and c[0] == 0xFF and (c[1] & 0xE0) == 0xE0)


def descargar(url, final, timeout, max_bytes):
    """Descarga a final+'.part' con tope REAL de bytes, valida la cabecera y renombra.
    El .part se borra siempre que no llegue a renombrarse (error o Ctrl-C)."""
    parcial = final + ".part"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    hecho = False
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp, open(parcial, "wb") as out:
            declarado = resp.headers.get("Content-Length")
            if declarado and declarado.isdigit() and int(declarado) > max_bytes:
                raise RuntimeError("archivo demasiado grande")
            escrito = 0
            while True:
                trozo = resp.read(TROZO)
                if not trozo:
                    break
                escrito += len(trozo)
                if escrito > max_bytes:
                    raise RuntimeError("se superó el tope de tamaño")
                out.write(trozo)
        if not parece_audio(parcial):
            raise RuntimeError("el archivo recibido no parece audio")
        os.replace(parcial, final)
        hecho = True
    finally:
        if not hecho and os.path.exists(parcial):
            os.remove(parcial)
