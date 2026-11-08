# Usar tu música en el iPhone

## 1. Acceso desde fuera de casa (Tailscale)
1. Instala Tailscale en la computadora que corre el servidor y en el iPhone (App Store, gratis).
2. Inicia sesión con la misma cuenta en ambos.
3. En la computadora ejecuta `tailscale ip -4` para ver su IP (empieza con 100.).

## 2. App en el iPhone
Navidrome usa el protocolo Subsonic, así que sirven estas apps (confirma precio actual en la App Store):
- **Amperfy**
- **Substreamer**
- **play:Sub**

Configura: servidor `http://<IP-de-Tailscale>:4533`, tu usuario y contraseña de Navidrome.

## 3. Música sin conexión
Las apps permiten descargar álbumes y listas para escucharlos sin internet.

## Seguridad
No abras el puerto 4533 en tu router. Con Tailscale no hace falta y solo tus dispositivos entran.
