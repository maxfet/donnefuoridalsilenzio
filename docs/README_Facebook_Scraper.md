# 📱 Facebook Scraper per "Donne Fuori Dal Silenzio"

**Data creazione:** 13 ottobre 2025  
**Pagina Facebook:** https://www.facebook.com/donnefuoridalsilenziociampino/  
**Obiettivo:** Scaricare e archiviare post e media dalla pagina Facebook

---

## 🎯 **Funzionalità**

### **📥 Download Automatico:**
- **Testo dei post** con timestamp e metadati
- **Immagini** dai post (JPG, PNG, etc.)
- **Video** dai post (MP4, etc.)
- **Reazioni, commenti, condivisioni** (conteggi)
- **Link esterni** condivisi nei post

### **💾 Archiviazione:**
- **Formato JSON** strutturato per ogni post
- **File media** scaricati in cartella locale
- **Metadati completi** per ogni elemento
- **Log dettagliati** di tutte le operazioni

---

## �️ **Setup e Installazione**

### **1️⃣ Prerequisiti**
```bash
# Python 3.8+ richiesto
python3 --version

# Pip aggiornato
pip install --upgrade pip
```

### **2️⃣ Installazione Dipendenze**
```bash
# Naviga nella cartella del progetto
cd /path/to/donnefuoridalsilenzio

# Installa requirements
pip install -r requirements.txt
```

---

## 🚀 **Utilizzo**

### **🔄 Esecuzione Manuale:**
```bash
# Naviga nella cartella scripts
cd scripts/

# Esegui scraper
python3 facebook_scraper_donnefuori.py
```

### **⏰ Esecuzione Programmata (Cron):**
```bash
# Modifica crontab
crontab -e

# Aggiungi riga per esecuzione giornaliera alle 08:00
0 8 * * * /home/massimo/mfhnas01_massimo/Progetti/Software/Donnefuoridalsilenzio/scripts/run_facebook_scraper_cron.sh

# O settimanale (ogni lunedì alle 09:00)
0 9 * * 1 /home/massimo/mfhnas01_massimo/Progetti/Software/Donnefuoridalsilenzio/scripts/run_facebook_scraper_cron.sh
```

---

## 📁 **Struttura Output**

```
Post-facebook/
├── posts.json                 # Tutti i post in formato JSON
├── summary.txt                # Riepilogo dell'ultima esecuzione
└── media/                     # Media scaricati
    ├── POST_ID_img0_20251013_095030.jpg
    ├── POST_ID_img1_20251013_095031.jpg
    └── POST_ID_video_20251013_095045.mp4
```

### **📋 Formato JSON:**
```json
{
  "page_name": "donnefuoridalsilenziociampino",
  "scraped_at": "2025-10-13T09:50:30",
  "total_posts": 25,
  "posts": [
    {
      "post_id": "123456789",
      "timestamp": "2025-10-12 15:30:00",
      "text": "Testo del post...",
      "user_id": "donnefuori",
      "username": "Donne fuori dal silenzio",
      "post_url": "https://facebook.com/...",
      "likes": 45,
      "comments": 12,
      "shares": 8,
      "reactions": {
        "like": 30,
        "love": 10,
        "care": 5
      },
      "media_files": [
        {
          "type": "image",
          "url": "https://...",
          "local_path": "media/123456789_img0_20251013_095030.jpg"
        }
      ],
      "scraped_at": "2025-10-13T09:50:35"
    }
  ]
}
```

---

## ⚙️ **Configurazione**

### **📝 File config_facebook_scraper.json:**
```json
{
  "facebook_scraper_config": {
    "page_name": "donnefuoridalsilenziociampino",
    "pages_to_scrape": 5,           // Pagine da scaricare
    "sleep_time_between_posts": 2,   // Pausa tra post (secondi)
    "download_media": true,          // Scarica immagini/video
    "max_media_size_mb": 50         // Limite dimensione file
  }
}
```

### **🎛️ Parametri Principali:**
- **pages_to_scrape:** Numero pagine Facebook (2-10 post per pagina)
- **sleep_time:** Pausa per evitare rate limiting
- **download_media:** true/false per scaricare media
- **max_media_size_mb:** Limite dimensioni file

---

## 📊 **Monitoraggio**

### **📈 Log Files:**
- **facebook_scraper.log** - Log dettagliato delle operazioni
- **cron_facebook_scraper.log** - Log delle esecuzioni programmate

### **🔍 Controlli:**
```bash
# Ultimi log
tail -f facebook_scraper.log

# Statistiche directory
ls -la Post-facebook/
find Post-facebook/media -type f | wc -l

# Verifica JSON
python3 -m json.tool Post-facebook/posts.json | head -20
```

---

## ⚠️ **Limitazioni e Note**

### **🚧 Limitazioni Facebook:**
- **Rate limiting:** Facebook limita richieste troppo frequenti
- **Contenuti privati:** Solo post pubblici accessibili
- **Cambiamenti API:** Facebook cambia spesso struttura
- **IP blocking:** Possibile blocco temporaneo con troppe richieste

### **💡 Buone Pratiche:**
- **Esecuzione moderata:** Non più di 1-2 volte al giorno
- **Pausa tra richieste:** Minimo 2 secondi
- **Backup regolari:** Copia periodica dei dati
- **Monitoring:** Controlla log per errori

### **🔧 Troubleshooting:**
```bash
# Se facebook-scraper non funziona
pip install --upgrade facebook-scraper

# Se timeout su media grandi
# Aumenta request_timeout in config

# Se troppi errori 429 (rate limit)
# Aumenta sleep_time o riduci pages_to_scrape
```

---

## 📞 **Supporto**

### **🔗 Risorse:**
- **facebook-scraper docs:** https://github.com/kevinzg/facebook-scraper
- **Pagina Facebook:** https://www.facebook.com/donnefuoridalsilenziociampino/

### **📧 Contatti:**
- **Tecnico:** massimo.fettucciari@libero.it
- **Organizzazione:** donnefuoridalsilenzio@gmail.com

---

**📅 Ultimo aggiornamento:** 13 ottobre 2025  
**🔧 Versione script:** 1.0