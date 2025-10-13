#!/bin/bash
# Script per esecuzione programmata del Facebook Scraper
# Da usare con cron per automatizzare il download
# Data: 13 ottobre 2025

# Configurazione
SCRIPT_DIR="/home/massimo/mfhnas01_massimo/Progetti/Software/Donnefuoridalsilenzio"
VENV_PATH="$SCRIPT_DIR/venv_facebook"
PYTHON_SCRIPT="$SCRIPT_DIR/facebook_scraper_donnefuori.py"
LOG_FILE="$SCRIPT_DIR/cron_facebook_scraper.log"

# Funzione di logging
log_message() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

# Cambio directory
cd "$SCRIPT_DIR" || {
    log_message "ERRORE: Impossibile accedere alla directory $SCRIPT_DIR"
    exit 1
}

log_message "=== INIZIO ESECUZIONE PROGRAMMATA FACEBOOK SCRAPER ==="

# Attiva virtual environment
if [ -d "$VENV_PATH" ]; then
    source "$VENV_PATH/bin/activate"
    log_message "Virtual environment attivato"
else
    log_message "ERRORE: Virtual environment non trovato in $VENV_PATH"
    exit 1
fi

# Verifica che lo script Python esista
if [ ! -f "$PYTHON_SCRIPT" ]; then
    log_message "ERRORE: Script Python non trovato: $PYTHON_SCRIPT"
    exit 1
fi

# Esegui lo scraper
log_message "Avvio scraper Facebook..."
python3 "$PYTHON_SCRIPT" >> "$LOG_FILE" 2>&1

# Controlla esito
if [ $? -eq 0 ]; then
    log_message "✅ Scraper completato con successo"
    
    # Conta i file nella directory Post-facebook
    if [ -d "Post-facebook" ]; then
        POST_COUNT=$(find Post-facebook -name "*.json" | wc -l)
        MEDIA_COUNT=$(find Post-facebook/media -type f 2>/dev/null | wc -l)
        log_message "📊 Statistiche: $POST_COUNT file JSON, $MEDIA_COUNT file media"
    fi
    
else
    log_message "❌ Errore durante l'esecuzione dello scraper"
fi

# Pulizia file vecchi (opzionale) - mantieni solo ultimi 30 giorni
find Post-facebook -name "*.json" -mtime +30 -delete 2>/dev/null
find Post-facebook/media -type f -mtime +30 -delete 2>/dev/null

log_message "=== FINE ESECUZIONE PROGRAMMATA ==="
log_message ""

# Deattiva virtual environment
deactivate