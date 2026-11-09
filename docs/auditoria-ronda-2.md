# Auditoría externa, ronda 2 (ChatGPT, Gemini, DeepSeek)

Estado: listo para usar. Rama: `spec-diseno-ampliacion` (no `main`).
Repo público: https://github.com/marcosfeliz28/musica-personal/tree/spec-diseno-ampliacion
Esta ronda **no repite** la primera. Pide refutar afirmaciones de Claude y revisar lo nuevo.

## Cómo usarlo
1. Una conversación nueva por modelo.
2. Pega el prompt de abajo. Si el modelo no puede abrir enlaces, pega también los archivos de la lista.
3. Guarda cada respuesta completa como `docs/auditoria-r2-chatgpt.md`, `docs/auditoria-r2-gemini.md` y `docs/auditoria-r2-deepseek.md`.
4. Antes de pegar, no incluyas claves, `.env`, contraseñas ni direcciones de Tailscale.

## Archivos a revisar (rama `spec-diseno-ampliacion`)
`docs/consolidacion-auditoria.md`, `docs/despliegue-pc-y-nube.md`, `docs/piloto-mopidy.md`, `docs/prueba-scripts-v2.md`, `docs/prueba-fase1-linux.md`, `docs/plan-implementacion.md`, `docs/guia-fase1-windows.md`, `propuestas/v2/archive_descargar.py`, `propuestas/v2/jamendo_descargar.py`, `propuestas/v2/docker-compose.yml`.
Enlace crudo de ejemplo: https://raw.githubusercontent.com/marcosfeliz28/musica-personal/spec-diseno-ampliacion/docs/consolidacion-auditoria.md

## Prompt para pegar
```
Eres auditor técnico y legal, escéptico, de un proyecto personal en español: una plataforma de
música propia (Navidrome en Docker, Tailscale, PC con Windows como servidor principal y una
máquina en la nube como respaldo). Solo se permite música con licencia libre, dominio público o
comprada sin DRM. Las fuentes piratas están fuera de alcance y no las recomiendes.

Una auditoría anterior (tres modelos) ya produjo hallazgos. En esta ronda tu trabajo es:
1. REFUTAR. Para cada afirmación de la lista de abajo, intenta demostrar que es falsa o
   incompleta consultando la fuente primaria. Di CONFIRMADA, REFUTADA o NO VERIFICADA.
2. REVISAR lo nuevo: los scripts de propuestas/v2, el modo C (PC principal y nube de respaldo)
   y el piloto de Mopidy. Busca errores que pierdan datos, riesgos legales y fallas en Windows.
3. DECIR qué falta.

Afirmaciones a refutar:
 A1. Los términos de la API de Jamendo dicen que las aplicaciones "must not be specifically
     designed to cache the content nor offering an offline access to the content", y esa frase
     NO está en la cláusula 3.3 (que trata del uso no comercial). Hay otra cláusula que da licencia
     para uso privado y personal dentro del marco de la API.
 A2. Los términos de Free Music Archive (sección 7(e)) prohíben las solicitudes automatizadas.
 A3. En Internet Archive, "licenseurl" lo declara quien sube el item y no prueba los derechos;
     pertenecer a una colección (georgeblood, 78rpm, etree) no equivale a una licencia.
 A4. Ningún item de la colección etree (Live Music Archive) declara licenseurl.
 A5. Oracle Always Free: 2 OCPU y 12 GB para Ampere A1, 200 GB de disco en total incluido el de
     arranque, y puede recuperar instancias con uso de CPU, red y memoria por debajo del 20%
     durante 7 días.
 A6. El respaldo automático de Navidrome (ND_BACKUP_*) guarda solo la base de datos.
 A7. El servidor de Tailscale SSH existe solo en Linux y macOS.
 A8. Syncthing propaga los borrados; sincronizar no es respaldar.
 A9. Mopidy reproduce en el servidor donde corre y no envía audio a un celular por sí solo.
 A10. La imagen deluan/navidrome publica linux/arm64.
 A11. Render gratis tiene sistema de archivos efímero; Fly.io no tiene plan gratuito para cuentas nuevas.

Reglas:
- No inventes precios, límites, versiones ni términos. Si no puedes comprobarlo, escribe
  NO VERIFICADO y di por qué.
- Cada hallazgo cita archivo, línea o sección, y un enlace a la fuente.
- No es asesoría legal; señala qué debe revisar un abogado.
- El acuerdo entre modelos no prueba un hecho. Cita la fuente.

Formato en español:
A) Tabla de refutación: ID | Veredicto | Evidencia (enlace y cita breve) | Matiz
B) Hallazgos nuevos: ID | Severidad | Archivo y sección | Hallazgo | Evidencia | Corrección
C) Riesgos del modo C que pierden datos o dejan dos bases activas
D) Lo que falta
E) ¿Está lista la fase 1 para ejecutarse en Windows? Sí o no, y por qué.
```

## Registro
| Auditor | Fecha | Archivo | Refutadas | Hallazgos nuevos | Veredicto fase 1 |
|---|---|---|---|---|---|
| ChatGPT | | `docs/auditoria-r2-chatgpt.md` | | | |
| Gemini | | `docs/auditoria-r2-gemini.md` | | | |
| DeepSeek | | `docs/auditoria-r2-deepseek.md` | | | |
