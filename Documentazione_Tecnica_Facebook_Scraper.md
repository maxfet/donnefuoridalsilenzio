# 🔧 Documentazione Tecnica - Facebook Scraper

**Progetto:** Facebook Scraper per "Donne Fuori Dal Silenzio"  
**Data:** 13 ottobre 2025  
**Versione:** 1.0

---

## 🏗️ **Architettura del Sistema**

### **📁 File del Progetto:**
```
/home/massimo/mfhnas01_massimo/Progetti/Software/Donnefuoridalsilenzio/
├── facebook_scraper_donnefuori.py     # Script principale
├── config_facebook_scraper.json       # Configurazione
├── requirements_facebook.txt          # Dipendenze Python
├── setup_facebook_scraper.sh          # Setup automatico
├── run_facebook_scraper_cron.sh       # Wrapper per cron
├── venv_facebook/                     # Virtual environment
└── Post-facebook/                     # Directory output
    ├── posts.json                     # Dati scaricati
    ├── summary.txt                    # Riepilogo
    └── media/                         # File media
```

### **🐍 Dipendenze Python:**
```python
facebook-scraper>=3.0.0    # Libreria principale scraping
requests>=2.31.0           # Download HTTP
pathlib                    # Gestione percorsi (built-in)
datetime                   # Timestamp (built-in)
json                       # Parsing JSON (built-in)
logging                    # Sistema logging (built-in)
```

---

## 🔍 **Analisi del Codice**

### **📦 Classe DonneFuoriScraper:**

#### **🔧 Metodi Principali:**

1. **`__init__(self, config_file)`**
   - Carica configurazione da JSON
   - Inizializza logging
   - Crea directory output

2. **`download_media(self, media_url, post_id, media_type, index)`**
   - Scarica immagini/video da URL
   - Gestisce timeout e errori HTTP
   - Salva con naming convention strutturato
   - Verifica dimensioni file

3. **`scrape_posts(self)`**
   - Utilizza facebook-scraper per ottenere post
   - Itera attraverso pagine specificate
   - Estrae metadati completi per ogni post
   - Gestisce rate limiting con sleep

4. **`save_data(self, posts)`**
   - Salva dati in formato JSON strutturato
   - Crea file summary.txt con statistiche
   - Gestisce encoding UTF-8
   - Backup dati esistenti

#### **🛡️ Gestione Errori:**
```python
try:
    # Operazione critica
except facebook_scraper.exceptions.FacebookScraperException as e:
    # Errori specifici facebook-scraper
except requests.exceptions.RequestException as e:
    # Errori di rete/HTTP
except Exception as e:
    # Errori generici
finally:
    # Cleanup sempre eseguito
```

### **📊 Struttura Dati Output:**
```python
post_data = {
    "post_id": str,           # ID univoco Facebook
    "timestamp": str,         # Data/ora post (YYYY-MM-DD HH:MM:SS)
    "text": str,              # Contenuto testuale
    "user_id": str,           # ID utente/pagina
    "username": str,          # Nome visualizzato
    "post_url": str,          # URL completo post
    "likes": int,             # Numero like
    "comments": int,          # Numero commenti
    "shares": int,            # Numero condivisioni
    "reactions": dict,        # Dettaglio reazioni
    "media_files": list,      # Lista file media
    "scraped_at": str         # Timestamp scraping
}
```

---

## ⚙️ **Configurazione Sistema**

### **🔧 File config_facebook_scraper.json:**
```json
{
  "facebook_scraper_config": {
    "page_name": "donnefuoridalsilenziociampino",
    "pages_to_scrape": 5,
    "sleep_time_between_posts": 2,
    "download_media": true,
    "max_media_size_mb": 50,
    "output_directory": "Post-facebook",
    "request_timeout": 30,
    "user_agent": "Mozilla/5.0 (compatible; DonneFuoriScraper/1.0)"
  }
}
```

#### **📋 Parametri di Configurazione:**

| Parametro | Tipo | Default | Descrizione |
|-----------|------|---------|-------------|
| `page_name` | string | - | Nome pagina Facebook (obbligatorio) |
| `pages_to_scrape` | int | 5 | Numero pagine da scaricare (2-10 post/pagina) |
| `sleep_time_between_posts` | int | 2 | Pausa tra post in secondi (min 1) |
| `download_media` | bool | true | Scarica immagini/video |
| `max_media_size_mb` | int | 50 | Limite dimensione file in MB |
| `output_directory` | string | "Post-facebook" | Directory output |
| `request_timeout` | int | 30 | Timeout richieste HTTP in secondi |
| `user_agent` | string | - | User-Agent per richieste HTTP |

---

## 🔄 **Workflow di Esecuzione**

### **📋 Processo Principale:**

1. **Inizializzazione:**
   ```python
   # Carica configurazione
   # Verifica directory output
   # Inizializza logging
   # Controlla connessione
   ```

2. **Scraping Facebook:**
   ```python
   # Per ogni pagina da scaricare:
   #   - Richiesta a Facebook
   #   - Parse HTML/JSON
   #   - Estrazione metadati
   #   - Sleep anti-rate-limit
   ```

3. **Download Media:**
   ```python
   # Per ogni media trovato:
   #   - Verifica URL valido
   #   - Download con timeout
   #   - Controllo dimensioni
   #   - Salvataggio locale
   ```

4. **Salvataggio Dati:**
   ```python
   # Backup dati esistenti
   # Merge nuovi post con esistenti
   # Salvataggio JSON finale
   # Creazione summary
   ```

### **⏱️ Timing e Performance:**

- **Tempo per post:** 2-5 secondi (con media)
- **Pagina Facebook:** ~30-60 secondi per 10 post
- **Rate limiting:** Pausa obbligatoria 2+ secondi
- **Dimensioni output:** 5-50MB per sessione (con media)

---

## 🔐 **Sicurezza e Limitazioni**

### **🛡️ Misure di Sicurezza:**

1. **Rate Limiting:**
   - Sleep minimo 2 secondi tra post
   - Timeout su richieste lunghe
   - Retry automatico con backoff

2. **Gestione Errori:**
   - Try/catch su tutte le operazioni critiche
   - Logging dettagliato di errori
   - Fallback su errori di rete

3. **Validazione Input:**
   - Controllo format URL
   - Validazione dimensioni file
   - Sanificazione nomi file

### **⚠️ Limitazioni Facebook:**

1. **API Restrictions:**
   - Nessuna API ufficiale gratuita
   - Scraping soggetto a ToS Facebook
   - Possibili cambiamenti struttura HTML

2. **Rate Limiting:**
   - Max ~100 richieste/ora per IP
   - Blocco temporaneo se troppe richieste
   - Necessario rispettare delays

3. **Contenuti Accessibili:**
   - Solo post pubblici
   - No contenuti protetti
   - Dipende da privacy settings

---

## 🔍 **Troubleshooting**

### **❌ Problemi Comuni:**

#### **1. ModuleNotFoundError: 'facebook_scraper'**
```bash
# Soluzione:
source venv_facebook/bin/activate
pip install -r requirements_facebook.txt
```

#### **2. Timeout su richieste**
```json
// Aumenta timeout in config:
"request_timeout": 60
```

#### **3. Too Many Requests (429)**
```json
// Aumenta sleep time:
"sleep_time_between_posts": 5
// Riduci pagine:
"pages_to_scrape": 2
```

#### **4. No posts found**
```bash
# Verifica connessione:
ping facebook.com

# Verifica nome pagina:
curl -s "https://www.facebook.com/donnefuoridalsilenziociampino/"
```

#### **5. Permission denied su directory**
```bash
# Fix permessi:
chmod 755 Post-facebook/
chmod 644 Post-facebook/*
```

### **🔧 Debug Commands:**

```bash
# Test connessione Facebook
python3 -c "
import facebook_scraper
posts = list(facebook_scraper.get_posts('donnefuoridalsilenziociampino', pages=1))
print(f'Found {len(posts)} posts')
"

# Verifica configurazione
python3 -c "
import json
with open('config_facebook_scraper.json') as f:
    config = json.load(f)
print(json.dumps(config, indent=2))
"

# Test download singolo post
python3 -c "
from facebook_scraper_donnefuori import DonneFuoriScraper
scraper = DonneFuoriScraper('config_facebook_scraper.json')
# Test con pages=1
"
```

---

## 📈 **Monitoraggio e Manutenzione**

### **📊 Metriche da Monitorare:**

1. **Performance:**
   - Tempo esecuzione script
   - Numero post scaricati
   - Dimensioni file output
   - Errori di rete

2. **Health Check:**
   - Presenza file output
   - Validità JSON
   - Completezza download media
   - Log errori

### **🔧 Manutenzione Programmata:**

#### **📅 Settimanale:**
- Controllo log errori
- Verifica spazio disco
- Backup dati Post-facebook/

#### **📅 Mensile:**
- Update facebook-scraper library
- Pulizia log vecchi
- Controllo performance

#### **📅 Quando Necessario:**
- Fix breaking changes Facebook
- Update User-Agent string
- Ottimizzazione parametri config

### **🏗️ Script di Manutenzione:**

```bash
#!/bin/bash
# maintenance_facebook_scraper.sh

echo "🔧 Manutenzione Facebook Scraper"

# Backup dati
cp -r Post-facebook/ "Post-facebook-backup-$(date +%Y%m%d)"

# Update dipendenze
source venv_facebook/bin/activate
pip install --upgrade facebook-scraper requests

# Pulizia log vecchi
find . -name "*.log" -mtime +30 -delete

# Health check
python3 -c "
import json
with open('Post-facebook/posts.json') as f:
    data = json.load(f)
print(f'✅ {len(data.get(\"posts\", []))} post in archivio')
"

echo "✅ Manutenzione completata"
```

---

## 📝 **Changelog e Versioning**

### **v1.0 (13 ottobre 2025):**
- ✅ Implementazione iniziale
- ✅ Scraping post Facebook
- ✅ Download media automatico
- ✅ Output JSON strutturato
- ✅ Sistema logging completo
- ✅ Script setup e automazione
- ✅ Documentazione completa

### **🔮 Roadmap Future:**
- **v1.1:** Gestione commenti post
- **v1.2:** Export in formato CSV
- **v1.3:** Dashboard web per visualizzazione
- **v1.4:** Integrazione database MySQL
- **v1.5:** API REST per accesso dati

---

**👨‍💻 Sviluppatore:** Massimo Fettucciari  
**📧 Supporto:** massimo.fettucciari@libero.it  
**📅 Ultima modifica:** 13 ottobre 2025