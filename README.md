# Progetto Donne Fuori Dal Silenzio

Questo repository contiene tutti gli strumenti, documentazione e script per la gestione del sito web e dei contenuti social di "Donne Fuori Dal Silenzio".

## Struttura del Progetto

```
📁 docs/                     # 📚 Documentazione completa
├── Documentazione_Sito_DonneFuoriDalSilenzio.md
├── Documentazione_Tecnica_Manutenzione.md
├── Documentazione_Tecnica_Facebook_Scraper.md
├── Guida_Clonazione_QNAP.md
├── Guida_Clonazione_Sito_Locale.md
├── Configurazioni_dfds_maxfet_cloud.md
├── QNAP_mfh-nas01_config.md
└── README_Facebook_Scraper.md

📁 scripts/                  # 🐍 Script Python e automazione
├── facebook_scraper_donnefuori.py
├── run_facebook_scraper_cron.sh
└── setup_facebook_scraper.sh

📁 config/                   # ⚙️ File di configurazione
├── facebook_scraper_config.py
├── config_facebook_scraper.json
└── QNAP-staging-data

📁 Post-facebook/            # 📄 Dati scaricati da Facebook (JSON)

📄 requirements.txt          # 📦 Dipendenze Python
📄 workspace.donnefuoridalsilenzio.code-workspace
```

## Componenti Principali

### 🌐 Sito Web WordPress
- **Produzione**: Hosting cloud standard
- **Test/Staging**: Server QNAP locale con MariaDB
- **Tema**: Divi 4.27.4
- **Database**: MariaDB 10.5.8 (porta 3307)

### 🔧 Facebook Scraper
- Scraping automatico dei post dalla pagina Facebook
- Salvataggio dati in formato JSON
- Download automatico di media (immagini/video)
- Esecuzione schedulata via cron

### 📋 Documentazione
- Guide complete per setup, manutenzione e clonazione
- Configurazioni specifiche per QNAP
- Procedure tecniche dettagliate

## Quick Start

### Setup Facebook Scraper
```bash
# Installa dipendenze
pip install -r requirements.txt

# Esegui setup iniziale
./scripts/setup_facebook_scraper.sh

# Avvia scraping manuale
cd scripts/
python facebook_scraper_donnefuori.py
```

### Clonazione Sito su QNAP
1. Consultare `docs/Guida_Clonazione_QNAP.md`
2. Configurare MariaDB come da `docs/QNAP_mfh-nas01_config.md`
3. Utilizzare Duplicator per la migrazione

## Tecnologie

- **Backend**: WordPress 6.6.3, PHP 8.2, MariaDB 10.5.8
- **Frontend**: Divi Theme, CSS personalizzato
- **Automazione**: Python 3, facebook-scraper, bash scripts
- **Infrastruttura**: QNAP NAS, Web Station
- **Version Control**: Git

## Contribuzione

Per modifiche o aggiornamenti:
1. Consultare la documentazione in `docs/`
2. Testare sempre su ambiente QNAP di staging
3. Aggiornare la documentazione correlata
4. Commit con messaggi descrittivi

---
*Ultimo aggiornamento: 13 ottobre 2025*