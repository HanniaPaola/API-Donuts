#!/bin/bash
set -euo pipefail

# MySQL datos persistentes (volumen Fly montado en /data)
DATADIR=/data/mysql
RUNDIR=/run/mysqld
SOCKET="${RUNDIR}/mysqld.sock"

mkdir -p "$DATADIR" "$RUNDIR"
chown -R mysql:mysql "$DATADIR" "$RUNDIR"

: "${DB_NAME:?Definir DB_NAME}"
: "${DB_USER:?Definir DB_USER}"
: "${DB_PASSWORD:?Definir DB_PASSWORD}"

if [ ! -f "${DATADIR}/ibdata1" ] && [ ! -d "${DATADIR}/mysql" ]; then
  echo "[entrypoint] Inicializando MariaDB en ${DATADIR}..."
  mariadb-install-db --user=mysql --datadir="$DATADIR" >/dev/null
fi

echo "[entrypoint] Arrancando MariaDB..."
mariadbd \
  --user=mysql \
  --datadir="$DATADIR" \
  --bind-address=127.0.0.1 \
  --skip-name-resolve \
  --socket="$SOCKET" &
MYSQLD_PID=$!

for _ in $(seq 1 90); do
  if mysqladmin ping -S "$SOCKET" -u root --silent 2>/dev/null; then
    break
  fi
  if ! kill -0 "$MYSQLD_PID" 2>/dev/null; then
    echo "[entrypoint] mariadbd terminó inesperadamente"
    exit 1
  fi
  sleep 1
done

echo "[entrypoint] Creando base y usuario de aplicación (idempotente)..."
mysql -u root -S "$SOCKET" -e "
CREATE DATABASE IF NOT EXISTS \`${DB_NAME}\`;
CREATE USER IF NOT EXISTS '${DB_USER}'@'127.0.0.1' IDENTIFIED BY '${DB_PASSWORD}';
GRANT ALL PRIVILEGES ON \`${DB_NAME}\`.* TO '${DB_USER}'@'127.0.0.1';
FLUSH PRIVILEGES;
"

export DB_HOST="${DB_HOST:-127.0.0.1}"
export DB_PORT="${DB_PORT:-3306}"

LISTEN_PORT="${PORT:-8000}"
echo "[entrypoint] Arrancando Uvicorn en 0.0.0.0:${LISTEN_PORT}..."

/venv/bin/uvicorn main:app --host 0.0.0.0 --port "$LISTEN_PORT" &
UV_PID=$!

shutdown() {
  echo "[entrypoint] Señal recibida, deteniendo..."
  kill "$UV_PID" 2>/dev/null || true
  kill "$MYSQLD_PID" 2>/dev/null || true
  wait "$UV_PID" 2>/dev/null || true
  wait "$MYSQLD_PID" 2>/dev/null || true
  exit 0
}
trap shutdown SIGTERM SIGINT

wait "$UV_PID"
