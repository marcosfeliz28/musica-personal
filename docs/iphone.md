# Usar tu música en el iPhone

## 1. Acceso desde fuera de casa (Tailscale)
1. Instala Tailscale en la computadora que corre el servidor y en el iPhone (App Store; **[verificar]** precio y límites del plan).
2. Inicia sesión con la misma cuenta en ambos.
3. En la computadora ejecuta `tailscale ip -4` para ver su IP (empieza con 100.).

## 2. App en el iPhone
Navidrome usa el protocolo Subsonic, así que sirven estas apps (confirma precio actual en la App Store):
- **Amperfy**
- **Substreamer**
- **play:Sub**

Configura: servidor `http://<IP-de-Tailscale>:4533`, tu usuario y contraseña de Navidrome. **[verificar]** que iOS y la app permitan HTTP; si no, usa `tailscale serve` con HTTPS.

## 3. Música sin conexión
**[verificar]** Algunas apps Subsonic permiten descargar álbumes y listas para escucharlos sin internet; comprueba en la app elegida (ocupan espacio).

## Seguridad
No abras el puerto 4533 en tu router; con Tailscale no hace falta. **[verificar]** quién puede conectarse: el compose publica `4533:4533` en todas las interfaces de la red local, así que revisa el firewall o enlaza el puerto a la IP de Tailscale.
