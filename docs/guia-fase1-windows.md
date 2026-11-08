# Guía de la fase 1 en Windows (PowerShell)

Estado: BORRADOR. Los comandos de PowerShell y de Windows **no se probaron** (no hay Windows en la nube). Lo que sí se probó está en `docs/prueba-fase1-linux.md`. Cada paso lleva su verificación; si algo falla, para y avísame.
Ejecuta todo desde PowerShell, en la carpeta del repo.

## 0. Antes de empezar
- Cuenta de Tailscale (plan personal) **[verificar]** límites y precio vigentes.
- No pongas música con derechos dudosos. Para la prueba usa una pista de dominio público o Creative Commons, o un tono generado por ti.

## 1. Docker Desktop
1. Instálalo desde la web oficial de Docker y reinicia si lo pide.
2. Ábrelo y activa "Start Docker Desktop when you sign in" **[verificar]** nombre exacto de la opción.
3. Comprueba: `docker --version` y `docker compose version`.
Aviso: en Windows con WSL 2, los contenedores pueden levantar solo después de iniciar sesión. Se prueba en el paso 8.

## 2. Repo y configuración
```powershell
git clone https://github.com/marcosfeliz28/musica-personal.git
cd musica-personal
git checkout spec-diseno-ampliacion
Copy-Item .env.example .env
```
Edita `.env` (`notepad .env`): deja `TZ` y las rutas. **No subas `.env` a GitHub.**
```powershell
New-Item -ItemType Directory -Force music\local, music\gratis, data | Out-Null
```

## 3. Compose de la fase 1
Copia la propuesta (versión fija, solo `127.0.0.1`) sobre el compose activo, después de revisar la versión:
```powershell
Copy-Item propuestas\v2\docker-compose.yml docker-compose.yml
docker compose config
```
`docker compose config` no debe dar errores.

## 4. Una pista de prueba
Copia a mano **una** pista legal a `music\local\` y anota su licencia en `music\local\ATRIBUCION.txt`.

## 5. Arrancar y verificar
```powershell
docker compose up -d
docker compose ps
docker compose exec navidrome ls /music
```
Debe listar `gratis` y `local`. Abre http://127.0.0.1:4533 en tu PC y crea el administrador con una contraseña propia. Espera el escaneo o lánzalo desde la interfaz. Comprueba que la pista aparece por artista y álbum, y prueba favorito, lista y aleatorio.

## 6. Tailscale
1. Instala Tailscale en la PC y en el celular, con la misma cuenta.
2. En la PC, en PowerShell: `tailscale serve --bg 4533`
3. El comando guía para activar HTTPS en tu tailnet si hace falta. Muestra una dirección `https://<nombre-de-tu-pc>.<tailnet>.ts.net`.
4. `tailscale serve status` debe mostrarla **[verificar]**.
Esa dirección es privada, pero no la pegues en el repo ni en chats públicos.

## 7. Celular
Instala una app compatible con Subsonic **[verificar]** precio y descargas sin conexión. Servidor: la dirección HTTPS del paso 6, con tu usuario y contraseña. Prueba con **datos móviles**, con el Wi-Fi apagado: debe sonar la pista de prueba.

## 8. Respaldo y restauración
Respaldo (para el contenedor un momento):
```powershell
docker compose stop navidrome
Compress-Archive -Path data, music\local, music\gratis -DestinationPath "$HOME\respaldo-musica-$(Get-Date -Format yyyy-MM-dd).zip" -Force
docker compose start navidrome
```
Restauración de prueba:
```powershell
docker compose stop navidrome
Rename-Item data data.bak
Expand-Archive -Path "$HOME\respaldo-musica-AAAA-MM-DD.zip" -DestinationPath . -Force
docker compose start navidrome
```
Comprueba que siguen tu usuario, el favorito y la lista. Solo entonces borra `data.bak`.
El respaldo automático de Navidrome (`ND_BACKUP_*`) guarda solo la base de datos. **[verificar]** si lo activas.

## 9. Reinicio
Reinicia Windows sin abrir sesión de inmediato y comprueba si Navidrome responde. Anota el resultado. Si no responde hasta iniciar sesión, es la limitación conocida de Docker Desktop.

## 10. Seguridad
- No reenvíes el puerto 4533 en el router.
- Contraseña propia; no reutilices otra.
- Antes de cada commit: `git status` y `git diff`, sin `.env`, claves ni direcciones de Tailscale.

## Criterio de éxito de la fase 1
Suena la pista de prueba desde el celular con datos móviles, y se restaura un respaldo sin pérdida.
