# Escaneo de vulnerabilidades de la imagen de Navidrome (2026-11-09)

Herramienta: Trivy (imagen oficial `ghcr.io/aquasecurity/trivy`), solo vulnerabilidades, severidad HIGH y CRITICAL, base de datos del día. Imagen: `deluan/navidrome:0.64.2` (Alpine 3.22.6). Escaneo estático: **un hallazgo indica que el componente está presente, no que se pueda explotar aquí.**

## Resultado
| Parte | HIGH | CRITICAL | Sin corrección disponible |
|---|---|---|---|
| Paquetes de Alpine (curl, libcurl, libexpat, musl, pcre2, zlib) | 22 | 0 | 0 |
| Binario de Navidrome (`golang.org/x/net`, biblioteca estándar de Go) | 6 | 0 | 0 |
| **Total** | **28** | **0** | **0** |

## Comparación de versiones
- `latest` y `0.64.2` tienen el **mismo digest**: son la misma imagen. Resultado idéntico al escanear ambas.
- `0.64.2` (2026-09-24) es la etiqueta numérica más reciente.
- Existe una etiqueta `develop` actualizada el 2026-11-08. No es estable y **no se escaneó ni se recomienda**.
- Conclusión: hoy no hay una versión estable que corrija estos hallazgos. Las correcciones existen en sus proyectos de origen (Alpine y Go) pero la imagen no se ha reconstruido con ellas.

## Cómo se interpreta en este proyecto
- Navidrome se publica solo en `127.0.0.1` y se alcanza por Tailscale; el uso es de una sola persona. Eso reduce la exposición, pero no la elimina.
- Que `curl` y `libcurl` estén en la imagen no significa que el servidor los use. **NO VERIFICADO** qué componentes ejecuta Navidrome en ese contenedor.
- Los hallazgos del binario (`x/net`, biblioteca estándar) sí afectan al propio servidor, aunque la exposición sea limitada.

## Decisión propuesta (a confirmar por el propietario)
1. Fijar `0.64.2`, la más reciente estable; no usar `latest`.
2. Mantener el puerto solo en `127.0.0.1` y el acceso por Tailscale.
3. **Volver a escanear antes de cada actualización** y antes de la fase 1B (la nube); si sale una versión nueva, comparar antes de cambiar.
4. No exponer el puerto a Internet ni abrirlo en el router.

Fijación opcional por digest (más estricta que la etiqueta): `deluan/navidrome@sha256:38dc2727bfcfd5ede290f8ada114fc90368146f265ae4701ddddbcbe2a44ee52`

## Cómo repetir el escaneo
```powershell
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock ghcr.io/aquasecurity/trivy:latest image --scanners vuln --severity HIGH,CRITICAL deluan/navidrome:0.64.2
```
En Windows con Docker Desktop el acceso al socket puede requerir otra forma **[verificar]**. El plugin "Docker Image Scan" del catálogo hace lo mismo.
