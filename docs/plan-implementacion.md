# Plan de implementación por fases

Estado: BORRADOR, pendiente de aprobación. Base: `docs/spec-diseno.md`.
Regla: no se instala ni se escribe código de una fase hasta que el usuario la apruebe.
Cada fase termina con una verificación real. Si algo no se puede probar, queda como **[verificar]**.

## Fase 1: Núcleo (Navidrome, Tailscale, radios)
Meta: escuchar desde cualquier lugar lo que haya en la biblioteca.
1. Instalar Docker Desktop en Windows y activar el arranque con el sistema.
2. Copiar `.env.example` a `.env`; ajustar `TZ` y las rutas.
3. Cambiar el puerto a `127.0.0.1:4533` o a la IP de Tailscale (cierra R2) y fijar la versión de la imagen (R3).
4. `docker compose up -d`; crear el administrador; confirmar que `/music` lista `local` y `gratis` (cierra A01).
5. Instalar Tailscale en la PC y en el celular, con la misma cuenta.
6. Agregar radios por internet en Navidrome **[verificar]** soporte en la versión instalada.
7. Configurar la PC: sin suspensión con corriente y reinicio automático de Docker.
Verificación: reproducir una pista desde el celular con datos móviles; 4533 no reenviado en el router.

## Fase 2: Descargas legales
Meta: llenar la biblioteca con música de licencia libre.
1. Revisar términos y API de Jamendo, Internet Archive y Free Music Archive **[verificar]**.
2. Jamendo: filtro de licencia (A10), reintentos y atribución sin duplicados.
3. Internet Archive: registrar licencia y atribución por item.
4. Free Music Archive: nuevo script, solo si sus términos lo permiten.
5. Tarea programada de Windows que baje música nueva cada cierto tiempo.
Verificación: 20 pistas descargadas, `ATRIBUCION.txt` con una línea por pista, reescaneo correcto.

## Fase 3: Streaming con Mopidy
Meta: buscar y reproducir catálogos sin descargar.
1. Evaluar extensiones de Mopidy para Jamendo e Internet Archive **[verificar]** que existan y estén mantenidas.
2. Instalar Mopidy como servicio.
3. Acción "guardar en mi biblioteca" que baje la pista a `music/gratis/`.
Verificación: buscar, reproducir y guardar una pista que aparezca luego en Navidrome.

## Fase 4: Buscador unificado y página de inicio
Meta: un solo punto de entrada.
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

## Riesgos que se vigilan
R2 (puerto abierto en la red local), R11 (repo público: nunca subir `.env`, claves ni IP de Tailscale), R13 (precios y límites de Tailscale y apps) y R15 (licencia de cada pista).

## Orden y dependencias
Fase 1 antes que todas. Las fases 2 y 3 son independientes entre sí. La fase 4 necesita las dos. La fase 5 puede ir en paralelo desde la fase 2.
