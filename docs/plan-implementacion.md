# Plan de implementación por fases

Estado: fase 1 revisada incorporada el 2026-11-08 por decisión delegada del propietario ("haz lo que entiendas"); sigue pendiente su confirmación expresa antes de instalar nada. Base: `docs/spec-diseno.md` y `docs/consolidacion-auditoria.md`.
Regla: no se instala ni se escribe código de una fase hasta que el usuario la apruebe.
Cada fase termina con una verificación real. Si algo no se puede probar, queda como **[verificar]**.

## Fase 1: Núcleo mínimo (revisada tras tres auditorías)
Meta: probar el núcleo de punta a punta con una sola pista legal, sin descargas automáticas.
No incluye: descargas automáticas, Mopidy ni buscador propio.
1. Instalar Docker Desktop en Windows. Probar el arranque tras un reinicio completo **[verificar]**: Docker Desktop puede levantar los contenedores solo después de iniciar sesión.
2. Copiar `.env.example` a `.env`; ajustar `TZ` y las rutas. Mantener `MUSICA_LOCAL` y `MUSICA_GRATIS` como dos carpetas.
3. Navidrome con **versión fija probada** (no `latest`) y puerto `127.0.0.1:4533:4533`. Ver `propuestas/v2/docker-compose.yml`. Elegir la versión al implementar; el 2026-11-09 la más reciente era `0.64.2` (igual que `latest`) y su escaneo dio 28 HIGH y 0 CRITICAL, todos con corrección disponible río arriba: ver `docs/escaneo-imagen-navidrome.md`. Volver a escanear antes de actualizar.
4. `tailscale serve` hacia el puerto local, para acceso privado con HTTPS dentro de la tailnet **[verificar]** comando exacto y activación de HTTPS en la versión instalada. Actualizar la URL en la app del celular.
5. Copiar a mano **una pista de prueba** con licencia documentada, y anotarla en `music/local/ATRIBUCION.txt`.
6. Verificar `docker compose exec navidrome ls /music`, el escaneo real, listas, favoritos y aleatorio.
7. Respaldo y restauración probados una vez (A06; recetas en PowerShell, no Bash).
8. Contraseña propia en Navidrome; puerto 4533 no reenviado en el router.
Criterio de éxito: suena la pista de prueba desde el celular con datos móviles, y se restaura un respaldo sin pérdida.
Radios por internet: opcionales hasta verificar el soporte en la versión elegida.

## Fase 1B: servidor de respaldo en la nube (modo C, decidido por el propietario)
La PC sigue siendo la principal; esta fase va después de que la fase 1 funcione. Ver `docs/despliegue-pc-y-nube.md`.
1. El propietario crea su cuenta de Oracle (Claude no puede).
2. Máquina Arm Always Free con Linux, Docker, Tailscale y Navidrome con la misma versión que la PC.
3. Música: Syncthing de PC a nube. Base de datos: respaldo de la PC copiado a la nube.
4. Simulacro de fallo: apagar la PC, restaurar en la nube y verificar; luego volver a la PC.
5. Copia adicional en disco externo, porque Oracle puede recuperar una máquina inactiva.
Criterio de éxito: tras el simulacro, usuario, favoritos, listas y música están en la nube y suena una pista desde el celular.

## Fase 2: Procedencia y descargas con permiso
Meta: llenar la biblioteca con música cuyos derechos estén documentados.
Puerta legal previa a cada fuente: derechos de la obra, términos del servicio o API, y permiso para automatizar. Sin las tres, solo descarga manual.
2a. Manifiesto de procedencia por pista (fuente, licencia, URL, fecha) y descarga manual.
2b. Automatización solo donde esté permitida. Estado hoy:
- **Jamendo:** bloqueada hasta aclarar con Jamendo (restricción de caché y acceso sin conexión). Streaming o descarga manual mientras tanto.
- **Free Music Archive:** automatizar está prohibido por sus términos (sección 7(e)). Solo manual.
- **Internet Archive:** `propuestas/v2/archive_descargar.py`, solo con `licenseurl` libre.
2c. Tarea programada de Windows solo para fuentes con permiso, con tope de espacio en disco.
Verificación: una pista de cada fuente permitida suena en Navidrome con su licencia anotada y reescaneo correcto.

## Fase 3: Streaming con Mopidy (solo piloto)
Meta: buscar y reproducir catálogos sin descargar. Condicionada a una prueba piloto: `mopidy-jamendo` no está confirmado en Mopidy 4; `mopidy-internetarchive` sí figura.
Resultado del piloto (2026-11-09, ver `docs/piloto-mopidy.md`): búsqueda y exploración de Internet Archive funcionan; Mopidy no filtra por licencia y reproduce en el servidor, no en el celular; `mopidy-jamendo` tiene su última versión de 2021. **Decisión pendiente del propietario:** mantener Mopidy solo para buscar, o reemplazarlo por una web propia con reproductor y botón "guardar" que use los scripts con licencia.
1. Evaluar extensiones de Mopidy para Jamendo e Internet Archive **[verificar]** que existan y estén mantenidas.
2. Instalar Mopidy como servicio.
3. Acción "guardar en mi biblioteca" que baje la pista a `music/gratis/`.
Verificación: buscar, reproducir y guardar una pista que aparezca luego en Navidrome.

## Fase 4: Buscador unificado y página de inicio (condicionada)
Meta: un solo punto de entrada. Solo si el piloto de la fase 3 demuestra que hace falta.
1. Diseñar la web (grupos "En tu biblioteca" y "Para descubrir"), con contraseña propia.
2. Consultar la API Subsonic de Navidrome y las APIs de los catálogos.
3. Acciones: reproducir, guardar, añadir a lista.
Verificación: una búsqueda devuelve resultados de ambos grupos y funciona desde el celular por Tailscale.

## Fase 5: Extras
1. beets para etiquetas y carátulas (cierra R7).
2. Descargas sin conexión en la app del celular **[verificar]** por app.
3. Respaldo automático de `data/`, `music/local/` y `ATRIBUCION.txt` a un disco externo; probar la restauración.
4. Jellyfin como pestaña opcional.
Verificación: modo avión con una lista descargada; restauración probada.

## Fase 6: Ampliación de fuentes legales
Meta: más variedad, siempre con licencia libre o compras sin DRM.
1. Live Music Archive e Internet Archive 78 rpm: descarga manual, o `archive_descargar.py` con `--forzar-licencia` tras revisar los derechos de cada item (ningún item de `etree` declara `licenseurl`; 78 rpm no es dominio público por defecto).
2. Radio Browser: importar emisoras a Navidrome **[verificar]** formato y soporte.
3. Emisoras independientes (SomaFM, NTS, KEXP) **[verificar]** URLs vigentes.
4. Bandcamp: guía para descargas gratis y compras sin DRM hacia `music/local/`.
5. ccMixter y Musopen: revisar API y términos **[verificar]**; solo se implementa si lo permiten.
6. CDs propios: guía con fre:ac o abcde **[verificar]** ley local.
7. ListenBrainz para historial completo; Picard junto a beets.
8. Evaluar Funkwhale, Ampache y Audiobookshelf; no se instalan por defecto.
Verificación: una pista de cada fuente nueva suena en Navidrome con su licencia anotada.
Fuera de alcance: cualquier fuente sin licencia (piratería).

## Riesgos que se vigilan
R2 (puerto abierto en la red local), R11 (repo público: nunca subir `.env`, claves ni IP de Tailscale), R13 (precios y límites de Tailscale y apps) y R15 (licencia de cada pista).

## Orden y dependencias
Fase 1 antes que todas. Las fases 2 y 3 son independientes entre sí. La fase 4 necesita las dos. La fase 5 puede ir en paralelo desde la fase 2. La fase 6 va después de la fase 2.
