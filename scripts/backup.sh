#!/bin/bash

# Configuration
BACKUP_DIR="/home/patadamortal/backups/experimento"
DAYS_TO_KEEP=7
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="${BACKUP_DIR}/db_backup_${TIMESTAMP}.sql"

# Create backup directory if it doesn't exist
mkdir -p "$BACKUP_DIR"

echo "Starting database backup at $(date)"

# Perform backup using pg_dump inside the container
docker exec experimento_db pg_dump -U postgres experimento_db > "$BACKUP_FILE"

if [ $? -eq 0 ]; then
    echo "Backup successfully created: $BACKUP_FILE"
    # Compress the backup
    gzip "$BACKUP_FILE"
    echo "Backup compressed: ${BACKUP_FILE}.gz"
else
    echo "Error: Database backup failed"
    exit 1
fi

# Rotate backups: delete files older than X days
find "$BACKUP_DIR" -type f -name "*.sql.gz" -mtime +$DAYS_TO_KEEP -delete
echo "Old backups cleaned up (kept last $DAYS_TO_KEEP days)"

echo "Backup process completed at $(date)"
