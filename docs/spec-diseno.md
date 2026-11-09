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
- Alcance: todo incluido. "Cualquier circunstancia" significa: biblioteca accesible mientras servidor y red estén disponibles; sin conexión suenan solo las pistas descargadas en el dispositivo y autorizadas.
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
| Streaming de catálogo | No existe (Mopidy figura como "no necesario") | Mopidy con Jamendo e Internet Archive | Fase 3 como piloto condicionado. Se corrige `docs/herramientas.md`. |
| Free Music Archive | Solo mencionada | Descarga incluida | Solo manual: sus términos prohíben solicitudes automáticas (sección 7(e)). |
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
6. **Ampliación de fuentes legales:** ver sección 8b.

## 8b. Ampliación de fuentes legales (fase 6)
Principio: solo fuentes con licencia libre o compradas sin DRM. No se integran fuentes piratas.
| Fuente | Tipo | Notas |
|---|---|---|
| Live Music Archive (Internet Archive) | Conciertos autorizados | Misma API que Internet Archive; reutiliza el script. |
| Radio Browser | Directorio abierto de radios | Alimenta las emisoras de Navidrome. |
| Emisoras independientes (SomaFM, NTS, KEXP) | Radio | **[verificar]** que sus transmisiones sigan abiertas. |
| Bandcamp | Descarga gratis o compra sin DRM | Descarga manual; los archivos van a `music/local/`. |
| ccMixter | Remixes Creative Commons | **[verificar]** API y licencias por pista. |
| Musopen | Clásica de dominio público | **[verificar]** términos de uso. |
| Internet Archive 78 rpm | Dominio público | Mismo script de Internet Archive. |
| CDs y compras propias | Música propia | Copia con fre:ac o abcde; **[verificar]** la ley de copia privada de tu país. |
| ListenBrainz | Historial completo | Cierra el límite del historial parcial. |
| Picard | Etiquetas y carátulas | Complementa a beets. |
| Funkwhale / Ampache | Alternativas a Navidrome | Solo evaluar; no se instalan por defecto. |
| Audiobookshelf | Podcasts | Opcional; Navidrome los maneja de forma limitada **[verificar]**. |

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

## 11. Decisiones tras las auditorías (2026-11-08)
Ver `docs/consolidacion-auditoria.md`. Resumen:
- Fase 1 reducida: Navidrome con versión fija, `127.0.0.1` más `tailscale serve`, una pista legal de prueba, respaldo y restauración probados.
- Jamendo: descarga automática bloqueada hasta aclarar con Jamendo.
- Free Music Archive: solo manual. Musopen y ccMixter: sin automatización hasta leer sus términos.
- Live Music Archive y Internet Archive: solo con licencia declarada, o forzada tras revisión humana.
- Mopidy y buscador propio: condicionados a un piloto.
- Fuera de alcance, sin excepción: fuentes sin licencia.

## 12. Despliegue en PC y en la nube (2026-11-09)
Requisito del propietario: poder manejarlo desde la nube y desde la PC. Se resuelve con una sola receta de Docker que corre en los dos sitios; ver `docs/despliegue-pc-y-nube.md`. Modos: A solo PC, B solo nube, C ambos con una sola base activa. La nube propuesta es Oracle Always Free, con el riesgo documentado de recuperación por inactividad. Render gratis queda descartado (sistema de archivos efímero) y Fly.io no tiene plan gratuito para cuentas nuevas.
