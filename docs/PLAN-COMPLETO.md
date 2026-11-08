# Plan completo: Música personal (Navidrome + Tailscale + app Subsonic en iPhone)

> **Documento de trabajo para edición por varios modelos.**
> Estado: borrador v1 (Claude Haiku) → auditoría v1 (Claude Sonnet, hecha, ver abajo) → edición Gemini → edición DeepSeek → edición ChatGPT → contra-auditoría final.
> Convención: **[verificar]** = viene de conocimiento general, no de los archivos del repo; comprobar en documentación vigente.

## Instrucciones para quien edite este documento

1. No borres contenido de otros: corrige, agrega y marca cada cambio en la sección "Registro de cambios" (al final) con tu nombre de modelo.
2. No inventes datos. Si no puedes verificar algo (precios, límites, versiones), déjalo como **[verificar]**.
3. Mantén el español y los comandos exactos.
4. Revisa en especial: R1 (carpeta de música de Navidrome), R4 (clave de Jamendo), R11 (.gitignore), la licencia de cada fuente y el historial de reproducción.
5. No agregues claves, contraseñas ni datos personales. El repo es público.

---

## 1) Objetivo y alcance

- Biblioteca musical propia, sin suscripción mensual, escuchable desde el iPhone.
- Fuentes: biblioteca local (`music/local/`), música gratuita y legal (Jamendo, Internet Archive) y radios por internet (solo mencionadas, no configuradas).
- Acceso remoto privado con Tailscale, sin abrir puertos en el router.
- Funciones: listas de reproducción, buscador, favoritos, aleatorio, organización por artistas y álbumes e historial (este último **parcial**: contador de reproducciones; el historial completo puede requerir scrobbling, ver sección 5).
- Fuera de alcance: Spotify, YouTube Music y descargas de servicios comerciales; exposición pública a Internet.

## 2) Arquitectura

```
 iPhone: app Subsonic (Amperfy / Substreamer / play:Sub)
        │  http://100.x.y.z:4533  (cifrado por Tailscale)
 ═══════╪═══════ red privada Tailscale
        │
 Computadora o Raspberry Pi (servidor en casa)
   Tailscale (cliente)
   Docker: contenedor navidrome (puerto 4533)
     /data         <- ./data
     /music/local  <- ./music/local   (solo lectura)
     /music/gratis <- ./music/gratis  (solo lectura)
   Scripts en el host:
     jamendo_descargar.py -> music/gratis/jamendo/ + ATRIBUCION.txt
     archive_descargar.sh -> music/gratis/archive/
```

| Componente | Función | Definido en |
|---|---|---|
| Navidrome | Servidor, indexa y expone API Subsonic | `docker-compose.yml` |
| Docker | Ejecuta Navidrome | `docker-compose.yml` |
| Tailscale | Red privada iPhone ↔ servidor | `docs/iphone.md` |
| App Subsonic | Interfaz en el iPhone | `docs/iphone.md` |
| Scripts | Descargan música libre | `scripts/` |
| `.env` | Rutas, zona horaria, clave de Jamendo | `.env.example` |

## 3) Requisitos previos

- Equipo encendido de forma continua (computadora o Raspberry Pi). **[verificar]** arquitectura soportada por la imagen de Navidrome.
- Docker con plugin `compose`; Python 3; Bash; `pip install internetarchive` (solo para Internet Archive).
- Clave gratuita de Jamendo (devportal.jamendo.com).
- Cuenta de Tailscale (plan personal) en servidor e iPhone. **[verificar]** límites del plan gratuito.
- App Subsonic en el iPhone. **[verificar]** precio vigente en la App Store.
- Música local en formatos soportados por Navidrome **[verificar]** y espacio en disco suficiente.

## 4) Pasos de instalación

1. Comprobar Docker: `docker --version && docker compose version`
2. Clonar y entrar: `git clone https://github.com/marcosfeliz28/musica-personal.git && cd musica-personal`
3. Configurar: `cp .env.example .env` y editar `TZ`, `MUSICA_LOCAL`, `MUSICA_GRATIS`, `JAMENDO_CLIENT_ID`.
4. Poner tu música en `music/local/` (o apuntar `MUSICA_LOCAL` a tu carpeta).
5. Validar: `docker compose config`
6. Arrancar: `docker compose up -d && docker compose ps && docker compose logs -f navidrome`
7. Abrir http://localhost:4533 y crear el usuario administrador. Si el servidor no tiene pantalla (p. ej. Raspberry Pi), abrir `http://<IP-del-servidor>:4533` desde otro equipo de la red local. **[verificar]** que el primer usuario sea administrador.
8. Escanear: esperar `ND_SCANSCHEDULE: 1h` o lanzarlo desde la interfaz. **[verificar]** ubicación del botón.
   Verificación funcional (no solo sintaxis): `docker compose exec navidrome ls /music` debe listar `local` y `gratis`, y el conteo de canciones en la web debe coincidir con tu música.
9. Jamendo (el script lee el entorno del shell, no `.env`):
   ```bash
   set -a; . ./.env; set +a
   python3 scripts/jamendo_descargar.py --genero lofi --cantidad 20
   ```
   Revisar `music/gratis/jamendo/ATRIBUCION.txt` y reescanear.
10. Internet Archive: `pip install internetarchive && bash scripts/archive_descargar.sh <identificador>`; reescanear. El comando `ia` debe estar en el `PATH` (a veces queda en `~/.local/bin`); el script avisa si no lo encuentra.
11. Tailscale en el servidor (guía oficial según tu sistema): `sudo tailscale up` y `tailscale ip -4` (IP `100.x`).
12. Probar desde otro dispositivo de la tailnet: `http://<IP-Tailscale>:4533`.
13. Tailscale en el iPhone (misma cuenta) y configurar la app (sección 7).
14. Arranque automático: `restart: unless-stopped` cubre el contenedor; Docker y Tailscale deben iniciar con el sistema. **[verificar]** por sistema operativo.
15. Hacer un respaldo (sección 8).

## 5) Cobertura de funciones

Ninguna función se configura en el repo: las provee Navidrome y la app. Verificar cada una en la versión instalada.

| Función | Cómo se cubre | Estado |
|---|---|---|
| Listas de reproducción | Web de Navidrome y app | **[verificar]** edición desde la app |
| Buscador | Web y app (API Subsonic) | **[verificar]** |
| Favoritos | Por usuario en Navidrome | **[verificar]** |
| Aleatorio | Canciones o álbumes | **[verificar]** |
| Historial | Contador de reproducciones; historial completo puede requerir scrobbling (Last.fm / ListenBrainz) | **Parcial / [verificar]** |
| Artistas y álbumes | Según etiquetas (tags) de los archivos y carpetas `Artista/Álbum/` | Depende de la calidad de las etiquetas (R7) |

Complemento recomendado y no incluido: `beets` (etiquetado y orden).

## 6) Fuentes gratuitas y legales

| Fuente | En el repo | Licencia | Pendiente |
|---|---|---|---|
| Jamendo | `scripts/jamendo_descargar.py` (`audiodownload_allowed=true`) | Creative Commons, por pista; se guarda `license_ccurl` | No filtra por tipo de licencia (NC/ND/atribución) |
| Internet Archive | `scripts/archive_descargar.sh` (`*.mp3`, `*.flac`) | Varía por item | No comprueba licencia ni registra atribución |
| Free Music Archive | Solo mencionada | CC por pista | No implementada |
| Radios por internet | Solo mencionadas | Depende de la emisora | No configuradas; **[verificar]** soporte en Navidrome |
| Navidrome | Servidor | **[verificar]** (se cree GPL-3.0) | Revisar repo oficial |
| Tailscale | Acceso remoto | **[verificar]** | Límites del plan |

No es asesoría legal; manda la licencia de cada pista.

## 7) Acceso desde el iPhone

1. Tailscale activo en servidor e iPhone con la misma cuenta.
2. IP del servidor: `tailscale ip -4`.
3. Instalar Amperfy, Substreamer o play:Sub.
4. Servidor `http://<IP-de-Tailscale>:4533`, usuario y contraseña de Navidrome.
5. Probar reproducción, favorito, lista, aleatorio y búsqueda.
6. Descargas sin conexión desde la app (ocupan espacio).

A verificar: **[verificar]** si iOS/la app permite HTTP; alternativa `tailscale serve` con HTTPS. No abrir el puerto 4533 en el router.

## 8) Respaldo y mantenimiento

- Respaldar `data/` (usuarios, favoritos, listas, historial), `.env` (secreto), `music/local/` (original) y conservar `ATRIBUCION.txt`.
- Respaldo (desde la carpeta del repo; Navidrome se reinicia aunque `tar` falle):
  ```bash
  docker compose stop navidrome
  tar -czf "$HOME/respaldo-musica-$(date +%F).tar.gz" data .env music/local; r=$?
  docker compose start navidrome
  [ "$r" -eq 0 ] && echo "Respaldo OK" || echo "tar falló (código $r); Navidrome ya se reinició"
  ```
  Si `MUSICA_LOCAL` apunta a otra carpeta, respáldala aparte (la ruta `music/local` solo cubre la carpeta del repo).
- Restaurar (desde la carpeta del repo, sustituye la fecha):
  ```bash
  docker compose stop navidrome
  tar -xzf "$HOME/respaldo-musica-AAAA-MM-DD.tar.gz"; r=$?
  docker compose start navidrome
  [ "$r" -eq 0 ] && echo "Restaurado" || echo "tar falló (código $r)"
  ```
- Actualizar: `docker compose pull && docker compose up -d` (la imagen usa `latest`; considerar fijar versión).
- Logs: `docker compose logs --tail=100 navidrome`.

## 9) Riesgos y límites conocidos

- **R1.** Carpeta de música: el compose monta `/music/local` y `/music/gratis` sin definir `ND_MUSICFOLDER`. El borrador de Haiku lo marca como riesgo de biblioteca vacía y propone `ND_MUSICFOLDER: /music`. **Sin confirmar:** el auditor debe comprobar el valor por defecto en la documentación oficial.
- **R2.** `"4533:4533"` escucha en todas las interfaces de red local; revisar firewall o enlazar a la IP de Tailscale.
- **R3.** Imagen `latest` sin versión fija.
- **R4.** El script de Jamendo lee `os.environ`, no `.env`; sin el paso 9 falla con "Falta JAMENDO_CLIENT_ID". El README no lo explica.
- **R5.** Script de Jamendo: duplica líneas en `ATRIBUCION.txt` al reejecutar, deja archivos parciales si falla una descarga, fuerza `.mp3`, sin reintentos ni filtro de licencia.
- **R6.** Script de Internet Archive sin comprobación de licencia ni atribución.
- **R7.** Organización por artistas/álbumes depende de las etiquetas; `beets` no está incluido.
- **R8.** Funciones sin pruebas automáticas; historial completo posiblemente requiere servicio externo.
- **R9.** Free Music Archive y radios sin implementar.
- **R10.** Respaldo solo manual.
- **R11.** Repo público: confirmar que `.gitignore` excluye `.env`, `music/` y `data/` (`git check-ignore -v .env`).
- **R12.** HTTP dentro de Tailscale.
- **R13.** Límites o costos de Tailscale y de las apps del iPhone sin verificar.
- **R14.** Raspberry Pi mencionada pero no probada.
- **R15.** Legal: licencia de cada pista; sin verificación automática.
- **R16.** Sistema operativo no especificado.

## 10) Checklist final

- [ ] `docker compose config` sin errores y `docker compose ps` con `navidrome` Up.
- [ ] http://localhost:4533 carga y el administrador existe.
- [ ] El conteo de canciones coincide con `music/local/` (R1).
- [ ] Artistas y álbumes agrupan bien en una muestra de 10 pistas (R7).
- [ ] Jamendo descarga con el `.env` cargado y `ATRIBUCION.txt` tiene una línea por pista.
- [ ] Internet Archive descarga un item de prueba con licencia verificada a mano.
- [ ] `tailscale status` muestra servidor e iPhone.
- [ ] La app conecta y se prueban reproducción, favoritos, lista, aleatorio y búsqueda.
- [ ] Descarga sin conexión probada en modo avión.
- [ ] Puerto 4533 no reenviado en el router.
- [ ] `git check-ignore -v .env` confirma que `.env` está ignorado; `git status` limpio.
- [ ] Respaldo de `data/` y `.env` creado y restaurado en prueba.
- [ ] Contenedor y Tailscale arrancan tras reiniciar el equipo.

## Auditoría v1 (Claude Sonnet) y qué se hizo

| ID | Sev. | Hallazgo | Estado |
|---|---|---|---|
| A01 | Alta | R1: biblioteca posiblemente vacía sin `ND_MUSICFOLDER` | **Dudoso.** Navidrome escanea `/music` por defecto y las carpetas están montadas dentro de `/music`, por lo que probablemente no era un fallo. Se fijó `ND_MUSICFOLDER: /music` de forma explícita (inofensivo). **Verificar en la práctica:** `docker compose exec navidrome ls /music` y el conteo de canciones. |
| A02 | Alta | Script de Jamendo no lee `.env` | Corregido en README (se carga con `set -a; . ./.env; set +a`). Falta rellenar `JAMENDO_CLIENT_ID`. |
| A03 | Media | `.gitignore` no versionaba `music/*/.gitkeep`; un clon nuevo no tenía las carpetas | **Corregido.** Patrones `music/local/*` y `music/gratis/*`; ahora los `.gitkeep` están versionados. README añade `mkdir -p`. |
| A04 | Media | README ejecutaba el script sin `bash`; `ia` puede no estar en el `PATH` | **Corregido.** README usa `bash`; aviso del `PATH` en README y paso 10; el script comprueba `ia` y avisa. |
| A05 | Media | `docker compose config` solo valida sintaxis | **Corregido.** Verificación funcional (`docker compose exec navidrome ls /music`) en README y paso 8. Sin ejecutar aquí. |
| A06 | Media | Respaldo: `stop` + `tar` puede dejar Navidrome parado; falta incluir `music/local/` | **Corregido.** Comandos de respaldo y restauración que reinician Navidrome aunque falle `tar`; incluyen `music/local`. Sin probar en un servidor real. |
| A07 | Media | README e `iphone.md` afirman cosas como hechos (gratis, "solo tus dispositivos entran", descargas sin conexión) | **Corregido.** Afirmaciones sin respaldo marcadas **[verificar]** o retiradas ("solo tus dispositivos entran" sustituido por aviso de `4533:4533` abierto en la red local). |
| A08 | Media | README y alcance prometen "historial" sin matiz | **Corregido.** Marcado como parcial en README y en el alcance. |
| A09 | Baja | Script de Jamendo duplicaba atribución y dejaba archivos parciales | **Corregido** (descarga a `.part`, sin duplicados, errores omitidos). `limpio()` ahora devuelve "desconocido" con nombres vacíos o `..` (quita puntos en los extremos). |
| A10 | Baja | Sin filtro de licencia | Pendiente. |
| A11 | Baja | Paso 7 usa `localhost` aunque el servidor sea una Raspberry sin pantalla | **Corregido.** Paso 7 y README indican la IP del servidor si no tiene pantalla. |

**Para los editores (Gemini, DeepSeek, ChatGPT):** resuelvan los pendientes, revisen que A01 sea de verdad un falso positivo y no cierren ninguno sin evidencia.

---

## Registro de cambios

| Fecha | Modelo | Cambio |
|---|---|---|
| 2026-11-08 | Claude Haiku | Borrador v1 |
| 2026-11-08 | Claude Sonnet | Auditoría v1 (11 hallazgos) |
| 2026-11-08 | Claude (orquestador) | Aplicadas correcciones A02, A03, A04 (README), A09; `ND_MUSICFOLDER` explícito |
| 2026-11-08 | Claude Sonnet (editor) | Resueltos A04, A05, A06, A07, A08, A09 (`limpio()`), A11; A01 sigue dudoso; A10 y licencias sin tocar |
