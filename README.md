# Música personal

Sistema propio para escuchar música sin suscripciones mensuales: biblioteca en tu equipo, música con licencia libre y acceso desde el celular.

**Estado (2026-11-09):** en diseño y preparación. La fase 1 (núcleo mínimo) aún no se ha ejecutado en el equipo del propietario. Lo que está probado y lo que no está en [`docs/prueba-fase1-linux.md`](docs/prueba-fase1-linux.md). Todo vive en la rama `spec-diseno-ampliacion`.

## Qué es
- **Servidor:** [Navidrome](https://www.navidrome.org) (código abierto). Lee la biblioteca y la organiza por artistas y álbumes. Listas, buscador, favoritos y aleatorio funcionaron en una prueba con la API; el historial es un contador de reproducciones.
- **Acceso remoto:** [Tailscale](https://tailscale.com), sin abrir puertos del router. Plan personal **[verificar]** límites vigentes.
- **Despliegue (modo C):** la PC es el servidor principal y un servidor en la nube (Oracle Always Free, opcional) es el respaldo. Una sola base activa a la vez. Ver [`docs/despliegue-pc-y-nube.md`](docs/despliegue-pc-y-nube.md).
- **Música:** solo con licencia libre, dominio público o comprada sin DRM. **Fuentes piratas: fuera de alcance.**

## Por dónde empezar
1. Lee [`docs/lista-dia-laptop.md`](docs/lista-dia-laptop.md) (comprobaciones previas).
2. Sigue [`docs/guia-fase1-windows.md`](docs/guia-fase1-windows.md) paso a paso (PowerShell).
3. Celular: [`docs/iphone.md`](docs/iphone.md) y [`docs/apps-celular.md`](docs/apps-celular.md).

> **Aviso:** el `docker-compose.yml` de la raíz es la versión anterior: usa `latest` y publica `4533` en toda la red local. La fase 1 lo reemplaza por [`propuestas/v2/docker-compose.yml`](propuestas/v2/docker-compose.yml) (versión fija, solo `127.0.0.1`). No lo uses tal cual para acceso remoto.

## De dónde sale la música
| Fuente | Estado |
|---|---|
| Archivos propios o comprados sin DRM, copiados a mano a `music/local/` | Permitido |
| Internet Archive | Con [`propuestas/v2/archive_descargar.py`](propuestas/v2/archive_descargar.py): solo si el item declara licencia Creative Commons o dominio público. Probado con una descarga real en Linux. |
| Jamendo | **Descarga automática bloqueada** hasta aclarar con Jamendo (sus términos restringen guardar contenido). Streaming o descarga manual. |
| Free Music Archive | **Solo manual**: sus términos prohíben solicitudes automáticas. |
| Musopen, ccMixter | Sin automatizar hasta leer sus términos. |
| Radios por internet | Se pueden agregar a Navidrome; solo escuchar, no grabar. |

Los scripts de `scripts/` son las **versiones anteriores**; las corregidas están en `propuestas/v2/` y no se activan sin aprobación. Revisa siempre la licencia de cada pista.

## Documentos
| Documento | Para qué |
|---|---|
| [`docs/spec-diseno.md`](docs/spec-diseno.md) | Diseño y decisiones |
| [`docs/plan-implementacion.md`](docs/plan-implementacion.md) | Fases |
| [`docs/consolidacion-auditoria.md`](docs/consolidacion-auditoria.md) | Resumen de las auditorías de ChatGPT, Gemini y Claude |
| [`docs/despliegue-pc-y-nube.md`](docs/despliegue-pc-y-nube.md) | Modo C y relevo entre PC y nube |
| [`docs/piloto-mopidy.md`](docs/piloto-mopidy.md) | Resultado del piloto de Mopidy |
| [`docs/PLAN-COMPLETO.md`](docs/PLAN-COMPLETO.md) | Documento histórico anterior |

## Estructura
```
docker-compose.yml     compose anterior (se reemplaza en la fase 1)
.env.example           configuración (copia a .env; .env no se sube)
music/local/           tu biblioteca (no se sube a GitHub)
music/gratis/          descargas con licencia libre (no se sube a GitHub)
data/                  base de datos de Navidrome (no se sube a GitHub)
scripts/               descargadores anteriores
propuestas/            versiones nuevas, piloto y pista de prueba (no activas)
docs/                  diseño, plan, guías y auditorías
```

> Este repo es **público**: no subas música, claves, `.env` ni direcciones de Tailscale. `.gitignore` excluye `music/`, `data/` y `.env`.
