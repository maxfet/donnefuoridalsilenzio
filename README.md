# Progetto Donne Fuori Dal Silenzio - Facebook Scraper

Strumenti per l'archiviazione automatica dei contenuti pubblici dalla pagina Facebook "Donne Fuori Dal Silenzio Ciampino".

**Ultimo aggiornamento:** 6 novembre 2025

## 📋 Descrizione

Questo progetto fornisce diversi metodi per scaricare e archiviare i post pubblici dalla pagina Facebook dell'associazione, con lo scopo di:
- 📚 Preservare la memoria storica delle attività
- 💾 Creare backup dei contenuti pubblicati
- 📊 Organizzare i dati in formato strutturato (JSON)

## Struttura del Progetto

```
📁 docs/                     # 📚 Documentazione completa
├── Documentazione_Tecnica_Facebook_Scraper.md
├── Stato_Progetto_Facebook_Scraper.md
├── Privacy_Policy.md
└── README_Facebook_Scraper.md

📁 scripts/                  # 🐍 Script Python
├── facebook_scraper_donnefuori.py    # Scraper con cookies
├── facebook_graph_scraper.py         # Scraper Graph API
├── simple_facebook_scraper.py        # Scraper alternativo
└── [guide e test vari]

📁 config/                   # ⚙️ File di configurazione
├── facebook_cookies_template.json
├── facebook_graph_token_template.txt
└── facebook_page_id_template.txt

📁 Post-facebook/            # 📄 Dati scaricati (JSON)

📄 requirements.txt          # 📦 Dipendenze Python
📄 privacy.html             # Privacy Policy (GitHub Pages)
📄 index.html               # Homepage progetto
```

## Componenti Principali

### 🔧 Facebook Scraper
- Scraping automatico dei post dalla pagina Facebook
- **Stato:** In sviluppo - limitazioni tecniche Facebook 2025
- Metodi implementati:
  - facebook-scraper con cookies (limitato da anti-scraping)
  - Graph API con token (richiede App Review)
  - Scraper alternativo requests-based
- Salvataggio dati in formato JSON
- Download automatico di media (immagini/video)
- Esecuzione schedulata via cron (quando funzionante)

**Limitazioni attuali:**
- Facebook ha rafforzato protezioni anti-scraping
- Graph API richiede permission `pages_read_engagement`
- Permission richiedono App Review Facebook (2-4 settimane)
- Framework pronto per quando le API saranno disponibili

### 📋 Documentazione
- Guide complete per setup e configurazione
- Privacy Policy per App Review Facebook
- Stato progetto e next steps

## Quick Start

### Setup Facebook Scraper
```bash
# Installa dipendenze
pip install -r requirements.txt

# Configura token Graph API
echo "YOUR_TOKEN" > config/facebook_graph_token.txt
echo "100066348746548" > config/facebook_page_id.txt

# Esegui scraper
cd scripts/
python facebook_graph_scraper.py
```

### Metodi Alternativi
Consulta la documentazione in `docs/` per:
- Setup con cookies (facebook-scraper)
- Configurazione Graph API
- Richiesta App Review Facebook

## Tecnologie

- **Python 3.8+**: facebook-scraper, requests, beautifulsoup4
- **Facebook Graph API**: API ufficiale per accesso dati
- **GitHub Pages**: Hosting Privacy Policy

## Contribuzione

Per modifiche o aggiornamenti:
1. Consultare la documentazione in `docs/`
2. Testare le modifiche localmente
3. Aggiornare la documentazione correlata
4. Commit con messaggi descrittivi

## Links

- **Privacy Policy**: https://maxfet.github.io/donnefuoridalsilenzio/privacy.html
- **Pagina Facebook**: https://www.facebook.com/donnefuoridalsilenziociampino
- **Repository**: https://github.com/maxfet/donnefuoridalsilenzio

---
*Ultimo aggiornamento: 6 novembre 2025*