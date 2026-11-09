# Herramientas de código abierto consideradas

Actualizado el 2026-11-09 tras las auditorías y los pilotos. Lo marcado "probado" se ejecutó en un contenedor Linux, no en Windows.

| Herramienta | Uso | Decisión |
|---|---|---|
| Navidrome | Servidor de música ligero, API Subsonic | **Elegida.** Probada la versión 0.64.2 (imagen con arm64) |
| Tailscale | Acceso remoto privado (`tailscale serve`; Tailscale SSH en el servidor Linux) | **Elegida.** Sin probar en este proyecto |
| Docker | Ejecutar Navidrome | **Elegida** (Docker Desktop en Windows) |
| Syncthing | Mantener la música igual en PC y nube | Propuesta para el modo C. Sin probar. Sincronizar no es respaldar |
| ListenBrainz (scrobbling de Navidrome) | Historial completo de reproducciones | Opcional; envía hábitos de escucha a un servicio externo |
| beets / MusicBrainz Picard | Etiquetado y carátulas | Fase 5 |
| Mopidy | Búsqueda y exploración de Internet Archive | **Piloto.** Funciona para buscar; no filtra por licencia y reproduce en el servidor. `mopidy-jamendo` sin mantenimiento desde 2021. Ver `docs/piloto-mopidy.md` |
| Jellyfin | Video y música | Alternativa opcional, solo si se quiere video |
| Funkwhale, Ampache | Alternativas a Navidrome | Solo evaluadas |
| Audiobookshelf | Podcasts y audiolibros | Opcional |
| MPD | Reproductor de servidor | No necesario |

Fuentes con licencia libre: ver la tabla del `README.md`. No se usan Spotify, YouTube Music ni fuentes sin licencia.
