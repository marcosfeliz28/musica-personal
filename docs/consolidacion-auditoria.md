# Consolidación de auditorías (ChatGPT y Gemini)

Estado: BORRADOR para revisión del propietario. Solo documentación: no autoriza instalar ni cambiar código.
Fecha: 2026-11-08
Fuentes: `docs/auditoria-chatgpt.md`, auditoría de Gemini (pegada en la conversación, aún sin archivo en el repo), un script bash de origen no indicado. DeepSeek: sin respuesta.
Regla: el acuerdo entre dos modelos no prueba un hecho. Cada decisión cita lo que se verificó.

## 1. Verificado por Claude con fuente primaria
| Hecho | Resultado | Fuente |
|---|---|---|
| `ND_MUSICFOLDER` en la imagen oficial de Navidrome | El Dockerfile define `ENV ND_MUSICFOLDER=/music` y `ND_DATAFOLDER=/data`. A01 se cierra como falso positivo. Falta probar el escaneo real. | Dockerfile en github.com/navidrome/navidrome |
| Etiquetas de imagen | Existen `0.54.1` y `0.60.3`. La más reciente vista el 2026-11-08 fue `0.64.2`. Fijar una versión probada al implementar, no una vieja. | Docker Hub, deluan/navidrome |
| Jamendo y el acceso sin conexión | Los términos de la API dicen: las aplicaciones "must not be specifically designed to cache the content nor offering an offline access to the content". Está en otra cláusula, no en la 3.3. La 3.3 trata del uso no comercial. | devportal.jamendo.com/api_terms_of_use |
| Jamendo y uso personal | Existe una licencia "para fines privados y personales", limitada al marco de uso de la API. | misma página |
| Texto de `PLAN-COMPLETO.md` | Usa `--genero lofi --cantidad 20`. El hallazgo G03 de Gemini es falso. | `docs/PLAN-COMPLETO.md` |

Alcance real de la restricción de Jamendo: es una zona gris para un script personal, no una prohibición probada. Se resuelve preguntando a Jamendo, o evitando la descarga automática.

## 2. Tabla de decisiones
| Tema | ChatGPT | Gemini | Decisión |
|---|---|---|---|
| Puerto 4533 | Loopback + Tailscale Serve | Igual | **Adoptar.** Un solo esquema; actualizar URL de clientes. |
| Imagen Navidrome | Fijar versión | Fijar `0.60.3` | **Adoptar fijar versión.** Elegir la versión al implementar; verificar compatibilidad. |
| A01 | Definido, falta prueba | Falso positivo | **Cerrado en configuración.** Prueba real en fase 1. |
| Jamendo automático | Bloquear hasta aclarar | No lo ve | **Adoptar bloqueo.** Descarga manual o streaming. Consultar a Jamendo. |
| Filtro de licencia | Evaluar según uso | Filtro NC/ND/SA | **Registrar la licencia exacta por pista.** No excluir NC/ND para uso privado sin criterio. |
| Internet Archive | Fail closed por metadatos | Python + `licenseurl` | **Adoptar fail closed.** Los metadatos son declarados por terceros; revisión humana. |
| Free Music Archive y Musopen | Solo manual | Solo manual | **Adoptar.** Sin automatización. |
| ccMixter | No verificado | API oficial | **Dejar abierto.** Leer términos antes de decidir. |
| Mopidy | Prueba piloto antes | Eliminar la fase | **Piloto.** `mopidy-jamendo` no confirmado en Mopidy 4; `mopidy-internetarchive` sí figura. |
| Buscador propio | Solo si hace falta | Absorbe a Mopidy | **Condicionado a la prueba piloto.** |
| Respaldo y restauración | Adelantar a fases 1–2 | Respaldo nativo `ND_BACKUP_*` | **Adelantar.** Evaluar `ND_BACKUP_*` **[verificar]**; incluir `ATRIBUCION.txt` y `music/gratis`. |
| Comandos de Windows | Guías PowerShell | Igual | **Adoptar.** |
| Docker Desktop y arranque | Sin verificar | Arranca tras iniciar sesión | **Plausible, sin probar.** Probar con reinicio real. |
| ListenBrainz | Fase 3 | Fase 1 | **Opcional.** Privacidad: se envían hábitos de escucha. Condiciones **[verificar]**. |
| Promesa "cualquier circunstancia" | Es falsa | No lo toca | **Adoptar reformulación.** Ver sección 4. |
| Radios | No grabar ni retransmitir | Abiertas | **Solo escuchar.** No éxito obligatorio hasta verificar soporte. |
| Tailscale límites | Abierto | "Cerrado" con cifras contradictorias | **Abierto.** |
| Ley de copia privada | Abogado | Cita ley dominicana | **Abierto.** Pregunta para abogado. |
| Veredicto fase 1 | No lista tal cual | Sí, con dos ajustes | **No lista tal cual.** Ver sección 3. |

## 3. Fase 1 revisada (propuesta)
Alcance: probar el núcleo sin descargas automáticas.
1. Docker Desktop en Windows; inicio de sesión automático solo si se acepta el riesgo **[verificar]**.
2. Navidrome con versión fija y `127.0.0.1:4533`.
3. `tailscale serve` hacia el puerto local; probar en el celular fuera de casa.
4. Una pista de prueba con licencia documentada, copiada a mano.
5. Verificar el escaneo real de `/music`, listas, favoritos y aleatorio.
6. Respaldo y restauración probados una vez.
7. Contraseña propia, sin puertos del router abiertos.
Criterio de éxito: suena la pista de prueba desde el celular con datos móviles y se restaura un respaldo.
Sin descargas automáticas, sin Mopidy y sin buscador propio en esta fase.

## 4. Cambios a los documentos existentes (pendientes de aprobación)
- Promesa: "Biblioteca local accesible mientras servidor y red estén disponibles; sin conexión suenan solo las pistas descargadas en el dispositivo y autorizadas."
- Fase 2 se divide: 2a (manifiesto de procedencia y descarga manual) y 2b (automatización por fuente con permiso).
- Fase 3 y 4 quedan condicionadas a una prueba piloto.
- `PLAN-COMPLETO.md`: añadir recetas PowerShell.

## 5. Script bash recibido: no aplicar
Ideas aprovechables: `--dry-run`, etiquetas de licencia con mutagen, guía de restauración, `SECURITY.md`.
Fallas que lo descartan tal cual:
1. Etiqueta con la licencia del item todos los MP3 y FLAC de `./music`, y pisaría la licencia de otras pistas.
2. Elimina `--genero` y `--buscar`, exige la clave por línea de comandos y quita las carpetas Artista/Álbum y las correcciones de descarga parcial.
3. Monta `./music` entera y rompe `MUSICA_LOCAL` y `MUSICA_GRATIS` del `.env`.
4. Añade `music/` y `data/` al `.gitignore` y anula las excepciones de `.gitkeep`.
5. Usa `read -p`, `rsync` y `chown`, que no sirven en tareas de Windows.
6. Hace `git push` sin revisión y marca como cerrado lo que nadie probó.

## 6. Pendiente
- Respuesta de DeepSeek.
- Archivo `docs/auditoria-gemini.md` en el repo.
- Aprobación de este documento antes de cambiar scripts, compose o fases.
- Consulta a Jamendo y, para la copia de CDs, a un abogado.

## 7. Revisión de lo recibido después (2026-11-08)

### Auditoría de Gemini
Guardada tal cual en `docs/auditoria-gemini.md`. Sigue incluyendo el hallazgo G03, que es falso: `PLAN-COMPLETO.md` ya usa `--genero lofi --cantidad 20`. Corrige solo la cifra de usuarios de Tailscale; su veredicto de fase 1 no cambia.

### Scripts propuestos (`propuestas/`)
Revisión estática. Compilan sin errores de sintaxis. No se ejecutaron ni se probó la red.

**`propuestas/jamendo_descargar.py`**
- Verificado en la documentación de la API de Jamendo: existen `ccnc`, `ccnd`, `ccsa`, `boost`, `audiodlformat` (mp31, mp32, ogg, flac), `type=single albumtrack`, `include=licenses` y el límite de 200 resultados.
- Mejoras reales: carga `.env`, nombres seguros en Windows, ID de pista en el nombre del archivo, timeouts, descarga parcial con `.part` y atribución sin duplicados.
- **No resuelve la restricción contractual de Jamendo** (sección 1). Sigue descargando a una biblioteca permanente sin ninguna puerta. Propuesta: exigir una bandera explícita (por ejemplo `--acepto-terminos-api`) y no ejecutar sin ella, hasta consultar a Jamendo.
- `license_ccurl` no aparece en el texto de la página de documentación que revisé. Probar con una respuesta real antes de confiar en él.
- Sin etiquetas de licencia en el archivo y sin `--dry-run` (ideas del script bash, aún sin recuperar).

**`propuestas/archive_descargar.py`**
- Mejoras reales: funciona en Windows sin Bash ni `ia`, verifica `licenseurl` antes de bajar, evita duplicar FLAC y MP3, usa `.part`, timeouts y atribución sin duplicados.
- **Problema legal:** `COLECCIONES_AUTORIZADAS` trata como libres las colecciones `georgeblood` y `78rpm`. Pertenecer a esa colección no prueba que una grabación sea de dominio público (ChatGPT, H13). Propuesta: quitar ambas de la lista por defecto.
- `etree` (Live Music Archive) y `freemusicarchive`: permitir solo con una nota en la atribución y revisión humana **[verificar]**.
- Para elegir entre original y derivado conviene usar el campo `source` de los metadatos, no solo el nombre del archivo.
- Archivos con el mismo nombre en subcarpetas del item pueden pisarse.
- Hay que actualizar README y `PLAN-COMPLETO.md`, que aún citan `archive_descargar.sh`.

### Decisión pendiente
Ninguno de los dos se activa hasta que apruebes la fase 1 revisada y se apliquen las dos correcciones de arriba.

## 8. Tercera auditoría (Claude): verificaciones y scripts v2

### Discrepancia con el paquete recibido
- El paquete llegó **cortado** (el bloque de `docker-compose.yml` no cierra y falta lo que seguía). Se trabajó con lo completo.
- El `docker-compose.yml` del paquete dice ser "actual, en la rama", pero **no coincide con el repo**. El repo (gana el repo) usa `${MUSICA_LOCAL}` y `${MUSICA_GRATIS}` como dos volúmenes, sin `user` ni `ND_DATAFOLDER`, y sigue en `latest` y `"4533:4533"`. El del paquete monta `./music:/music:ro`, que es la versión del script bash descartado.

### Pendientes resueltos con fuente (2026-11-08)
| Tema | Resultado | Fuente |
|---|---|---|
| Free Music Archive | **Automatizar está prohibido.** Sección 7(e): "You will not attack the Site with automated requests or attempt to data mine the Site". Solo descarga manual. | freemusicarchive.org/terms_of_use |
| ccMixter | Tiene API pública (Query API 2.0 beta). Su sección 8 solo exige aceptar las políticas. **No encontré permiso ni prohibición explícita de descargas masivas.** Licencia por pista. | ccmixter.org/terms y ccmixter.org/query-api |
| Musopen | **NO VERIFICADO**: el servidor respondió 403 a la consulta automática. Mantener descarga manual. | musopen.org/tos |
| Radios en Navidrome | La página de resumen lista "Internet Radios" entre sus funciones. La página específica de radios no existe (404). Soporte por versión **NO VERIFICADO**. | navidrome.org/docs/overview |
| Jamendo | Sin cambios: restricción de caché y acceso sin conexión, más licencia de uso privado y personal limitada al marco de la API. | devportal.jamendo.com/api_terms_of_use |

### Hallazgo nuevo sobre Live Music Archive
Una búsqueda en Internet Archive devolvió **0 items de la colección `etree` con `licenseurl`**. Un script que falle cerrado bloquea todo Live Music Archive. Opciones: descarga manual desde la web, o `--forzar-licencia` tras leer a mano los permisos de cada banda. El campo `licenseurl` lo declara quien sube el item, así que no es prueba de derechos (ChatGPT, H02).

### Scripts v2 (`propuestas/v2/`, no activos)
Correcciones respecto a la sección 7:
- **Jamendo:** se niega a descargar sin `--acepto-terminos-api`; con `--dry-run` solo lista. Omite pistas sin `license_ccurl`. Valida que lo recibido sea un MP3, limita el tamaño, pagina de 200 en 200 y la clave solo se lee del entorno o de `.env`.
- **Internet Archive:** ya no trata colecciones ni texto libre como licencia; solo `licenseurl` de Creative Commons o dominio público. `--forzar-licencia` queda anotado como FORZADO. Elige original sobre derivado con el campo `source`, conserva subcarpetas saneadas y tiene `--dry-run`.

Pruebas hechas: sintaxis, pruebas unitarias de las funciones puras, el bloqueo de Jamendo sin bandera, la falta de clave, un item sin licencia (cancela) y un item con licencia CC0 (lista sus pistas en `--dry-run`).
**No probado:** ninguna descarga real, ni Jamendo con clave (no hay clave), ni el campo `license_ccurl` en una respuesta real.

### Petición A: borrador del mensaje a Jamendo (para que lo envíes tú)
Para: licensing@jamendo.com (dirección que aparece en los términos de la API).
> Hola. Soy un usuario particular y no comercial. Quiero montar un servidor de música personal para mi uso privado, sin anuncios, sin ingresos y sin compartirlo con terceros. Me gustaría guardar en mi propio equipo algunas pistas con licencia Creative Commons descargadas con mi clave de la API, y escucharlas desde mis dispositivos. Los términos de la API indican que las aplicaciones no deben estar diseñadas para guardar contenido ni ofrecer acceso sin conexión. ¿Este uso personal está permitido, o prefieren que solo use el streaming o las descargas manuales desde la web? Gracias.

### Pendiente para el propietario
Aprobar la fase 1 revisada. Enviar el mensaje a Jamendo (opcional). Respuesta de DeepSeek (opcional). Un abogado debe revisar la copia de CDs propios.
