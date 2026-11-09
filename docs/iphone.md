# Usar tu música en el celular (iPhone y Android)

Actualizado el 2026-11-09. Nada de esto se probó en un teléfono. El nombre del archivo se conserva por los enlaces antiguos.
Lista de apps y lo que declara cada una: [`apps-celular.md`](apps-celular.md).

## 1. Acceso desde fuera de casa (Tailscale)
1. Instala Tailscale en la PC servidora y en el celular (tienda de aplicaciones; **[verificar]** precio y límites del plan personal).
2. Inicia sesión con la misma cuenta en ambos.
3. En la PC, `tailscale serve --bg 4533` publica Navidrome dentro de tu red privada con HTTPS (`docs/guia-fase1-windows.md`, paso 6).
4. Usa la dirección `https://...ts.net` que muestre. No la subas al repo.

## 2. App
Navidrome usa el protocolo Subsonic. Candidata inicial: **Substreamer** (iOS y Android, gratis y de código abierto según el directorio de Navidrome). Alternativas: Symfonium o Tempus en Android, Amperfy en iPhone.
Configura: servidor = la dirección HTTPS del paso 1, y tu usuario y contraseña de Navidrome.

## 3. Música sin conexión
Las fichas de varias apps declaran descargas sin conexión. **[verificar]** en tu app, y en modo avión. Ocupan espacio.

## 4. Con el servidor de respaldo (modo C)
Guarda en la app las dos direcciones (PC y nube) si tu app admite varios servidores **[verificar]**. Usa la de la nube solo si la PC está fuera de servicio.

## Seguridad
No abras el puerto 4533 en el router. El compose de la fase 1 lo publica solo en `127.0.0.1`; el acceso remoto pasa por Tailscale.
