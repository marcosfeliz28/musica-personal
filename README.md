# Música personal

Sistema propio para escuchar música sin suscripciones mensuales, con acceso desde el iPhone.

- **Servidor:** [Navidrome](https://www.navidrome.org) (código abierto). Lee tu biblioteca y la organiza por artistas y álbumes.
- **Funciones:** listas de reproducción, buscador, favoritos y aleatorio (las provee Navidrome y la app; **[verificar]** en tu versión). Historial: parcial, solo contador de reproducciones; el historial completo puede requerir scrobbling (Last.fm / ListenBrainz) **[verificar]**.
- **Acceso remoto:** [Tailscale](https://tailscale.com) (plan personal; **[verificar]** límites y precio vigentes).
- **Música gratuita y legal:** Jamendo e Internet Archive (la licencia varía por pista o item; revísala), más radios por internet (solo mencionadas, no configuradas).

## Inicio rápido

1. Instala Docker en tu computadora (o Raspberry Pi).
2. `cp .env.example .env` y ajusta las rutas.
3. `mkdir -p music/local music/gratis data` y copia tu música a `music/local/` (o apunta `MUSICA_LOCAL` a tu carpeta actual).
4. `docker compose up -d`
5. Abre http://localhost:4533 (si el servidor no tiene pantalla, usa `http://<IP-del-servidor>:4533` desde otro equipo de tu red) y crea tu usuario administrador.
6. Verifica que funciona: `docker compose ps` (navidrome Up) y `docker compose exec navidrome ls /music` (debe listar `local` y `gratis`); luego confirma en la web que el conteo de canciones coincide con tu música.

## Música gratuita y legal

```bash
# Jamendo: rellena JAMENDO_CLIENT_ID en .env y cárgalo en la terminal
set -a; . ./.env; set +a
python3 scripts/jamendo_descargar.py --genero lofi --cantidad 20

# Internet Archive
pip install internetarchive   # el comando `ia` debe quedar en el PATH (a veces ~/.local/bin)
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
