# Prueba de la fase 1 en un contenedor Linux (2026-11-08)

Qué es: ensayo en el entorno en la nube de Claude, con Docker Engine en Linux. **No es Windows, ni Docker Desktop, ni Tailscale, ni un celular.** Sirve para descartar errores del compose y de Navidrome antes de tocar tu PC.
Material: `propuestas/v2/docker-compose.yml` (Navidrome `0.64.2`) y un tono de 440 Hz de 5 segundos generado con ffmpeg, sin derechos de terceros. Todo corrió fuera del repo y se borró después.

## Resultados
| Comprobación | Resultado |
|---|---|
| El compose arranca y publica solo en `127.0.0.1:4533` | OK (`docker port` lo confirma) |
| `/music` contiene `local` y `gratis` (cierra A01 en la práctica) | OK |
| Alta del administrador y `ping` de la API | OK, servidor `0.64.2` |
| Escaneo: la pista aparece por artista y álbum | OK (Artista Prueba / Album Prueba) |
| Aleatorio | OK |
| Buscador (`search3`) | OK |
| Favoritos | OK |
| Listas de reproducción | OK |
| Historial: el contador de reproducciones sube a 1 tras un `scrobble` | OK (es el contador, no un historial completo) |
| Radios por internet (crear y listar) | OK en la API; no se reprodujo ninguna emisora |
| Respaldo y restauración: se paró el contenedor, se empaquetó `data/` y la música, se borró `data/`, se restauró | OK: tras restaurar siguen el usuario, el favorito, la lista y la radio |

## Qué documentación oficial confirmó
- `ND_BACKUP_PATH`, `ND_BACKUP_SCHEDULE` y `ND_BACKUP_COUNT` existen. El respaldo automático **solo guarda la base de datos**, no la música ni la configuración.
- Navidrome incluye scrobbling a Last.fm y ListenBrainz, y soporte de varias bibliotecas.
- `tailscale serve [flags] <destino>`; `--bg` corre en segundo plano; HTTPS es el valor por defecto y el comando guía para activarlo.

## Qué NO queda probado
- Docker Desktop y WSL 2 en Windows, y el arranque tras reiniciar.
- Tailscale: instalación, `tailscale serve` y acceso desde el celular con datos móviles.
- Una app Subsonic real en el celular.
- Reproducir audio de verdad (solo se probó la API).
- Una radio real.
- El respaldo automático `ND_BACKUP_*` (solo se probó el respaldo manual de archivos).
