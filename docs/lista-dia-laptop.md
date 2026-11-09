# Lista para el día de la laptop

Objetivo del día: fase 1 en la PC (modo C, PC principal). La nube (fase 1B) queda para después.
Guía paso a paso: `docs/guia-fase1-windows.md`. Esta lista es lo que conviene tener listo **antes**.

## 1. Comprobaciones previas (5 minutos)
Requisitos de Docker Desktop según su documentación oficial (leída el 2026-11-09):
- Windows 10 versión 22H2 (compilación 19045) o Windows 11 23H2 (compilación 22631) o superior. Las ediciones Home y Education **sí** ejecutan contenedores Linux, que es lo que necesita Navidrome. **[verificar]** si una compilación inferior también sirve.
- WSL 2 versión 2.1.5 o superior.
- 8 GB de memoria.
- Virtualización activada en la BIOS/UEFI.

Cómo mirarlo (PowerShell; **[verificar]** que los comandos y menús existan en tu versión):
```powershell
winver                      # versión y compilación de Windows
wsl --version               # versión de WSL, si ya está instalado
systeminfo | Select-String "Memoria física total|Total Physical Memory"
```
Virtualización: Administrador de tareas, pestaña Rendimiento, CPU, campo "Virtualización". Si dice "Deshabilitada", hay que activarla en la BIOS.

Si algo no se cumple, **para y avísame** antes de instalar nada.

## 2. Cosas que te conviene tener a mano
- Cuenta de Tailscale (plan personal). **[verificar]** límites vigentes.
- El celular con la tienda de aplicaciones abierta; la app candidata es Substreamer (`docs/apps-celular.md`).
- Espacio libre en disco y una contraseña nueva para Navidrome.
- Un disco externo, para la copia de seguridad.
- La pista de prueba: `propuestas/prueba/tono-prueba.mp3`. No hace falta buscar música.

## 3. Orden del día
1. Docker Desktop e inicio de sesión automático.
2. Clonar el repo y copiar `.env`.
3. Compose de la fase 1 y `docker compose config`.
4. Copiar la pista de prueba y arrancar.
5. Tailscale y `tailscale serve --bg 4533`.
6. Celular con datos móviles.
7. Respaldo, restauración de prueba y reinicio.

## 4. Qué pegarme de vuelta
Cuando algo falle, pega el mensaje **completo** de PowerShell, sin cambiar nada, **pero borra** contraseñas, tokens y direcciones `*.ts.net` o `100.x.x.x` antes de pegarlo.
Al terminar cada paso, dime solo "OK" o el error.

## 5. Lo que NO se hace mañana
- Descargas automáticas (Jamendo bloqueado, Free Music Archive solo manual).
- Mopidy, buscador propio y la nube.
- Subir `.env` a GitHub.
