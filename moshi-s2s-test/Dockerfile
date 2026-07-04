FROM nvidia/cuda:12.4.1-cudnn-runtime-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python3-venv \
    ffmpeg \
    git \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install --upgrade pip setuptools wheel

# Moshi package + runtime utilities (pinned for reproducible builds).
RUN python3 -m pip install \
    moshi==0.2.13 \
    'huggingface_hub[cli]==1.21.0'

WORKDIR /app

COPY scripts/run-local.sh /app/scripts/run-local.sh
RUN chmod +x /app/scripts/run-local.sh

EXPOSE 8000 7860

CMD ["/app/scripts/run-local.sh"]
