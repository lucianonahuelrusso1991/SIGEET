#!/bin/bash
# SIGES Automated Backup Script (Local + Google Drive)
# Se recomienda ejecutar este script mediante Cron todos los dias a las 03:00 AM

# Rutas y Variables
APP_DIR="/opt/sigeet"
BACKUP_DIR="/opt/sigeet/backups"
DB_USER="sigeet_user"
DB_NAME="sigeet_db"
DATE=$(date +"%Y-%m-%d_%H-%M-%S")
FILE_NAME="siges_db_backup_$DATE.sql.gz"
RCLONE_REMOTE="gdrive:SIGES_Backups" # Nombre de la conexion en rclone

echo "=================================================="
echo "Iniciando Backup de SIGES - $DATE"
echo "=================================================="

# 1. Crear directorio local de backups si no existe
mkdir -p "$BACKUP_DIR"
cd "$APP_DIR" || exit 1

# 2. Estrategia 1: Generar dump local y comprimir
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

# 4. Estrategia 2: Sincronizar a la Nube (Google Drive) via rclone
echo "[3/3] Sincronizando carpeta de backups a Google Drive..."
# 'sync' hara que en Google Drive haya exactamente lo mismo que en local (se borran los viejos tambien ahi)
rclone sync "$BACKUP_DIR" "$RCLONE_REMOTE"

echo "=================================================="
echo "Backup finalizado exitosamente a las $(date +"%H:%M:%S")"
echo "=================================================="
