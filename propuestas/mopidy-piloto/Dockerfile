# PILOTO, no activo. Mopidy 4 necesita Python 3.13: Debian trixie lo trae.
# En el entorno donde se probó hizo falta un certificado de proxy propio (PIP_CERT);
# en un equipo normal no hace falta y esa línea se omite.
FROM debian:trixie-slim
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends python3 python3-venv python3-pip python3-gi gir1.2-gstreamer-1.0 gir1.2-gst-plugins-base-1.0 gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-tools ca-certificates curl && rm -rf /var/lib/apt/lists/*
RUN python3 -m venv --system-site-packages /opt/mop && /opt/mop/bin/pip install --no-cache-dir mopidy==4.0.5 mopidy-internetarchive==4.0.1
