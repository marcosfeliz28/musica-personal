# Spec de diseño: Música personal (ampliación)

Estado: BORRADOR, pendiente de aprobación del usuario.
Fecha: 2026-11-08
Base: este documento amplía lo que el repo ya tiene (`docker-compose.yml`, `scripts/`, `docs/PLAN-COMPLETO.md`). No reemplaza nada.

## 1. Objetivo
Reemplazar las suscripciones mensuales con un sistema propio, gratuito y legal: biblioteca local más catálogos de música libre, accesible desde cualquier lugar y también sin conexión.

## 2. Decisiones del usuario
- Acceso desde cualquier lugar con túnel gratuito (Tailscale; Cloudflare Tunnel como plan B).
- Servidor: la PC que ya tiene, con **Windows**, encendida de forma continua.
- Música: no tiene biblioteca previa; se llena con descargas legales y streaming.
- Alcance: todo incluido, usable en cualquier circunstancia.
- Fuera de alcance: Spotify, YouTube Music y cualquier servicio comercial.

## 3. Qué ya existe en el repo y se conserva
| Pieza | Estado |
|---|---|
| Navidrome en Docker (`docker-compose.yml`) | Se conserva como núcleo. |
| `scripts/jamendo_descargar.py`, `scripts/archive_descargar.sh` | Se conservan; se mejoran en la fase 2. |
| Tailscale + app Subsonic (`docs/iphone.md`) | Se conserva; se generaliza a cualquier celular. |
| Respaldo manual, `.env.example`, `.gitignore` | Se conservan; se automatiza el respaldo en la fase 5. |
| Auditoría con pendientes (A01, A10, R1–R16) | Se hereda como lista de riesgos abiertos. |

## 4. Diferencias con el repo actual y cómo se resuelven
| Tema | Repo actual | Esta spec | Decisión propuesta |
|---|---|---|---|
| Instalación | Docker | Navidrome nativo en Windows | **Mantener Docker** (Docker Desktop en Windows). Ya está escrito y probado en sintaxis. El nativo queda como alternativa. |
| Celular | Solo iPhone | Cualquier celular | Generalizar `docs/iphone.md`; las apps Subsonic cubren Android (p. ej. Symfonium, DSub) **[verificar]**. |
| Streaming de catálogo | No existe (Mopidy figura como "no necesario") | Mopidy con Jamendo e Internet Archive | Nueva fase 3. Se corrige `docs/herramientas.md`. |
| Free Music Archive | Solo mencionada | Descarga incluida | Fase 2, tras revisar sus términos **[verificar]**. |
| Radios por internet | Solo mencionadas | Configuradas en Navidrome | Fase 1, **[verificar]** soporte en la versión instalada. |
| Buscador unificado y página de inicio | No existe | Web propia | Nueva fase 4. |
| Jellyfin | Alternativa | Pestaña opcional | Fase 5, opcional. |
| Sistema operativo | Sin especificar (R16) | Windows | Cierra R16. |

## 5. Arquitectura
| Capa | Herramienta | Función |
|---|---|---|
| Biblioteca y reproductor | Navidrome (Docker) | Listas, favoritos, aleatorio, historial parcial, artistas/álbumes. |
| Descargas legales | Scripts del repo + tarea programada de Windows | Jamendo, Internet Archive y Free Music Archive hacia `music/gratis/`. |
| Streaming de catálogo | Mopidy | Busca y reproduce Jamendo e Internet Archive; "guardar" baja a la biblioteca. |
| Etiquetado | beets | Ordena etiquetas y carátulas (cierra R7). |
| Buscador unificado y página de inicio | Web propia ligera | Consulta Navidrome y los catálogos a la vez. |
| Acceso remoto | Tailscale | Túnel privado sin abrir puertos en el router. |
| Video (opcional) | Jellyfin | Solo como pestaña aparte. |

## 6. Uso en cualquier circunstancia
- Sin internet: apps Subsonic que descargan listas al celular **[verificar]** por app.
- PC apagada: sigue sonando lo descargado; lo demás exige PC encendida con Tailscale.
- Sin suspensión de la PC con corriente; Docker y Tailscale arrancan con Windows **[verificar]**.
- Respaldo periódico de `data/`, `music/local/` y `ATRIBUCION.txt` a un disco externo.

## 7. Seguridad
- Contraseña propia en Navidrome y en la página de inicio.
- Enlazar `4533` a la IP de Tailscale o cerrarlo con firewall (R2).
- El repo es **público**: nunca subir `.env`, claves ni IP de Tailscale (R11).

## 8. Fases
1. **Núcleo:** Navidrome, Tailscale y radios; cerrar A01 y R2 con pruebas reales.
2. **Descargas legales:** filtro de licencia en Jamendo (A10), atribución en Internet Archive, Free Music Archive.
3. **Streaming:** Mopidy con Jamendo e Internet Archive.
4. **Buscador unificado y página de inicio.**
5. **Extras:** beets, Jellyfin opcional, uso sin conexión en el celular y respaldo automático.

## 9. Limitaciones
- Solo música con licencia libre: repertorio de artistas independientes y dominio público.
- Con la PC como servidor, el acceso remoto exige que esté encendida y conectada.
- El historial completo puede requerir scrobbling (Last.fm o ListenBrainz).
- El buscador unificado es desarrollo propio: la parte con más trabajo y mantenimiento.
- Los términos y APIs de Jamendo, Free Music Archive e Internet Archive deben revisarse antes de automatizar.
- No es asesoría legal; manda la licencia de cada pista.

## 10. Pendiente
- Aprobación de esta spec; luego plan de implementación por fases.
- Confirmar con el usuario: Docker en vez de nativo, y la visibilidad del repo (hoy público).
