# Apps de celular para Navidrome

Fuente: directorio oficial https://www.navidrome.org/apps/ (111 apps al 2026-11-09). Cualquier app compatible con la API OpenSubsonic funciona con Navidrome.
Alcance: lo que cada ficha **declara**. No se probó ninguna app en un teléfono, ni su precio actual en la tienda, ni su comportamiento en modo avión.

## Candidatas
| App | Plataforma | Costo según el directorio | Funciones declaradas | Actualizada |
|---|---|---|---|---|
| Substreamer | iOS y Android | Gratis y código abierto | Descargas sin conexión, scrobbling, listas, valoraciones | 2026-10-13 |
| Symfonium | Android | Prueba gratuita | Ecualizador, Android Auto; reúne varias fuentes | 2026-09-22 |
| Tempus (bifurcación de Tempo) | Android | Código abierto | Android Auto, Chromecast, scrobbling | 2026-10-25 |
| Tempo | Android | Código abierto | Modo sin conexión, Last.fm, Chromecast | 2024-12-31 |
| Ultrasonic | Android | Gratis y código abierto | Modo sin conexión, varios servidores, listas | 2026-03-10 |
| DSub2000 | Android | No indicado | Bifurcación de DSub, listas, control en pantalla de bloqueo | 2026-11-01 |
| Amperfy | iOS, iPadOS, macOS | No indicado | Soporte sin conexión, CarPlay, podcasts | 2026-08-13 |
| Arpeggi | iOS 17 o superior | Gratis, en TestFlight | Reproducción sin conexión, transcodificación | 2026-11-06 |
| play:Sub | iOS | De pago | Caché automática y manual, CarPlay | 2026-10-24 |

## Recomendación inicial (a confirmar con una prueba real)
Probar primero **Substreamer**: es gratis, de código abierto, sirve en iOS y Android, y declara descargas sin conexión. Si falla, Symfonium en Android o Amperfy en iPhone.

## Qué falta comprobar en tu teléfono
- Que la app acepte la dirección HTTPS de `tailscale serve` (fase 1, paso 6).
- Que las descargas funcionen **en modo avión**.
- Precio actual en la tienda y permisos pedidos.
- Que reproduzca la pista de prueba con datos móviles.
