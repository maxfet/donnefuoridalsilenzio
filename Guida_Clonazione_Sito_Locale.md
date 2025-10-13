# 🔧 Guida Clonazione Sito WordPress in Locale

**Sito:** donnefuoridalsilenzioaps.it  
**Obiettivo:** Creare ambiente di test locale  
**Data:** 9 ottobre 2025

---

## 🎯 Opzioni di Clonazione

### 📦 **Opzione 1: Duplicator Plugin (Consigliata)**

#### Vantaggi:
- ✅ Processo completamente automatizzato
- ✅ Include files + database in un unico pacchetto
- ✅ Gestisce automaticamente cambio URL
- ✅ Interfaccia user-friendly

#### Procedura:

**Sul sito live:**
1. Installa plugin **Duplicator** (versione gratuita sufficiente)
2. Vai su `Duplicator > Packages`
3. Clicca "Create New Package"
4. Configura esclusioni se necessario
5. Avvia la creazione del pacchetto
6. Scarica i due file generati:
   - `[nome]_archive.zip` (files del sito)
   - `installer.php` (script di installazione)

**In locale/server di test:**
1. Crea nuovo database MySQL vuoto
2. Copia i due file nella cartella web del server
3. Accedi a `https://dfds.maxfet.cloud/installer.php`
4. Segui il wizard di installazione
5. Inserisci credenziali database del server
6. Completa l'installazione

**⚠️ IMPORTANTE - Configurazioni post-installazione per dfds.maxfet.cloud:**

7. **Verifica URL nel database:**
   ```sql
   -- Controlla URL correnti
   SELECT option_name, option_value 
   FROM wp_options 
   WHERE option_name IN ('home', 'siteurl');
   
   -- Se necessario, aggiorna URL
   UPDATE wp_options 
   SET option_value = 'https://dfds.maxfet.cloud' 
   WHERE option_name = 'home';
   
   UPDATE wp_options 
   SET option_value = 'https://dfds.maxfet.cloud' 
   WHERE option_name = 'siteurl';
   ```

8. **Configura wp-config.php per ambiente test:**
   ```php
   // URL specifici per dfds.maxfet.cloud
   define('WP_HOME','https://dfds.maxfet.cloud');
   define('WP_SITEURL','https://dfds.maxfet.cloud');
   
   // Ambiente di test
   define('WP_ENVIRONMENT_TYPE', 'staging');
   define('WP_DEBUG', true);
   define('WP_DEBUG_LOG', true);
   
   // Disabilita indicizzazione sui motori di ricerca
   define('BLOG_PUBLIC', 0);
   
   // Forza HTTPS
   define('FORCE_SSL_ADMIN', true);
   if (strpos($_SERVER['HTTP_X_FORWARDED_PROTO'], 'https') !== false)
       $_SERVER['HTTPS']='on';
   ```

9. **Disabilita plugin non necessari per test:**
   ```php
   // Aggiungi a wp-config.php o functions.php del tema
   if (WP_ENVIRONMENT_TYPE === 'staging') {
       // Disabilita plugin di produzione
       add_filter('option_active_plugins', function($plugins) {
           $disable = [
               'wordfence/wordfence.php',
               'really-simple-ssl/rlrsssl-really-simple-ssl.php',
               'google-analytics-dashboard-for-wp/gadwp.php',
               'mailchimp-for-wp/mailchimp-for-wp.php'
           ];
           return array_diff($plugins, $disable);
       });
   }
   ```

10. **Configura SSL e sicurezza:**
    ```apache
    # .htaccess - Forza HTTPS
    RewriteEngine On
    RewriteCond %{HTTPS} off
    RewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]
    
    # Protezione wp-config.php
    <Files wp-config.php>
    Order allow,deny
    Deny from all
    </Files>
    
    # Blocca accesso a file sensibili
    <FilesMatch "\.(htaccess|htpasswd|ini|log|sh|sql|conf)$">
    Order allow,deny
    Deny from all
    </FilesMatch>
    ```

---

### 🛠️ **Opzione 2: Backup Manuale**

#### Cosa Scaricare:

**Files WordPress:**
```bash
# Via FTP o cPanel File Manager
- Tutta la cartella public_html/
- Inclusi .htaccess e wp-config.php
```

**Database:**
```sql
-- Via phpMyAdmin o comando MariaDB/MySQL
EXPORT DATABASE donnefuori_wp
-- Salva come file .sql

-- MariaDB preferibile per performance
-- Comando export ottimizzato:
mariadb-dump -u root -p --single-transaction --routines donnefuori_wp > backup.sql
```

#### Procedura Manuale:

1. **Scarica tutti i files** via FTP
2. **Esporta database** da phpMyAdmin
3. **Setup ambiente locale** (XAMPP/WAMP)
4. **Importa database** in MySQL locale
5. **Modifica wp-config.php:**

```php
// Credenziali database locale (MariaDB/MySQL)
define('DB_NAME', 'donnefuori_locale');
define('DB_USER', 'root');
define('DB_PASSWORD', '');
define('DB_HOST', 'localhost');

// Charset ottimizzato (importante per MariaDB)
define('DB_CHARSET', 'utf8mb4');
define('DB_COLLATE', 'utf8mb4_unicode_ci');

// Debug per ambiente locale
define('WP_DEBUG', true);
define('WP_DEBUG_LOG', true);
define('WP_ENVIRONMENT_TYPE', 'local');
```

6. **Aggiorna URL nel database:**

```sql
-- Per ambiente locale
UPDATE wp_options 
SET option_value = 'http://localhost/donnefuori' 
WHERE option_name = 'home';

UPDATE wp_options 
SET option_value = 'http://localhost/donnefuori' 
WHERE option_name = 'siteurl';

-- Per server test come dfds.maxfet.cloud
UPDATE wp_options 
SET option_value = 'https://dfds.maxfet.cloud' 
WHERE option_name IN ('home', 'siteurl');

-- Verifica aggiornamento
SELECT option_name, option_value 
FROM wp_options 
WHERE option_name IN ('home', 'siteurl');
```

---

## 🌐 Configurazione Specifica per dfds.maxfet.cloud

### **Setup Completato - Checklist Verifica**

Il sito di test è raggiungibile a: `https://dfds.maxfet.cloud`

**Verifiche necessarie dopo clonazione Duplicator:**

1. **✅ Test accesso sito:**
   ```
   URL principale: https://dfds.maxfet.cloud
   Admin WordPress: https://dfds.maxfet.cloud/wp-admin
   ```

2. **✅ Verifica configurazione database:**
   ```sql
   -- Controlla URL nel database
   SELECT option_value FROM wp_options WHERE option_name = 'home';
   SELECT option_value FROM wp_options WHERE option_name = 'siteurl';
   
   -- Dovrebbero essere: https://dfds.maxfet.cloud
   ```

3. **✅ Test funzionalità critiche:**
   - [ ] Login amministratore funzionante
   - [ ] Menu di navigazione corretto
   - [ ] Immagini caricate correttamente
   - [ ] Plugin essenziali attivi
   - [ ] Tema Divi funzionante

4. **✅ Configurazioni sicurezza per ambiente test:**
   ```php
   // wp-config.php - Verificare presenza
   define('WP_ENVIRONMENT_TYPE', 'staging');
   define('BLOG_PUBLIC', 0); // Non indicizzare sui motori
   define('WP_DEBUG', true);
   define('WP_DEBUG_LOG', true);
   ```

5. **✅ Plugin da disabilitare in test:**
   - Wordfence Security (può bloccare test)
   - Google Analytics (evita tracciamento test)
   - MailChimp (evita invii email test)
   - Backup plugins (non necessari su test)

### **Comandi Rapidi Troubleshooting dfds.maxfet.cloud**

**Se il sito non carica correttamente:**
```sql
-- Reset URL nel database
UPDATE wp_options SET option_value = 'https://dfds.maxfet.cloud' WHERE option_name = 'home';
UPDATE wp_options SET option_value = 'https://dfds.maxfet.cloud' WHERE option_name = 'siteurl';

-- Verifica template attivo
SELECT option_value FROM wp_options WHERE option_name = 'template';
SELECT option_value FROM wp_options WHERE option_name = 'stylesheet';
```

**Se le immagini non caricano:**
```sql
-- Aggiorna path uploads
UPDATE wp_options 
SET option_value = 'https://dfds.maxfet.cloud/wp-content/uploads' 
WHERE option_name = 'upload_path';
```

**Se i plugin causano errori:**
```php
// Disabilita tutti i plugin temporaneamente
// In wp-config.php aggiungi:
define('WP_DEBUG', true);
define('WP_DEBUG_DISPLAY', false);
define('WP_DEBUG_LOG', true);

// Poi riattiva uno per uno per identificare problemi
```

### **Workflow Sincronizzazione dfds.maxfet.cloud ↔ Produzione**

**Da Produzione a Test (Aggiornamento ambiente test):**
1. Crea nuovo pacchetto Duplicator su donnefuoridalsilenzioaps.it
2. Scarica e carica su dfds.maxfet.cloud
3. Esegui installer sovrascrivendo installation esistente
4. Verifica URL e configurazioni ambiente test

**Da Test a Produzione (Deploy modifiche):**
1. **ATTENZIONE:** Mai clonare direttamente da test a produzione
2. Applica manualmente le modifiche testate
3. Backup completo produzione prima di ogni modifica
4. Test su staging prima del deploy finale

---

## 🖥️ Setup Ambiente Locale

### **Per Windows - XAMPP**

1. **Scarica XAMPP** da https://www.apachefriends.org/
2. **Installa** con componenti:
   - ✅ Apache
   - ✅ MySQL
   - ✅ PHP (versione 8.0+)
   - ✅ phpMyAdmin

3. **Avvia servizi:**
   ```
   XAMPP Control Panel > Start Apache + MySQL
   ```

4. **Verifica installazione:**
   - Apache: http://localhost
   - phpMyAdmin: http://localhost/phpmyadmin

### **Per macOS - MAMP**

1. **Scarica MAMP** da https://www.mamp.info/
2. **Configura porta Apache:** 80 (non 8888)
3. **Configura porta MySQL:** 3306 (non 8889)

### **Per Linux - LAMP Stack**

```bash
# Ubuntu/Debian - RACCOMANDATO: MariaDB invece di MySQL
sudo apt update
sudo apt install apache2 mariadb-server php libapache2-mod-php php-mysql

# Avvia servizi
sudo systemctl start apache2
sudo systemctl start mariadb

# Configura MariaDB (sicurezza)
sudo mysql_secure_installation

# Verifica installazione MariaDB
mysql --version
# Output atteso: mariadb Ver 15.1 Distrib 10.6+ 
```

**Perché MariaDB invece di MySQL:**
- ✅ Performance superiori (15-40% più veloce)
- ✅ Sicurezza avanzata nativa
- ✅ Compatibilità totale con WordPress
- ✅ Licenza GPL pura (no Oracle)

---

## 🔐 Configurazioni Specifiche

### **PHP Settings (php.ini)**
```ini
# Aumenta limiti per siti grandi
upload_max_filesize = 256M
post_max_size = 256M
max_execution_time = 300
memory_limit = 512M

# Abilita estensioni necessarie
extension=mysqli
extension=gd
extension=curl
extension=zip
```

### **Apache Settings (.htaccess)**
```apache
# WordPress permalink structure
RewriteEngine On
RewriteRule ^index\.php$ - [L]
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule . /index.php [L]

# Sicurezza locale
<Files wp-config.php>
Order allow,deny
Deny from all
</Files>
```

---

## 🎯 Opzioni Professionali

### **Local by Flywheel**

**Vantaggi:**
- ✅ Ambiente WordPress pre-configurato
- ✅ SSL locale automatico
- ✅ Gestione multiple installazioni
- ✅ Tool integrati (MailHog, Adminer)

**Download:** https://localwp.com/

### **DevKinsta (by Kinsta)**

**Vantaggi:**
- ✅ Stack identico a hosting Kinsta
- ✅ Sincronizzazione con sito live
- ✅ Database manager integrato
- ✅ Performance monitoring

---

## 🧪 Testing e Sincronizzazione

### **Best Practices Testing Locale**

1. **Separazione Ambienti:**
   ```
   Produzione: donnefuoridalsilenzioaps.it
   Staging: staging.donnefuoridalsilenzio.local
   Development: localhost/donnefuori
   ```

2. **Disabilita Plugin Produzione:**
   ```php
   // In wp-config.php locale
   define('WP_ENVIRONMENT_TYPE', 'local');
   
   // Disabilita plugin non necessari
   if (WP_ENVIRONMENT_TYPE === 'local') {
       // Disabilita analytics, cache, backup
   }
   ```

3. **Gestione Email Locali:**
   ```php
   // Evita invio email reali in test
   define('WP_MAIL_SMTP_ON', false);
   ```

### **Sincronizzazione Modifiche**

**Workflow consigliato:**

1. **Sviluppo locale** → Test modifiche
2. **Staging online** → Test con dati reali
3. **Produzione** → Deploy finale

**Tool per sincronizzazione:**
- **WP Migrate DB Pro** (sync database)
- **Git** per codice custom
- **rsync** per files

---

## ⚠️ Attenzioni Importanti

### **Sicurezza**

- 🔒 **Mai usare credenziali produzione** in locale
- 🔒 **Disabilita plugin di sicurezza** (Wordfence, etc)
- 🔒 **Non esporre ambiente locale** su internet
- 🔒 **Backup regolari** anche dell'ambiente locale

### **Performance**

- 🚀 **Disabilita cache** durante sviluppo
- 🚀 **Abilita WP_DEBUG** per troubleshooting
- 🚀 **Monitora log errori** in wp-content/debug.log

### **Database**

- 💾 **Usa prefisso tabelle diverso** (wp_local_)
- 💾 **Pulisci dati sensibili** (email utenti, etc)
- 💾 **Versioning database** per rollback

---

## 📋 Checklist Pre-Deploy

Prima di portare modifiche in produzione:

- [ ] ✅ Test completo funzionalità
- [ ] ✅ Verifica compatibilità plugin
- [ ] ✅ Test responsive design  
- [ ] ✅ Controllo prestazioni
- [ ] ✅ Backup sito produzione
- [ ] ✅ Piano rollback preparato

---

## 🆘 Troubleshooting Comuni

### **Problema: Immagini non caricate**
```sql
-- Aggiorna path uploads
UPDATE wp_options 
SET option_value = 'http://localhost/donnefuori/wp-content/uploads' 
WHERE option_name = 'upload_path';
```

### **Problema: Plugin non funzionano**
```php
// Forza reinstallazione plugin attivi
delete_option('active_plugins');
```

### **Problema: Tema non carica**
```sql
-- Reset tema attivo
UPDATE wp_options 
SET option_value = 'twentytwentythree' 
WHERE option_name = 'template';
```

---

**📞 Supporto Tecnico:**  
Per assistenza: massimo.fettucciari@libero.it

**📅 Ultimo aggiornamento:** 9 ottobre 2025