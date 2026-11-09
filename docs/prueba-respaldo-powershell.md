# Prueba del script de respaldo (2026-11-09)

Script: `propuestas/windows/respaldo.ps1`. Probado con PowerShell 7.4.2 oficial en un contenedor Linux, sobre un repo de prueba, con `-SinDocker`. **No es Windows PowerShell 5.1 ni Windows.**

## Por qué existe
La guía de la fase 1 usaba `Compress-Archive` para respaldar `data`, la música y `.env`. La documentación de Microsoft (versiones 5.1 y 7.4) dice que esa herramienta limita el tamaño máximo a 2 GB e ignora los archivos ocultos. Una biblioteca de música puede superar eso, así que la música se copia sin comprimir.

## Resultados
| Caso | Resultado |
|---|---|
| Respaldar: `.zip` de `data`, suma SHA-256, música local y gratis con subcarpetas, y `.env` | OK |
| Restaurar tras borrar `data` y la música | OK: todo vuelve igual |
| Restaurar cuando `data` existe | OK: lo posterior al respaldo queda en `data.bak-<fecha>`, no se pierde |
| `.zip` alterado | Rechazado por la suma SHA-256; `data` queda intacta |
| Restaurar sin respaldo | Falla con un mensaje claro |

## Errores míos que encontró la prueba
1. La rama alternativa de copia usaba `-LiteralPath` con un comodín `*`, que no se expande.
2. El script exigía que `data` existiera **incluso al restaurar**, cuando justo después de un desastre ya no existe. Ahora esa comprobación solo aplica al respaldar.

## Sin probar
- **`robocopy`:** no existe en Linux; en esta prueba se usó la copia alternativa. Es la ruta que correrá en Windows. Los códigos 0 a 7 se tratan como éxito según la convención conocida de `robocopy` **[verificar]**.
- **Docker:** la prueba omitió `docker compose stop/start`.
- **Windows PowerShell 5.1:** y la política de ejecución de scripts.
- **Archivos de más de 2 GB:** no aplica a `data`, que es pequeño; sí a la música, que no usa zip.
