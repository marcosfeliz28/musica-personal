# Piloto de Mopidy (2026-11-09)

Alcance: contenedor Linux en la nube (Debian trixie, Python 3.13.5). Archivos en `propuestas/mopidy-piloto/`. **No es Windows ni se conectó a Navidrome ni a un celular.** Salida de audio falsa (`fakesink`): no se escuchó nada.

## Qué se probó
| Comprobación | Resultado |
|---|---|
| Instalar `mopidy` 4.0.5 y `mopidy-internetarchive` 4.0.1 | OK. Requieren Python 3.13 o superior. |
| Arrancar con la extensión y el servidor HTTP | OK (hubo que poner `mixer = none`; error mío de configuración). |
| Explorar el catálogo | OK: Audio Archive, Live Music Archive, LibriVox, Música/Arte/Cultura, etc. |
| Buscar "beethoven sonata" | OK: 20 álbumes. |
| Resolver un álbum (`lookup`) | OK: 14 pistas con nombre y duración. |
| Búsqueda de una pista de `netlabels` | 0 resultados: la extensión solo consulta unas colecciones fijas, y `netlabels` no está entre ellas. |
| Aviso en el registro | "Collection not found: 'audio_podcast'" (colección por defecto que ya no existe; menor). |
| `mopidy-jamendo` | No se instaló: su última versión en PyPI es de 2021 (0.1.0) y sin confirmar en Mopidy 4. |

## Hallazgos
1. **Mopidy no filtra por licencia.** Los resultados mezclan material con distinta situación de derechos:
   - Dos álbumes (Schnabel y Rachmaninoff) declaran "Public Domain Mark 1.0". Lo declara quien subió el archivo y depende de la jurisdicción; no es prueba (ChatGPT, H13).
   - Un disco de 78 rpm de Victor (colección `georgeblood`) **no declara ninguna licencia**. Con los scripts v2 se bloquearía.
   Conclusión: la acción "guardar en mi biblioteca" nunca debe copiar desde Mopidy directo; debe pasar por la puerta de licencia de `archive_descargar.py`.
2. **Mopidy es un reproductor de servidor.** Por diseño reproduce en la máquina donde corre y se controla por MPD o HTTP; no es un proxy que mande audio a un celular. Para oír en el teléfono habría que sacar su audio como flujo (por ejemplo con Icecast) o usar una app que reproduzca directo las URL de Internet Archive. **NO VERIFICADO** en este piloto: no se probó la salida de audio.
3. **El valor real de Mopidy aquí es la búsqueda y la exploración**, no la reproducción. Eso apoya la propuesta de Gemini de reemplazarlo por una web propia con reproductor HTML5 y un botón "guardar" que use los scripts con licencia. Pendiente de decisión.

## Sin probar
- Audio real, flujo hacia el celular, integración con Navidrome.
- Mopidy en Windows (se recomienda contenedor Linux).
- Jamendo con Mopidy (sin extensión confirmada ni clave).
