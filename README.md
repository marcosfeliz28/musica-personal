# Música personal

Sistema propio para escuchar música sin suscripciones mensuales, con acceso desde el iPhone.

- **Servidor:** [Navidrome](https://www.navidrome.org) (código abierto). Lee tu biblioteca y la organiza por artistas y álbumes.
- **Funciones:** listas de reproducción, buscador, favoritos, aleatorio e historial.
- **Acceso remoto:** [Tailscale](https://tailscale.com) (gratis para uso personal).
- **Música gratuita y legal:** Jamendo e Internet Archive (licencias libres), más radios por internet.

## Inicio rápido

1. Instala Docker en tu computadora (o Raspberry Pi).
2. `cp .env.example .env` y ajusta las rutas.
3. `mkdir -p music/local music/gratis data` y copia tu música a `music/local/` (o apunta `MUSICA_LOCAL` a tu carpeta actual).
4. `docker compose up -d`
5. Abre http://localhost:4533 y crea tu usuario administrador.

## Música gratuita y legal

```bash
# Jamendo: rellena JAMENDO_CLIENT_ID en .env y cárgalo en la terminal
set -a; . ./.env; set +a
python3 scripts/jamendo_descargar.py --genero lofi --cantidad 20

# Internet Archive
pip install internetarchive
bash scripts/archive_descargar.sh <identificador-del-item>
```

Revisa la licencia de cada pista (se anota en `music/gratis/jamendo/ATRIBUCION.txt`).

## iPhone

Mira [docs/iphone.md](docs/iphone.md).

## Estructura

```
docker-compose.yml     servidor Navidrome
.env.example           configuración
music/local/           tu biblioteca (no se sube a GitHub)
music/gratis/          descargas gratuitas y legales (no se sube a GitHub)
data/                  base de datos de Navidrome (no se sube a GitHub)
scripts/               descargadores
docs/                  guías
```

> Este repo es público: no subas música ni claves. `.gitignore` ya excluye `music/`, `data/` y `.env`.
