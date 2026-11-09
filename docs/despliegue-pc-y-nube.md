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

## Decisión del propietario (2026-11-09): modo C
**PC principal, nube de respaldo.** Si la PC falla, el sistema sigue desde la copia de la nube.
Interpretación de Claude de "backup en el A": copia de respaldo en la nube. Si el propietario quiso otra cosa, se corrige aquí.

### Qué se copia y cómo
| Qué | Cómo | Estado |
|---|---|---|
| Música | Syncthing, de la PC a la nube, nube en "solo recibir" y con versionado | **[verificar]** nombres de las opciones; no probado |
| Base de datos (`data/`) | Respaldo periódico en la PC y copia del archivo a la nube por `scp` sobre Tailscale (Windows trae cliente OpenSSH) | **[verificar]**; no probado |
| `.env` | Copia manual y segura. Nunca al repo | |
Aviso: lo que cambie en la PC después del último respaldo (favoritos, listas, reproducciones) **se pierde** si hay que pasar a la nube.

### Pasar a la nube (si la PC falla)
1. Confirma que la PC está de verdad apagada o fuera de servicio. **Nunca dos servidores con usuarios activos.**
2. En la nube: restaura el último respaldo de `data/` y levanta Navidrome.
3. En el celular, usa la dirección de la nube (guarda las dos direcciones en la app; Ultrasonic declara varios servidores **[verificar]** en la app que elijas).

### Volver a la PC
1. Para Navidrome en la nube y haz un respaldo de su `data/`.
2. Cópialo a la PC, restaura y levanta.
3. Deja la nube detenida, con el respaldo nuevo.

### El riesgo que no se puede ignorar
Un servidor de respaldo casi siempre parado es justo lo que Oracle puede recuperar por inactividad (documentación de Oracle). Por eso **la nube no puede ser tu única copia**: mantén además una copia en un disco externo. Mitigación contra la recuperación: no verificada.

### Prueba obligatoria antes de confiar
Simular el fallo: apagar la PC, restaurar en la nube y comprobar usuario, favoritos, listas y música. Hasta hacerlo, el respaldo en la nube cuenta como **no probado**.
