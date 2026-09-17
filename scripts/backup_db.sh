#!/bin/bash
# SIGES Automated Backup Script (Local + Correo Electronico)

# Rutas y Variables
APP_DIR="/opt/sigeet"
BACKUP_DIR="/opt/sigeet/backups"
DB_USER="sigeet_user"
DB_NAME="sigeet_db"
DATE=$(date +"%Y-%m-%d_%H-%M-%S")
FILE_NAME="siges_db_backup_$DATE.sql.gz"

echo "=================================================="
echo "Iniciando Backup de SIGES - $DATE"
echo "=================================================="

# 1. Crear directorio local de backups si no existe
mkdir -p "$BACKUP_DIR"
cd "$APP_DIR" || exit 1

# 2. Generar dump local y comprimir (Estrategia 1)
echo "[1/3] Generando dump de PostgreSQL desde Docker..."
docker compose exec -T db pg_dump -U $DB_USER $DB_NAME | gzip > "$BACKUP_DIR/$FILE_NAME"

if [ -f "$BACKUP_DIR/$FILE_NAME" ]; then
    echo " > Backup local creado exitosamente: $FILE_NAME"
else
    echo " > ERROR: Fallo la creacion del backup local."
    exit 1
fi

# 3. Limpieza: Borrar backups locales de mas de 7 dias (Estrategia 1)
echo "[2/3] Limpiando backups antiguos (mas de 7 dias)..."
find "$BACKUP_DIR" -type f -name "*.sql.gz" -mtime +7 -delete

# 4. Enviar por Correo Electronico (Estrategia 2)
echo "[3/3] Enviando backup por correo electronico..."
# Llama a un script de Python que se encarga de mandar el mail con el adjunto
python3 /opt/sigeet/scripts/send_email_backup.py "$BACKUP_DIR/$FILE_NAME"

echo "=================================================="
echo "Backup finalizado exitosamente a las $(date +"%H:%M:%S")"
echo "=================================================="
