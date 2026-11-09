# Despliegue en PC y en la nube

Estado: BORRADOR. Nada de esto se probó en Oracle ni en Windows. Lo probado en Linux amd64 está en `docs/prueba-fase1-linux.md`.
Meta del propietario: que todo se pueda manejar desde la nube y desde la PC.

## Principio
Una sola receta (Docker Compose más `.env`) sirve para los dos sitios. El estado del sistema son tres cosas: `data/` (usuarios, listas, favoritos), la música y `.env`. Mover el sistema es mover esas tres cosas.

## Qué es igual y qué cambia
| Tema | PC con Windows | Servidor en la nube (Oracle, propuesta) |
|---|---|---|
| Compose y versión de Navidrome | El mismo `propuestas/v2/docker-compose.yml` | El mismo |
| Arquitectura | amd64 | Arm. La imagen `0.64.2` publica linux/arm64 (verificado en Docker Hub) |
| Acceso remoto | Tailscale y `tailscale serve --bg 4533` | Igual |
| Administración | Local, en PowerShell | **Tailscale SSH**: su servidor existe solo en Linux y macOS (documentación oficial), no en Windows |
| Arranque | Docker Desktop; puede levantar solo tras iniciar sesión **[verificar]** | `restart: unless-stopped` en un Linux sin sesión **[verificar]** |
| Disponibilidad | Depende de que la PC esté encendida | Siempre encendido, salvo que Oracle lo recupere |
| Recursos | Los de tu PC | 2 procesadores, 12 GB de memoria y 200 GB de disco en total, incluido el del sistema (documentación de Oracle) |
| Costo | $0 más electricidad | $0 si se mantiene en Always Free; condiciones de registro **NO VERIFICADAS** |

## Tres modos de uso
- **A. Solo PC.** Es la fase 1 actual.
- **B. Solo nube.** Lo mismo, pero en un servidor. La PC solo administra.
- **C. Los dos.** Uno es el **principal** y el otro un espejo o respaldo.

Regla de oro del modo C: **una sola base de datos activa.** Navidrome guarda usuarios, listas y favoritos en una base SQLite. No sincronices `data/` en vivo entre dos instancias encendidas: se corrompe o se pierden cambios.
- **Música:** sí se puede mantener igual en los dos sitios, por ejemplo con Syncthing (código abierto, funciona en Windows, macOS y Linux, según su web). La sincronización **no es un respaldo**: un borrado se propaga. Conviene que la copia de la nube sea de "solo recibir" y activar versionado **[verificar]** los nombres exactos de esas opciones.
- **Respaldo de `data/`:** manual o con `ND_BACKUP_*` (solo guarda la base de datos).

## Mover el sistema de un sitio a otro
1. Para el principal y haz el respaldo (`docs/guia-fase1-windows.md`, paso 8).
2. Copia el respaldo y `.env` al otro sitio.
3. Restaura y levanta.
4. Comprueba usuario, favoritos, lista y que la música aparezca por artista y álbum.
Probado: respaldo y restauración entre carpetas en Linux amd64. **No probado:** entre Windows y Linux, ni entre amd64 y Arm. El formato de la base debería ser el mismo, pero hay que comprobarlo **[verificar]**.

## Fase 1B (opcional): servidor en Oracle Always Free
Solo si el propietario decide el modo B o C. Pasos de alto nivel, ninguno probado:
1. **El propietario** crea la cuenta de Oracle. Claude no puede crear cuentas, dar datos personales ni aceptar términos.
2. Crear una máquina Arm Always Free con Linux y disco de hasta 200 GB, dentro del límite gratuito.
3. Instalar Docker y Tailscale (guías oficiales para Linux arm64).
4. Clonar el repo, copiar `.env` y el compose, y levantar.
5. `tailscale serve --bg 4533` y habilitar Tailscale SSH para administrar.
6. No abrir el puerto 4533 en las reglas de red de Oracle.
7. Probar respaldo, restauración y reinicio de la máquina.

Riesgos documentados por Oracle: puede recuperar máquinas "inactivas" (uso de procesador, red y memoria por debajo del 20% durante 7 días); a veces responde "out of host capacity". Un servidor de música para una persona puede quedar por debajo de esos umbrales.

## Seguridad
- Repo público: nada de `.env`, claves, direcciones de Tailscale ni IP de la nube.
- No abrir puertos públicos. Todo el acceso pasa por Tailscale.
- Contraseñas distintas en Navidrome, Tailscale y Oracle.

## Pendiente
Decisión del propietario: modo A, B o C, y si crea la cuenta de Oracle.
