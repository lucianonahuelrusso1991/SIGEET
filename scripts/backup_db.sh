#!/bin/bash
# SIGES Automated Backup Script (Local + Telegram)

# Rutas y Variables
APP_DIR="/opt/sigeet"
BACKUP_DIR="/opt/sigeet/backups"
DB_USER="sigeet_user"
DB_NAME="sigeet_db"
DATE=$(date +"%Y-%m-%d_%H-%M-%S")
FILE_NAME="siges_db_backup_$DATE.sql.gz"

# --- CONFIGURACION DE TELEGRAM ---
# Reemplaza estas variables con tus datos
TELEGRAM_BOT_TOKEN="TU_TOKEN_AQUI"
TELEGRAM_CHAT_ID="TU_CHAT_ID_AQUI"

echo "=================================================="
echo "Iniciando Backup de SIGES - $DATE"
echo "=================================================="

# 1. Crear directorio local de backups si no existe
mkdir -p "$BACKUP_DIR"
cd "$APP_DIR" || exit 1

# 2. Generar dump local y comprimir
echo "[1/3] Generando dump de PostgreSQL desde Docker..."
docker compose exec -T db pg_dump -U $DB_USER $DB_NAME | gzip > "$BACKUP_DIR/$FILE_NAME"

if [ -f "$BACKUP_DIR/$FILE_NAME" ]; then
    echo " > Backup local creado exitosamente: $FILE_NAME"
else
    echo " > ERROR: Fallo la creacion del backup local."
    exit 1
fi

# 3. Limpieza: Borrar backups locales de mas de 7 dias
echo "[2/3] Limpiando backups antiguos (mas de 7 dias)..."
find "$BACKUP_DIR" -type f -name "*.sql.gz" -mtime +7 -delete

# 4. Enviar a Telegram
echo "[3/3] Enviando backup a Telegram..."
if [ "$TELEGRAM_BOT_TOKEN" != "TU_TOKEN_AQUI" ]; then
    curl -s -F document=@"$BACKUP_DIR/$FILE_NAME" "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/sendDocument?chat_id=$TELEGRAM_CHAT_ID" > /dev/null
    echo " > Backup enviado a Telegram exitosamente."
else
    echo " > ADVERTENCIA: Telegram no configurado. Solo se guardo el backup local."
fi

echo "=================================================="
echo "Backup finalizado exitosamente a las $(date +"%H:%M:%S")"
echo "=================================================="
