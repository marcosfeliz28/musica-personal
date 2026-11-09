# Guía de la fase 2 en Windows (PowerShell)

Estado: BORRADOR. **No se probó en Windows.** Lo probado en Linux: `propuestas/v2/archive_descargar.py` bajó un MP3 real de Internet Archive (ver `docs/prueba-scripts-v2.md`). Jamendo sigue bloqueado y Free Music Archive es solo manual.
Requisito: la fase 1 funcionando.

## 0. Puerta legal (antes de cada fuente)
Tres preguntas, por escrito en `music\gratis\PROCEDENCIA.md`: ¿de quién son los derechos de la obra?, ¿los términos del servicio permiten esto?, ¿permiten automatizarlo? Sin las tres respuestas, solo descarga manual.
`licenseurl` en Internet Archive lo declara quien sube el item: no es prueba de derechos.

## 1. Python en Windows
Instala Python 3 desde python.org (marca "Add python.exe to PATH") **[verificar]**. Comprueba:
```powershell
py -3 --version
```

## 2. Activar el script de Internet Archive
Solo después de aprobar `propuestas\v2`. Hay que copiar también `comun.py`, que comparten los scripts:
```powershell
Copy-Item propuestas\v2\archive_descargar.py scripts\archive_descargar.py
Copy-Item propuestas\v2\comun.py scripts\comun.py
py -3 scripts\archive_descargar.py <identificador> --dry-run
```
Lee la licencia que muestra. Si es correcta:
```powershell
py -3 scripts\archive_descargar.py <identificador> --max-pistas 3
```
Los archivos quedan en `music\gratis\archive\<identificador>\` y la atribución en `music\gratis\archive\ATRIBUCION.txt`. Reescanea desde la web de Navidrome.

Si responde "acceso restringido", el item no es público: no se puede bajar. Si responde que no declara licencia, no insistas con `--forzar-licencia` hasta revisar los derechos en `https://archive.org/details/<identificador>`.

## 3. Control de espacio
Antes de bajar, mira el espacio libre:
```powershell
Get-PSDrive C | Select-Object Used, Free
```
Deja siempre un margen amplio. Un tope automático aún no está implementado en los scripts.

## 4. Tarea programada (solo si hay una fuente con permiso para automatizar)
Hoy ninguna fuente lo permite. No programes Jamendo ni Free Music Archive. Si más adelante una fuente lo permite, se programa con `Register-ScheduledTask` **[verificar]** y con un tope de espacio.

## 5. Respaldo
Incluye `music\gratis\` y los `ATRIBUCION.txt`, además de `data` y `music\local` (ver `docs/guia-fase1-windows.md`, paso 8).
