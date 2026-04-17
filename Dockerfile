FROM debian:bookworm-slim

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update \
  && apt-get install -y --no-install-recommends \
    mariadb-server \
    mariadb-client \
    python3 \
    python3-venv \
    python3-dev \
    build-essential \
    libssl-dev \
    pkg-config \
    curl \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN python3 -m venv /venv \
  && /venv/bin/pip install --no-cache-dir --upgrade pip \
  && /venv/bin/pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x /app/docker-entrypoint.sh

EXPOSE 8000

ENV DB_HOST=127.0.0.1 \
    DB_PORT=3306

ENTRYPOINT ["/app/docker-entrypoint.sh"]
