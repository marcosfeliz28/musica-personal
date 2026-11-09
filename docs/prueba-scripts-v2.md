# Prueba de los scripts v2 (2026-11-09)

Alcance: entorno Linux en la nube, carpeta temporal fuera del repo (borrada después). **No es Windows.** Solo se probó `archive_descargar.py`; Jamendo no se descargó (sin clave y bloqueado por decisión).

## Internet Archive (`propuestas/v2/archive_descargar.py`)
| Caso | Resultado |
|---|---|
| Item sin `licenseurl` (colección `etree`) | Cancela con mensaje claro. |
| Item con licencia CC0 pero **de acceso restringido** | La descarga real dio **401**. Causa: `access-restricted-item: true` y archivos `private`. El script lo mostraba como error genérico. **Corregido**: ahora cancela de entrada con un mensaje explícito y `seleccionar()` ignora archivos privados. |
| Item público con licencia CC (`mtk014`, BY-ND-NC 1.0) | `--dry-run` lista la pista; la descarga real bajó 4 103 408 bytes. `ffprobe`: MP3 válido, 256 s, con título y artista. |
| Atribución | Una línea con licencia y enlace al item. |
| Reintento | No vuelve a bajar, no duplica la atribución y no deja archivos `.part`. |
| Item sin archivos de audio (solo carátula) | Responde "no tiene archivos MP3 ni FLAC utilizables". |

## Lo que se aprendió
- Una búsqueda mostró que `licenseurl` con Creative Commons es común en netlabels, pero ningún item de `etree` (Live Music Archive) lo declara.
- El campo `creator` puede faltar; en el ejemplo la atribución dice "desconocido" aunque la etiqueta del MP3 trae el artista. Mejora pendiente: usar la etiqueta como respaldo.
- La licencia BY-ND-NC permite copia personal no comercial; no se redistribuyó ni se copió al repo.

## Sin probar
- Windows (`py -3`, rutas, antivirus).
- Jamendo: parámetros de licencia verificados en la documentación, sin llamada real.
- Descargas largas o interrumpidas, y colisiones de nombres.

## Revisión de código y correcciones (2026-11-09)
Una revisión de código de `propuestas/v2` encontró 9 problemas. Se verificaron uno por uno contra el código antes de corregir: 8 eran errores reales y 1, un riesgo de documentación.
| Problema | Corrección |
|---|---|
| Nombres de archivo de más de 80 caracteres perdían su `.flac` o `.mp3`, y dos nombres largos podían colisionar | `nombre_archivo()` conserva la extensión y, si acorta, añade un hash corto |
| `AUX.mp3` o `nul.flac` no se protegían (en Windows están reservados aunque lleven extensión) | Se comprueba la parte antes del primer punto |
| El tope de tamaño dependía solo de `Content-Length` | Descarga por trozos con tope real de bytes |
| Saltos de línea en título o autor partían la línea de atribución | `una_linea()` normaliza los campos |
| Ctrl-C dejaba archivos `.part` | `try/finally` los borra siempre |
| El `.env` con BOM de Notepad, `export` o comentarios al final fallaba | Lector nuevo; verificado con los tres casos |
| Al mover el script a `scripts/`, la raíz apuntaba fuera del repo | `raiz_repo()` busca `.git`, o `docker-compose.yml` junto con `.env.example`; admite `MUSICA_RAIZ` |
| Funciones duplicadas en los dos scripts | Módulo común `propuestas/v2/comun.py` |
| El compose de `propuestas/v2` resolvía `./data` y `./music` bajo esa carpeta | Aviso al inicio del archivo: copiarlo a la raíz |

Error propio descubierto al probar: la primera versión de `raiz_repo()` se detenía en `propuestas/v2` por el `docker-compose.yml` de la propuesta. Corregido con el marcador doble.

Pruebas: 13 casos automáticos pasaron, incluido un servidor local que envía datos por trozos sin declarar tamaño. Descarga real de `mtk014` repetida con la versión corregida: mismo resultado (4 103 408 bytes, una línea de atribución, reintento sin duplicar). Item restringido y Jamendo sin bandera siguen bloqueados.
Sigue sin probarse: Windows y Jamendo con clave.
