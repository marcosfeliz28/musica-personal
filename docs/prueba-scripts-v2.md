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
