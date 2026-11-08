# Auditoría externa (ChatGPT y Gemini)

Estado: listo para usar. Rama: `spec-diseno-ampliacion`.
Repo público: https://github.com/marcosfeliz28/musica-personal/tree/spec-diseno-ampliacion

## Cómo usarlo
1. Abre una conversación nueva en ChatGPT y otra en Gemini. Una por modelo, sin mezclar.
2. Pega el **prompt** de abajo. Si el modelo no puede abrir enlaces, pega también el contenido de estos archivos de la rama:
   - `docs/spec-diseno.md`
   - `docs/plan-implementacion.md`
   - `docs/PLAN-COMPLETO.md`
   - `docker-compose.yml`
   - `scripts/jamendo_descargar.py` y `scripts/archive_descargar.sh`
3. Guarda cada respuesta completa en `docs/auditoria-chatgpt.md` y `docs/auditoria-gemini.md`.
4. Regresa a Claude con esos dos archivos para consolidar y decidir qué se corrige.

No pegues claves, `.env`, contraseñas ni IP de Tailscale. El repo es público.

## Prompt para pegar

```
Eres auditor técnico y legal de un proyecto personal en español: una plataforma de música
propia, sin suscripciones, para uso personal. Solo se permite música con licencia libre,
dominio público o comprada sin DRM. Las fuentes piratas están fuera de alcance.

Revisa los archivos del repositorio (adjuntos o en el enlace) y audita:
1. Exactitud técnica: Navidrome en Docker, volúmenes, ND_MUSICFOLDER, Tailscale, Mopidy,
   beets, Picard, ListenBrainz, Docker Desktop en Windows.
2. Los scripts jamendo_descargar.py y archive_descargar.sh: errores, riesgos, licencias.
3. Seguridad: puerto 4533, repo público, secretos, acceso remoto.
4. Legalidad de cada fuente (Jamendo, Internet Archive, Live Music Archive, Free Music Archive,
   ccMixter, Musopen, Bandcamp, Radio Browser, emisoras independientes) y de copiar CDs propios.
5. Viabilidad del plan por fases y de las dependencias entre fases.
6. Qué marcas [verificar] se pueden cerrar con evidencia.
7. Propuestas de mejora: herramientas, arquitectura, orden de fases o funciones que
   harían la plataforma más completa y variada, siempre con música legal y herramientas
   de código abierto o gratuitas.

Reglas:
- No inventes datos. Si no puedes verificar algo (precios, límites, versiones, términos,
  existencia de extensiones), escribe "NO VERIFICADO" y dilo.
- Cada hallazgo debe citar el archivo y la línea o sección, y una fuente con enlace.
- No confirmes un hallazgo sin evidencia.
- No es asesoría legal; señala qué debería revisar un abogado.
- No recomiendes fuentes sin licencia.
- Para cada mejora, di si es gratis y si el proyecto la necesita ahora o después.

Formato de salida en español:
A) Tabla: ID | Severidad (Alta/Media/Baja) | Archivo y sección | Hallazgo | Evidencia (enlace) | Corrección propuesta
B) Lista de [verificar] cerrados, con la fuente.
C) Lista de [verificar] que siguen abiertos y por qué.
D) Lo que falta y no está en el plan.
E) Propuestas de mejora: tabla con Propuesta | Beneficio | Costo (dinero y esfuerzo) | Riesgo | Enlace de respaldo | Prioridad (1 a 3).
F) Veredicto: listo para empezar la fase 1 (sí/no) y por qué.
```

## Puntos que pedimos mirar con más atención
- **A01:** si Navidrome escanea `/music` sin `ND_MUSICFOLDER`. La auditoría anterior lo dejó dudoso.
- **A10:** filtro de licencia en Jamendo (NC, ND, atribución) y qué se puede hacer con cada tipo.
- **R2:** exposición del puerto `4533` en la red local.
- **Mopidy:** si existen extensiones mantenidas para Jamendo e Internet Archive.
- **Free Music Archive, ccMixter y Musopen:** si sus términos permiten descargar de forma automática.
- **Copia de CDs propios:** matiz legal por país.

## Registro de resultados
| Auditor | Fecha | Archivo | Hallazgos Alta | Media | Baja | Veredicto fase 1 |
|---|---|---|---|---|---|---|
| ChatGPT | | `docs/auditoria-chatgpt.md` | | | | |
| Gemini | | `docs/auditoria-gemini.md` | | | | |

## Después de la auditoría
1. Claude consolida ambas respuestas y marca lo que coincide y lo que se contradice.
2. Nada se cierra sin evidencia verificable.
3. Se actualizan la spec y el plan, y se pide tu aprobación antes de empezar la fase 1.
