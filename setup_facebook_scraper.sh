#!/bin/bash
# Setup script per Facebook Scraper - Donne Fuori Dal Silenzio
# Data: 13 ottobre 2025

echo "🔧 Setup Facebook Scraper per Donne Fuori Dal Silenzio"
echo "======================================================="

# Controlla se Python3 è installato
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 non trovato. Installalo prima di continuare."
    exit 1
fi

echo "✅ Python3 trovato: $(python3 --version)"

# Controlla se pip è installato
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 non trovato. Installalo prima di continuare."
    exit 1
fi

echo "✅ pip3 trovato"

# Crea virtual environment (opzionale ma raccomandato)
echo "📦 Creando virtual environment..."
if [ ! -d "venv_facebook" ]; then
    python3 -m venv venv_facebook
    echo "✅ Virtual environment creato"
else
    echo "✅ Virtual environment già esistente"
fi

# Attiva virtual environment
echo "🔄 Attivando virtual environment..."
source venv_facebook/bin/activate

# Aggiorna pip
echo "⬆️  Aggiornando pip..."
pip install --upgrade pip

# Installa dipendenze
echo "📥 Installando dipendenze da requirements_facebook.txt..."
pip install -r requirements_facebook.txt

# Verifica installazione
echo "🔍 Verificando installazione..."
python3 -c "import facebook_scraper; print('✅ facebook-scraper installato correttamente')"
python3 -c "import requests; print('✅ requests installato correttamente')"

# Crea directory di output se non esiste
echo "📁 Creando directory di output..."
mkdir -p Post-facebook/media

echo ""
echo "🎉 Setup completato con successo!"
echo ""
echo "📋 Per utilizzare lo scraper:"
echo "   1. Attiva virtual environment: source venv_facebook/bin/activate"
echo "   2. Esegui scraper: python3 facebook_scraper_donnefuori.py"
echo ""
echo "📁 I post verranno salvati in: ./Post-facebook/"
echo "🖼️  Le immagini/video in: ./Post-facebook/media/"
echo ""
echo "⚠️  NOTA: Facebook può limitare il numero di richieste."
echo "   Se ricevi errori, riduci il numero di pagine o aumenta sleep_time."
echo ""