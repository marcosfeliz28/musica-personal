# Auditoría externa independiente — ChatGPT

**Fecha:** 2026-11-08  
**Auditor:** ChatGPT (GPT-6), revisión documental y de código estática  
**Repositorio:** https://github.com/marcosfeliz28/musica-personal/tree/spec-diseno-ampliacion  
**Rama:** `spec-diseno-ampliacion`  
**Estado:** INFORME PARA REVISIÓN DEL PROPIETARIO. NO AUTORIZA CAMBIOS NI INSTALACIONES.

## Alcance, evidencias y limitaciones

Se leyeron íntegramente `docs/auditoria-externa.md`, `docs/spec-diseno.md`, `docs/plan-implementacion.md`, `docs/PLAN-COMPLETO.md`, `docker-compose.yml`, `scripts/jamendo_descargar.py` y `scripts/archive_descargar.sh`. Adicionalmente se inspeccionaron `.gitignore`, `.env.example`, `README.md` y `docs/iphone.md`. Se contrastaron afirmaciones con documentación primaria enlazada abajo. **No** se ejecutó Docker, no se utilizó clave de Jamendo, no se descargó música, no se probó Tailscale ni se verificó un equipo Windows. Hallazgo en código ≠ explotación comprobada. El reporte no constituye asesoría jurídica.

Enlaces a archivos del commit/rama examinada:
- [Prompt](https://github.com/marcosfeliz28/musica-personal/blob/spec-diseno-ampliacion/docs/auditoria-externa.md)
- [Spec](https://github.com/marcosfeliz28/musica-personal/blob/spec-diseno-ampliacion/docs/spec-diseno.md)
- [Fases](https://github.com/marcosfeliz28/musica-personal/blob/spec-diseno-ampliacion/docs/plan-implementacion.md)
- [Plan anterior](https://github.com/marcosfeliz28/musica-personal/blob/spec-diseno-ampliacion/docs/PLAN-COMPLETO.md)
- [Compose](https://github.com/marcosfeliz28/musica-personal/blob/spec-diseno-ampliacion/docker-compose.yml)
- [Jamendo](https://github.com/marcosfeliz28/musica-personal/blob/spec-diseno-ampliacion/scripts/jamendo_descargar.py)
- [Archive](https://github.com/marcosfeliz28/musica-personal/blob/spec-diseno-ampliacion/scripts/archive_descargar.sh)

## A) Hallazgos: ID | Severidad | Archivo y sección | Hallazgo | Evidencia | Corrección

| ID | Sev. | Archivo y sección | Hallazgo (estado) | Evidencia externa verificable | Corrección propuesta |
|---|---|---|---|---|---|
| H01 | **Alta** | `docker-compose.yml`, `ports`; `docs/spec-diseno.md` §7 | **Confirmado en configuración:** `"4533:4533"` publica en todas las interfaces por defecto. No significa por sí solo que el router abra Internet; sí amplía la superficie en LAN. | [Docker: publicación de puertos](https://docs.docker.com/get-started/docker-concepts/running-containers/publishing-ports/) | Antes de iniciar, cambiar a `127.0.0.1:4533:4533` y publicar de forma privada con Tailscale Serve; comprobar desde LAN ajena a la tailnet que no abre. |
| H02 | **Alta** | `scripts/archive_descargar.sh`, comando `ia download`; `docs/plan-implementacion.md` fase 2 | **Confirmado en código:** descarga todos los MP3/FLAC del identificador sin consultar `licenseurl` ni `rights`, sin bloquear elementos de derechos desconocidos ni generar manifiesto. Que se pueda descargar no autoriza reutilizar. | [Internet Archive: derechos no garantizados](https://archivesupport.zendesk.com/hc/en-us/articles/360014759692-Rights); [metadatos licenseurl/rights](https://internetarchive.readthedocs.io/en/stable/metadata.html) | Modo *fail closed*: inspección previa de metadatos, lista explícita de licencias permitidas y revisión humana de derechos antes de descargar; persistir identificador, URLs, licencia y evidencia. No confiar ciegamente en metadatos declarados por terceros. |
| H03 | **Alta** | `scripts/jamendo_descargar.py`, `main()`; `docs/spec-diseno.md` §§5, 8 | **Confirmado en código + términos:** el programa está destinado a descargar y almacenar pistas permanentemente desde la API. Los términos oficiales de la API restringen aplicaciones específicamente diseñadas para cachear contenido u ofrecer acceso offline. Licencia CC de pista y contrato de API son obligaciones distintas. No se ha obtenido excepción. | [Términos oficiales de API Jamendo, cláusula 3.3](https://devportal.jamendo.com/api_terms_of_use) | **No automatizar Jamendo mediante esta API hasta resolver expresamente la compatibilidad contractual o recibir autorización.** Revisar alternativa legítima: descarga manual permitida por la interfaz y licencia de pista, sin asumir que la API habilita biblioteca offline permanente. |
| H04 | **Alta** | `docs/plan-implementacion.md`, fase 3; `docs/spec-diseno.md` §§4–5 | **Dependencia no verificada:** `mopidy-jamendo` figura como *Unconfirmed* para Mopidy 4 en el catálogo actual; la fase 3 y búsqueda unificada asumen que funcionará. `mopidy-internetarchive` sí figura para Mopidy 4, pero reproducción real local no probada. | [Mopidy Jamendo](https://mopidy.com/ext/jamendo/); [Mopidy Internet Archive](https://mopidy.com/ext/internetarchive/) | Poner la integración Jamendo tras una prueba de concepto con versiones fijas; no prometer streaming ni botón «guardar» antes de prueba técnica y revisión contractual. |
| H05 | **Media** | `scripts/jamendo_descargar.py`, `q`, `for t in pistas` | **Confirmado:** filtra `audiodownload_allowed` pero no valida `license_ccurl`, ni contempla NC/ND/SA según uso. Descargar legalmente no implica autorización para distribuir, comercializar o crear adaptaciones. | [Jamendo tracks API](https://developer.jamendo.com/v3.0/tracks); [Creative Commons licencias](https://creativecommons.org/cc-licenses/) | Si se autoriza la integración, validar la licencia exacta, versión y términos por pista; guardar atribución y restricciones de uso. No excluir automáticamente NC/ND del uso privado: evaluarlo según uso concreto. |
| H06 | **Media** | `scripts/jamendo_descargar.py`, control `os.path.exists(archivo)` + `ATRIBUCION.txt` | **Confirmado:** si el audio ya existe, se omite antes de escribir atribución; si falla la escritura del manifiesto tras descargar, el reintento tampoco repara la información. Colisiones por artista/álbum/título normalizados pueden omitir pistas diferentes. | [Creative Commons: obligaciones de crédito](https://creativecommons.org/chooser/) | Identificar por ID estable de pista, manifiesto estructurado indexado por ID, reconciliar archivos con registro, y usar escritura atómica o reparación al reinicio. |
| H07 | **Media** | `scripts/jamendo_descargar.py`, `urlopen`, `urlretrieve`, `--cantidad` | **Confirmado:** sin timeout explícito, límites de bytes, reintentos controlados, verificación del tipo/contenido o `cantidad > 0`; nombre siempre termina en `.mp3` sin validar el fichero recibido. | [Documentación Python urllib.request](https://docs.python.org/3/library/urllib.request.html) | Timeouts, límites de tamaño, códigos HTTP, validación de MIME/contenido, ID de pista, integridad, paginación y tope de cantidad; manejar fallos del JSON y listas vacías. |
| H08 | **Media** | `docker-compose.yml`, imagen `deluan/navidrome:latest`; plan fase 1 | **Confirmado:** la etiqueta `latest` no fija versión; actualizaciones pueden producir regresiones. | [Docker: referencias de imagen y digest](https://docs.docker.com/reference/cli/docker/image/pull/) | Fijar versión o digest probado y plan de reversión antes de actualizar. |
| H09 | **Media** | `docs/PLAN-COMPLETO.md` §4, §8 y `README.md` | **Confirmado:** comandos `cp`, `mkdir -p`, `set -a`, `python3`, `bash`, `sudo tailscale up`, `tar`, `date +%F` son de shell POSIX y no se pueden presentar como receta universal de Windows PowerShell. | [Microsoft: diferencias y cmdlets PowerShell](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/copy-item) | Dar recetas específicas PowerShell para Windows y dejar Bash/WSL como alternativa explícita. Probar rutas con espacios y unidad externa. |
| H10 | **Media** | `docs/plan-implementacion.md`, fase 1 pasos 3–5 | **Incompatibilidad de diseño:** cambiar el puerto a loopback protege LAN pero rompe el acceso directo por `http://100.x:4533` documentado. Sin configurar `tailscale serve` u otro proxy privado no hay acceso remoto. | [Tailscale Serve: servicio local en tailnet](https://tailscale.com/docs/features/tailscale-serve) | Definir un solo esquema final: loopback + Tailscale Serve HTTPS; actualizar URL de clientes y probar autenticación y conexión. |
| H11 | **Media** | `docs/spec-diseno.md` §8 y `docs/plan-implementacion.md` | **Orden débil:** copias y restauración probada solo en fase 5 después de almacenar música, cuentas y listas. Las fases 3–4 agregan complejidad antes de validar valor y legalidad. | [Navidrome: documentación de configuración](https://www.navidrome.org/docs/usage/configuration/options/) (contexto técnico); evidencia de orden en el plan | Llevar copia básica, restauración, control de licencias y prueba offline mínima a fases 1–2. Mopidy y buscador propio, bajo condición de una PoC satisfactoria. |
| H12 | **Media** | `docs/PLAN-COMPLETO.md` §8 | **Confirmado:** respaldo incluye `data`, `.env` y `music/local`, pero omite `music/gratis` y el archivo de atribución que contiene; restauración extrae `tar` sin validación de origen y no asegura prueba de recuperación. | [GNU tar manual](https://www.gnu.org/software/tar/manual/) | Incluir manifiestos/atribución y música descargada o procedimiento reproducible autorizado; cifrar copia que contiene `.env`, comprobar integridad y restaurar en destino aislado. |
| H13 | **Media** | `docs/spec-diseno.md` §8b, Musopen/78rpm/Live Music Archive | **No verificado para cada obra:** plan trata «clásica» o «78 rpm» como categoría de dominio público; el estatus depende de composición, grabación, jurisdicción y fuente. Musopen advierte expresamente que no garantiza dominio público universal. | [Musopen términos, §9](https://musopen.org/tos/); [Internet Archive derechos](https://archivesupport.zendesk.com/hc/en-us/articles/360014759692-Rights) | Revisión por grabación y jurisdicción; no aceptar colección completa como libre por época, género o etiqueta. |
| H14 | **Media** | `docs/spec-diseno.md` §§5, 8b; `docs/plan-implementacion.md` fase 6 | **No verificado:** ninguna evidencia contractual específica prueba que FMA, ccMixter o Musopen autoricen *scraping* o descargas masivas. FMA permite descargar pistas bajo licencias particulares; ello no prueba autorización para un robot. | [FMA, términos §§3, 7, 11](https://freemusicarchive.org/terms_of_use/); [Musopen términos](https://musopen.org/tos/) | Restringir a descarga manual hasta contar con autorización explícita o API y condiciones vigentes. |
| H15 | **Media** | `docs/spec-diseno.md` §§1, 6, 8b | **Promesa demasiado amplia:** «usable en cualquier circunstancia» es técnicamente falsa para pistas no descargadas, PC apagada, servicio caído, radios offline, cambios de licencias y ausencia de red. | Diseño §§6 y 9 (limitaciones) | Reformular «biblioteca local accesible mientras servidor/red estén disponibles; offline solo pistas descargadas en dispositivo y autorizadas». |
| H16 | **Baja** | `.gitignore` y `docs/PLAN-COMPLETO.md` R11 | **Confirmado en archivo:** `.gitignore` contiene reglas para `.env`, `data/*`, `music/local/*` y `music/gratis/*`. **No verificado** si archivos sensibles ya entraron al historial, ni otros nombres de secretos. | [Git: gitignore no afecta archivos ya seguidos](https://git-scm.com/docs/gitignore) | `git ls-files`, `git check-ignore -v`, escáner de secretos sobre historial; si hay exposición, rotar credenciales y eliminar contenido conforme a procedimiento seguro. |
| H17 | **Baja** | `docs/spec-diseno.md` §8b; radios | **Distinción legal:** un directorio de URL de radios no concede licencia para grabar/reemitir sus transmisiones. Escucha normal y archivo permanente son actos diferentes. | [Radio Browser proyecto](https://www.radio-browser.info/); derechos concretos de emisora **NO VERIFICADOS** | Ofrecer enlaces de streaming para escucha; no grabar, retransmitir ni conservar radio automáticamente. |

### Observaciones legales por fuente (estado)

| Fuente | Uso propuesto | Evaluación |
|---|---|---|
| Jamendo | Descarga automatizada a biblioteca offline | **BLOQUEAR** hasta resolver la restricción contractual de la API (cláusula 3.3); la licencia de la canción no resuelve por sí sola el uso de la API. |
| Internet Archive / Live Music Archive / 78 rpm | Descarga por identificador | **CONDICIONAR** a derechos explícitos de cada grabación/item, con verificación previa y respeto a sus términos. |
| Free Music Archive | Descarga | Descargas de pistas individuales previstas en sus términos, sujetas a licencia específica; **automatización NO VERIFICADA**. |
| ccMixter | Descarga o API | **NO VERIFICADO**: licencia y autorización técnica por pista/API; no implementar por suposición. |
| Musopen | Música clásica | **NO VERIFICADO** por obra/grabación; sus términos declinan garantizar estatus de dominio público; no implementar automatización sin revisión. |
| Bandcamp | Descargas manuales gratis o compradas | Solo archivos adquiridos y descargables legítimamente, con permisos para el uso pretendido; **NO VERIFICADO** que toda compra sea sin DRM o incluya derecho de redistribuir. |
| Radio Browser, SomaFM, NTS, KEXP y emisoras | Enlaces para escuchar | **NO VERIFICADO** disponibilidad o condiciones individuales; no inferir permiso de descarga/redistribución de la disponibilidad del stream. |
| CDs propios | Copia privada | **NO VERIFICADO** en jurisdicción del usuario. Titularidad del CD no implica permiso universal para eludir DRM ni distribuir; requiere abogado/localidad concreta. |

## B) [verificar] cerrados con evidencia (cierre limitado)

1. **A01 (solo cuestión de configuración):** `ND_MUSICFOLDER: /music` **sí está definido expresamente** en el compose inspeccionado. La documentación oficial confirma que `ND_MUSICFOLDER` controla carpeta de música y que su valor por defecto documentado es `./music`, no una garantía universal de `/music`. Por ello, la suposición previa de que no estaba definido es falsa para esta versión. **No** se cierra la prueba de indexación real. Fuente: https://www.navidrome.org/docs/usage/configuration/options/
2. **R2 (comportamiento de exposición):** la publicación sin IP en Docker enlaza todas las interfaces por defecto. **Confirmado el riesgo en configuración, no corregido todavía**. Fuente: https://docs.docker.com/get-started/docker-concepts/running-containers/publishing-ports/
3. **R16:** Windows está declarado como SO objetivo en `docs/spec-diseno.md` §2. **Cerrado a nivel de decisión**, no de compatibilidad probada.
4. **Mopidy Internet Archive (existencia del plugin):** listado oficialmente como extensión para Mopidy 4. **Cerrada existencia/documentación; pendiente compatibilidad reproducida en esta PC.** Fuente: https://mopidy.com/ext/internetarchive/
5. **Mopidy Jamendo (existencia, no funcionamiento):** la ficha existe, pero marca compatibilidad con Mopidy 4 como *Unconfirmed*. **No cerrar funcionamiento.** Fuente: https://mopidy.com/ext/jamendo/
6. **R11 (patrones de ignore):** `.gitignore` declara las exclusiones esperadas. **Cerrado solo existencia de reglas**, no ausencia de filtraciones históricas. Fuente: https://git-scm.com/docs/gitignore
7. **Licencias CC NC/ND:** NC restringe usos comerciales y ND distribución de adaptaciones, con matices legales; **cerrado el significado de las etiquetas, no la autorización de ninguna pista en particular**. Fuente: https://creativecommons.org/cc-licenses/

## C) [verificar] abiertos

1. **Pruebas del servidor:** `docker compose config`, estado de contenedores, escaneo efectivo de `/music`, permisos de los dos mounts, canciones, favoritos, playlists y restauración: **NO EJECUTADAS**.
2. **Sistema Windows:** Docker Desktop/WSL2, arranque sin sesión iniciada, recuperación tras reinicio, suspensión, rutas externas, antivirus, permisos, PowerShell: **NO VERIFICADOS**.
3. **Tailscale:** plan vigente, límites, restricciones ACL, Serve en Windows, HTTPS efectivo y apps de clientes: **NO VERIFICADOS EN ENTORNO**. Documentación de Serve: https://tailscale.com/docs/features/tailscale-serve
4. **Radios Navidrome:** soporte de estaciones en versión concreta, método de importación y compatibilidad de cada cliente: **NO VERIFICADO**.
5. **Apps Android/iOS:** precios, soporte Subsonic, descargas offline, reproducción en modo avión y HTTP/HTTPS: **NO VERIFICADOS** en dispositivos.
6. **Mopidy:** instalación para Windows, backend Jamendo e Internet Archive con prueba real, integración con Navidrome y función «guardar» desde reproducción: **NO VERIFICADOS**; podría requerir servicio adicional, no simple configuración.
7. **APIs/términos por fuente:** permisos de automatización FMA, ccMixter, Musopen; API vigente, cuotas, descarga/uso de archivos concretos: **NO VERIFICADOS**.
8. **Derechos de cada item de IA/Live Music/78rpm, cada pista CC y compras Bandcamp:** **NO VERIFICADOS**; se requiere evidencia individual.
9. **Copia privada de CD y límites de uso de streaming/catálogo** en República Dominicana u otra jurisdicción aplicable: **NO VERIFICADOS**; requerir consulta legal.
10. **R11 histórico:** ausencia de claves/IPs/música en Git e historial: **NO VERIFICADO**.
11. **R3/R7/R8/R10:** versión fija, etiquetado, pruebas funcionales y respaldo restaurado: **ABIERTOS**.
12. **Políticas de Jamendo:** comprobada restricción contractual general; alcance concreto de una excepción para este uso **NO VERIFICADO**, pedir autorización expresa.

## D) Lo que falta y no está suficientemente planificado

- **Puerta legal previa a cada origen**: derechos por pista + términos del servicio/API + permiso para automatizar + forma de uso (personal/offline/compartir), aprobación registrada; sin permiso, no se incorpora.
- **Manifiesto de procedencia** por audio (ID, obra, artista, URL de fuente, URL y versión de licencia, restricciones, fecha, hash, método de adquisición, atribución y decisión de revisión).
- **Diseño real de acceso remoto** que conecte `127.0.0.1` a Tailscale Serve por HTTPS y ajuste URLs de clientes; ACL y recuperación de cuenta.
- **Guía Windows probada** (PowerShell, Python, dependencias, WSL2, Bash explícito si fuera necesario, rutas y tareas programadas).
- **Plan de pruebas y criterios de aceptación** separados para servidor, apps, modo avión, reinicio Windows, red y permisos de descarga.
- **Backup/restauración tempranos**, cifrado de secretos, estrategia de duplicados, retención y límites de capacidad/espacio.
- **Gestión de fallos de origen externo** (API cambiante, bloqueos, límites, retiro de licencia, item borrado) y posibilidad de retirar contenido de biblioteca.
- **Decisión de interfaz**: no prometer un buscador global sin APIs aptas ni traducción fiable de una pista desde Mopidy hacia Navidrome.
- **Evitar duplicar servidores** mientras Navidrome satisfaga la experiencia núcleo; Mopidy/Jellyfin/Ampache/etc. solo con justificación funcional.

## E) Mejoras propuestas

*Prioridad 1 = imprescindible antes o durante fase 1; 2 = siguiente; 3 = opcional. Estimaciones de esfuerzo orientativas, no medidas. «Gratis» significa sin licencia pagada de software; hardware, electricidad, disco o conectividad pueden costar.*

| Propuesta | Beneficio | Costo (dinero; esfuerzo estimado) | Riesgo | Respaldo | Prioridad |
|---|---|---|---|---|---|
| Docker localhost + Tailscale Serve HTTPS | Evita exposición LAN innecesaria y permite acceso privado | Software disponible sin licencia pagada para uso elegible; medio | Configuración de proxy y cliente | https://docs.docker.com/get-started/docker-concepts/running-containers/publishing-ports/ ; https://tailscale.com/docs/features/tailscale-serve | **1** |
| Pinning de imagen + prueba de actualización/reversión | Reproducibilidad | Gratis; bajo | Actualizaciones manuales | https://docs.docker.com/reference/cli/docker/image/pull/ | **1** |
| Manifest de licencia y procedencia, rechazo por defecto | Evita admitir música de derechos dudosos | Código propio gratis; medio/alto | Metadatos incompletos | https://internetarchive.readthedocs.io/en/stable/metadata.html ; https://creativecommons.org/cc-licenses/ | **1** |
| Deshabilitar Jamendo API offline hasta aclarar contrato | Evita diseño contrario a términos | Gratis; bajo, pero menos catálogo | Menos variedad temporal | https://devportal.jamendo.com/api_terms_of_use | **1** |
| Respaldo/restauración mínimo en fase 1–2 | Reduce pérdida de biblioteca y favoritos | Software gratis; disco externo puede costar; medio | Pérdida/copia de secretos | https://www.navidrome.org/docs/usage/configuration/options/ | **1** |
| Guía PowerShell y smoke tests Windows | Reproducibilidad en PC objetivo | Gratis; medio | Incompatibilidades Docker/WSL | https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/copy-item | **1** |
| Mejoras script Jamendo si se autoriza | Descargas idempotentes, atribución completa | Gratis; medio | API/copyright | https://developer.jamendo.com/v3.0/tracks | **2** |
| Piloto de Mopidy Internet Archive antes de buscador | Confirma valor y compatibilidad antes de invertir en UI | Software libre/gratis; medio | Arquitectura dual y latencia | https://mopidy.com/ext/internetarchive/ | **2** |
| beets o MusicBrainz Picard para metadatos | Más orden en artistas/álbumes | Código abierto/gratis; bajo/medio | Etiquetas erróneas automáticas | https://beets.io/ ; https://picard.musicbrainz.org/ | **2** |
| Historial opcional ListenBrainz | Más historial entre dispositivos | Servicio/código disponible sin licencia pagada: condiciones actuales **NO VERIFICADAS**; medio | Privacidad de hábitos | https://listenbrainz.org/ | **3** |
| Jellyfin/otras herramientas solo si falta función real | Evita duplicar mantenimiento | Software libre; medio/alto | Recursos adicionales PC | https://jellyfin.org/ | **3** |

## F) Veredicto fase 1

**NO lista para ejecutar tal como está redactada. SÍ es viable preparar una fase 1 revisada** y someterla a aprobación del propietario.

**Bloqueadores antes de operar:** (1) corregir publicación del puerto y resolver HTTPS por tailnet sin dejar inutilizable el acceso remoto; (2) fijar imagen y presentar instrucciones Windows correctas; (3) separar instalación del núcleo de incorporación automática de música; (4) incorporar pruebas mínimas de escaneo/reinicio, contraseña y backup; (5) no lanzar descargas Jamendo/Internet Archive sin puerta legal. Las radios no deben ser criterio obligatorio de éxito hasta verificar soporte. No está demostrado que el sistema actual esté corriendo o sea inseguro en una máquina real: solo se identificaron problemas del repositorio y supuestos no acreditados.

**Alcance mínimo propuesto:** Navidrome local funcionando con una pista de prueba legal y documentada, Tailscale Serve privado, cliente celular probado, backup/restore probado y sin puertos del router abiertos. **Después** descargas por fuente con autorización documentada, luego piloto de streaming, y finalmente UI propia si se demuestra necesaria.

### Para la consolidación con Gemini

Contrastar, con pruebas independientes: alcance exacto cláusula 3.3 de Jamendo frente a biblioteca permanente; Navidrome `ND_MUSICFOLDER` explícito y escaneo real; publicación LAN de Docker; restricciones de Mopidy 4; autoridad de metadatos de licencias de IA; automatización FMA/Musopen/ccMixter; disponibilidad Tailscale Serve en Windows; reglas locales de copia privada. **El acuerdo entre dos modelos no acredita un hecho.** No convertir estas propuestas en cambios de código sin aprobación.

---
*Este documento es la respuesta completa de la auditoría ChatGPT basada en los archivos identificados. No representa una respuesta de Gemini o DeepSeek.*
