# 🔧 Configurazioni Post-Clonazione dfds.maxfet.cloud

**Sito test:** https://dfds.maxfet.cloud  
**Sito live:** donnefuoridalsilenzioaps.it  
**Data:** 9 ottobre 2025

---

## ✅ Checklist Configurazioni Immediate

### **1. Verifica URL nel Database**

**✅ MariaDB Compatibilità:** MariaDB è completamente compatibile e spesso preferibile a MySQL per WordPress.

Dopo l'installazione Duplicator, controlla che gli URL siano corretti:

```sql
-- Connetti al database via phpMyAdmin (funziona identico con MariaDB)
-- Verifica URL attuali
SELECT option_name, option_value 
FROM wp_options 
WHERE option_name IN ('home', 'siteurl');

-- Se non sono corretti, aggiorna:
UPDATE wp_options 
SET option_value = 'https://dfds.maxfet.cloud' 
WHERE option_name = 'home';

UPDATE wp_options 
SET option_value = 'https://dfds.maxfet.cloud' 
WHERE option_name = 'siteurl';
```

### **2. Configurazione wp-config.php**

Modifica il file `wp-config.php` aggiungendo:

```php
<?php
/* Configurazioni database - MariaDB compatibile */
define('DB_NAME', 'database_name_here');
define('DB_USER', 'username_here');
define('DB_PASSWORD', 'password_here');
define('DB_HOST', 'localhost'); // MariaDB usa stessa configurazione di MySQL
define('DB_CHARSET', 'utf8mb4'); // Raccomandato per MariaDB
define('DB_COLLATE', 'utf8mb4_unicode_ci'); // Migliore supporto Unicode

// URL specifici per ambiente test
define('WP_HOME','https://dfds.maxfet.cloud');
define('WP_SITEURL','https://dfds.maxfet.cloud');

// Identificazione ambiente
define('WP_ENVIRONMENT_TYPE', 'staging');

// Debug per ambiente test
define('WP_DEBUG', true);
define('WP_DEBUG_LOG', true);
define('WP_DEBUG_DISPLAY', false); // Non mostra errori ai visitatori
define('SCRIPT_DEBUG', true);

// Sicurezza ambiente test
define('BLOG_PUBLIC', 0); // Non indicizzare sui motori di ricerca
define('DISALLOW_FILE_EDIT', true); // Disabilita editor file in admin

// SSL/HTTPS
define('FORCE_SSL_ADMIN', true);
if (strpos($_SERVER['HTTP_X_FORWARDED_PROTO'], 'https') !== false) {
    $_SERVER['HTTPS'] = 'on';
}

// Aumenta limiti per testing
define('WP_MEMORY_LIMIT', '512M');
ini_set('max_execution_time', 300);

/* Il resto delle configurazioni WordPress */
```

### **3. Plugin da Disabilitare in Test**

Crea file `mu-plugins/disable-production-plugins.php`:

```php
<?php
/**
 * Disabilita plugin di produzione in ambiente test
 */

if (defined('WP_ENVIRONMENT_TYPE') && WP_ENVIRONMENT_TYPE === 'staging') {
    
    add_filter('option_active_plugins', function($plugins) {
        $production_plugins = [
            'wordfence/wordfence.php',                    // Sicurezza - può bloccare test
            'really-simple-ssl/rlrsssl-really-simple-ssl.php', // SSL già configurato
            'google-analytics-dashboard-for-wp/gadwp.php', // Analytics non necessario
            'mailchimp-for-wp/mailchimp-for-wp.php',    // Evita invii email test
            'updraftplus/updraftplus.php',               // Backup non necessario
            'wp-optimize/wp-optimize.php',               // Cache può interferire
            'jetpack/jetpack.php',                       // Statistiche non necessarie
        ];
        
        return array_diff($plugins, $production_plugins);
    });
    
    // Disabilita cron WordPress (evita task automatici)
    define('DISABLE_WP_CRON', true);
    
    // Disabilita aggiornamenti automatici
    define('AUTOMATIC_UPDATER_DISABLED', true);
}
```

### **4. Configurazione .htaccess**

Verifica/crea file `.htaccess` nella root:

```apache
# WordPress SEO by Yoast rewrite rules
RewriteEngine On
RewriteBase /

# Forza HTTPS
RewriteCond %{HTTPS} off
RewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]

# WordPress standard
RewriteRule ^index\.php$ - [L]
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule . /index.php [L]

# Sicurezza - Blocca accesso file sensibili
<FilesMatch "\.(htaccess|htpasswd|ini|log|sh|sql|conf|bak)$">
    Order allow,deny
    Deny from all
</FilesMatch>

# Proteggi wp-config.php
<Files wp-config.php>
    Order allow,deny
    Deny from all
</Files>

# Proteggi directory sensibili
<IfModule mod_rewrite.c>
    RewriteRule ^wp-admin/includes/ - [F,L]
    RewriteRule !^wp-includes/ - [S=3]
    RewriteRule ^wp-includes/[^/]+\.php$ - [F,L]
    RewriteRule ^wp-includes/js/tinymce/langs/.+\.php - [F,L]
    RewriteRule ^wp-includes/theme-compat/ - [F,L]
</IfModule>

# Headers sicurezza per ambiente test
<IfModule mod_headers.c>
    Header set X-Robots-Tag "noindex, nofollow"
    Header set X-Frame-Options "SAMEORIGIN"
    Header set X-Content-Type-Options "nosniff"
</IfModule>
```

---

## 🗄️ Configurazione MariaDB per WordPress

### **QNAP NAS - Scelta Package MariaDB**

**🏆 RACCOMANDAZIONE: MariaDB 10 (versione 1.2.1.31)**

**❌ NON usare MariaDB 5** - Versione obsoleta e non sicura

**✅ Motivi per scegliere MariaDB 10:**
- **Sicurezza:** MariaDB 5.x non riceve più aggiornamenti di sicurezza
- **Performance:** MariaDB 10.x fino al 40% più veloce
- **Compatibilità:** WordPress richiede MySQL 5.7+ o MariaDB 10.2+
- **Funzionalità:** JSON support, window functions, CTE
- **Supporto futuro:** Solo MariaDB 10.x riceve nuove feature

### **Installazione su QNAP**

```bash
# Via App Center QNAP
1. App Center > Cerca "MariaDB 10"
2. Installa "MariaDB 10" versione 1.2.1.31
3. ⚠️ NON installare "MariaDB 5" - è obsoleto

# Configurazione post-installazione
1. Apri MariaDB 10 da QTS Desktop
2. Configura password root
3. Abilita accesso remoto se necessario
```

### **Vantaggi MariaDB vs MySQL**

**✅ Perché MariaDB è preferibile:**
- **🚀 Performance migliori** - Query più veloci
- **🔒 Sicurezza avanzata** - Crittografia nativa
- **💾 Storage engines** - Più opzioni disponibili
- **🆓 Open Source puro** - Senza licenze Oracle
- **🔄 Backward compatibility** - Drop-in replacement per MySQL

### **Configurazione Ottimale MariaDB**

#### **1. Versioni Consigliate**
```bash
# Verifica versione MariaDB
mysql --version
# O da MySQL/MariaDB shell:
SELECT VERSION();

# Versioni consigliate per WordPress:
MariaDB 10.4+ (preferibile 10.6+ o 10.11 LTS)
```

#### **2. Configurazione my.cnf per WordPress**

**Per server standard:**
```ini
# /etc/mysql/mariadb.conf.d/50-server.cnf
# Oppure /etc/my.cnf

[mariadb]
# Prestazioni base
innodb_buffer_pool_size = 256M        # 70% RAM disponibile
innodb_log_file_size = 64M
innodb_flush_log_at_trx_commit = 2
innodb_flush_method = O_DIRECT

# WordPress specifico
max_connections = 100
table_open_cache = 4096
query_cache_type = 1
query_cache_size = 32M
query_cache_limit = 2M

# UTF8MB4 (WordPress raccomandato)
character_set_server = utf8mb4
collation_server = utf8mb4_unicode_ci
innodb_default_row_format = dynamic

# Sicurezza
local_infile = 0
symbolic_links = 0

# Log per debug
slow_query_log = 1
slow_query_log_file = /var/log/mysql/slow.log
long_query_time = 2

[mysql]
default_character_set = utf8mb4
```

**Per QNAP NAS (configurazione ottimizzata):**
```ini
# File: /share/CACHEDEV1_DATA/.qpkg/MariaDB10/etc/my.cnf
# Accesso: SSH su QNAP o File Station

[mariadb-10.6]
# === OTTIMIZZAZIONI QNAP SPECIFICHE ===
# RAM limitata su NAS - configurazione conservativa
innodb_buffer_pool_size = 128M        # Adatta alla RAM disponibile
innodb_log_file_size = 32M
innodb_flush_log_at_trx_commit = 2
innodb_flush_method = O_DIRECT

# Connessioni limitate per NAS
max_connections = 50
table_open_cache = 1024
query_cache_type = 1
query_cache_size = 16M
query_cache_limit = 1M

# UTF8MB4 per WordPress
character_set_server = utf8mb4
collation_server = utf8mb4_unicode_ci
innodb_default_row_format = dynamic

# Sicurezza NAS
local_infile = 0
symbolic_links = 0
bind_address = 127.0.0.1  # Solo accesso locale (sicurezza)

# Log ottimizzati per NAS (meno I/O)
slow_query_log = 0        # Disabilita per ridurre scritture SSD
general_log = 0
log_error = /share/CACHEDEV1_DATA/.qpkg/MariaDB10/logs/error.log

# Ottimizzazioni storage NAS
innodb_flush_neighbors = 0    # Ottimo per SSD
innodb_io_capacity = 200      # Conservativo per NAS
innodb_read_io_threads = 2
innodb_write_io_threads = 2

[mysql]
default_character_set = utf8mb4
```

#### **3. Creazione Database WordPress su MariaDB**

```sql
-- Connessione come root
mysql -u root -p

-- Crea database con charset corretto
CREATE DATABASE donnefuori_test 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

-- Crea utente dedicato
CREATE USER 'wp_user'@'localhost' IDENTIFIED BY 'password_sicura_qui';

-- Assegna privilegi specifici (principio least privilege)
GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, ALTER, INDEX 
ON donnefuori_test.* TO 'wp_user'@'localhost';

-- Flush privilegi
FLUSH PRIVILEGES;

-- Verifica configurazione
SHOW DATABASES;
SHOW GRANTS FOR 'wp_user'@'localhost';
```

#### **4. Ottimizzazioni WordPress per MariaDB**

```php
// wp-config.php - Configurazioni specifiche MariaDB
define('DB_CHARSET', 'utf8mb4');
define('DB_COLLATE', 'utf8mb4_unicode_ci');

// Ottimizzazioni database
define('WP_ALLOW_REPAIR', true); // Solo per debug, rimuovi dopo
define('AUTOMATIC_UPDATER_DISABLED', true); // Ambiente test

// Cache query se disponibile
define('WP_CACHE', true);

// Revisioni post (limita per performance)
define('WP_POST_REVISIONS', 5);
define('AUTOSAVE_INTERVAL', 300); // 5 minuti

// Garbage collection
define('EMPTY_TRASH_DAYS', 7);
```

### **Migrazione da MySQL a MariaDB**

Se stai migrando da MySQL esistente:

```bash
# 1. Backup database MySQL
mysqldump -u root -p --single-transaction --routines --triggers donnefuori_test > backup_mysql.sql

# 2. Installa MariaDB
# Ubuntu/Debian:
sudo apt update
sudo apt install mariadb-server mariadb-client

# CentOS/RHEL:
sudo yum install mariadb-server mariadb

# 3. Avvia MariaDB
sudo systemctl start mariadb
sudo systemctl enable mariadb

# 4. Secure installation
sudo mysql_secure_installation

# 5. Importa dati
mysql -u root -p donnefuori_test < backup_mysql.sql
```

### **Performance Tuning MariaDB per WordPress**

#### **Monitoring Performance**

```sql
-- Query performance
SHOW GLOBAL STATUS LIKE 'Slow_queries';
SHOW GLOBAL STATUS LIKE 'Questions';

-- Buffer pool efficiency
SHOW GLOBAL STATUS LIKE 'Innodb_buffer_pool_%';

-- Connection usage
SHOW GLOBAL STATUS LIKE 'Connections';
SHOW GLOBAL STATUS LIKE 'Max_used_connections';

-- Cache hit rate
SHOW GLOBAL STATUS LIKE 'Qcache%';
```

#### **Ottimizzazioni Automatiche**

```sql
-- Enable performance schema per monitoring avanzato
-- my.cnf:
[mariadb]
performance_schema = ON
```

### **Backup e Restore MariaDB**

#### **Backup Automatico**

```bash
#!/bin/bash
# Script backup MariaDB per WordPress
# /home/user/scripts/backup_mariadb.sh

DB_NAME="donnefuori_test"
DB_USER="wp_user"
DB_PASS="password"
BACKUP_DIR="/backup/database"
DATE=$(date +%Y%m%d_%H%M%S)

# Crea directory se non esiste
mkdir -p $BACKUP_DIR

# Backup con compressione
mysqldump -u $DB_USER -p$DB_PASS \
  --single-transaction \
  --routines \
  --triggers \
  --events \
  $DB_NAME | gzip > $BACKUP_DIR/wp_backup_$DATE.sql.gz

# Mantieni solo backup ultimi 7 giorni
find $BACKUP_DIR -name "wp_backup_*.sql.gz" -mtime +7 -delete

echo "Backup completato: wp_backup_$DATE.sql.gz"
```

#### **Cron per Backup Automatici**

```bash
# Aggiungi a crontab
crontab -e

# Backup giornaliero alle 02:00
0 2 * * * /home/user/scripts/backup_mariadb.sh >/dev/null 2>&1

# Backup settimanale completo domenica 01:00
0 1 * * 0 /home/user/scripts/backup_full_mariadb.sh >/dev/null 2>&1
```

---

## 🧪 Test Funzionalità Post-Installazione

### **Test Base (da eseguire nell'ordine)**

1. **✅ Accesso sito principale:**
   ```
   URL: https://dfds.maxfet.cloud
   Verifica: Sito carica senza errori 500/404
   ```

2. **✅ Login amministratore:**
   ```
   URL: https://dfds.maxfet.cloud/wp-admin
   Verifica: Login con credenziali funziona
   ```

3. **✅ Dashboard WordPress:**
   ```
   Verifica: Tutte le sezioni accessibili
   Controlla: Eventuali messaggi di errore
   ```

4. **✅ Menu di navigazione:**
   ```
   Test: Tutti i link del menu funzionano
   Verifica: Home, L'associazione, News, Contatti
   ```

5. **✅ Immagini e media:**
   ```
   Controllo: Immagini homepage caricano
   Test: Upload nuova immagine
   Verifica: Gallery e slider funzionano
   ```

6. **✅ Tema Divi:**
   ```
   Controllo: Divi Builder accessibile
   Test: Modifica pagina con Visual Builder
   Verifica: Personalizzazioni tema mantenute
   ```

### **Test Avanzati**

7. **✅ Plugin attivi essenziali:**
   ```bash
   # Via WP-CLI se disponibile
   wp plugin list --status=active
   
   # Verifica manualmente in admin:
   Plugin > Plugin installati
   ```

8. **✅ Database e contenuti:**
   ```sql
   -- Conta articoli
   SELECT COUNT(*) FROM wp_posts WHERE post_type = 'post' AND post_status = 'publish';
   
   -- Conta pagine
   SELECT COUNT(*) FROM wp_posts WHERE post_type = 'page' AND post_status = 'publish';
   
   -- Conta utenti
   SELECT COUNT(*) FROM wp_users;
   ```

9. **✅ SEO e metadati:**
   ```
   Verifica: Plugin Yoast SEO attivo
   Test: Meta description homepage
   Controllo: Robots.txt blocca indicizzazione
   ```

---

## 🔧 Troubleshooting Comune

### **Problema: Errore connessione MariaDB**

**Causa possibile:** Configurazione utente o permessi

**Soluzione:**
```sql
-- Verifica utente e permessi
SELECT user, host FROM mysql.user WHERE user = 'wp_user';
SHOW GRANTS FOR 'wp_user'@'localhost';

-- Se necessario, ricrea utente
DROP USER 'wp_user'@'localhost';
CREATE USER 'wp_user'@'localhost' IDENTIFIED BY 'nuova_password';
GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, ALTER, INDEX 
ON donnefuori_test.* TO 'wp_user'@'localhost';
FLUSH PRIVILEGES;
```

**Verifica connessione:**
```bash
# Test connessione da terminale
mysql -u wp_user -p -h localhost donnefuori_test

# Test da PHP
php -r "
\$mysqli = new mysqli('localhost', 'wp_user', 'password', 'donnefuori_test');
if (\$mysqli->connect_error) {
    die('Connection failed: ' . \$mysqli->connect_error);
}
echo 'Connected successfully to MariaDB';
"
```

### **Problema: Charset/Collation errors**

**Causa:** Database con charset diverso da utf8mb4

**Soluzione:**
```sql
-- Verifica charset attuale
SELECT DEFAULT_CHARACTER_SET_NAME, DEFAULT_COLLATION_NAME 
FROM information_schema.SCHEMATA 
WHERE SCHEMA_NAME = 'donnefuori_test';

-- Converte database a utf8mb4
ALTER DATABASE donnefuori_test 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

-- Converte tutte le tabelle
SELECT CONCAT('ALTER TABLE ', table_name, ' CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;')
FROM information_schema.tables 
WHERE table_schema = 'donnefuori_test';
```

### **Problema: Performance lente con MariaDB**

**Causa:** Configurazione non ottimizzata

**Soluzione:**
```sql
-- Analizza query lente
SELECT * FROM mysql.slow_log ORDER BY start_time DESC LIMIT 10;

-- Verifica status chiave
SHOW GLOBAL STATUS LIKE 'innodb_buffer_pool_read%';
SHOW GLOBAL STATUS LIKE 'query_cache%';

-- Ottimizza tabelle
OPTIMIZE TABLE wp_posts, wp_postmeta, wp_options;

-- Analizza e ripara se necessario
ANALYZE TABLE wp_posts;
REPAIR TABLE wp_posts;
```

---

## 📧 Configurazione Email Testing

### **Problema: Sito mostra contenuto del sito live**

**Causa:** URL nel database non aggiornati correttamente

**Soluzione:**
```sql
-- Aggiorna tutte le occorrenze URL
UPDATE wp_options SET option_value = 'https://dfds.maxfet.cloud' WHERE option_value = 'https://donnefuoridalsilenzioaps.it';

-- Aggiorna contenuti post
UPDATE wp_posts SET post_content = REPLACE(post_content, 'https://donnefuoridalsilenzioaps.it', 'https://dfds.maxfet.cloud');

-- Aggiorna meta post
UPDATE wp_postmeta SET meta_value = REPLACE(meta_value, 'https://donnefuoridalsilenzioaps.it', 'https://dfds.maxfet.cloud');
```

### **Problema: Immagini non caricano**

**Causa:** Path uploads non aggiornato

**Soluzione:**
```sql
-- Verifica path upload attuale
SELECT option_value FROM wp_options WHERE option_name = 'upload_path';

-- Aggiorna se necessario
UPDATE wp_options 
SET option_value = '/home/[user]/public_html/wp-content/uploads' 
WHERE option_name = 'upload_path';

-- Aggiorna URL uploads
UPDATE wp_options 
SET option_value = 'https://dfds.maxfet.cloud/wp-content/uploads' 
WHERE option_name = 'upload_url_path';
```

### **Problema: Plugin Divi non funziona**

**Causa:** Licenza legata al dominio originale

**Soluzione:**
```php
// Temporaneamente disabilita controllo licenza
// In wp-config.php aggiungi:
define('ET_CORE_PORTABILITY', true);

// Oppure riattiva licenza Divi per nuovo dominio
// Dashboard > Divi > Theme Options > Updates
```

---

## 📧 Configurazione Email Testing

### **Prevenire Invio Email Reali**

```php
// In wp-config.php o mu-plugin
if (WP_ENVIRONMENT_TYPE === 'staging') {
    
    // Blocca tutte le email
    function disable_wp_mail() {
        return false;
    }
    add_filter('pre_wp_mail', 'disable_wp_mail');
    
    // Oppure reindirizza a email test
    function redirect_test_emails($args) {
        $args['to'] = 'test@maxfet.cloud';
        $args['subject'] = '[TEST] ' . $args['subject'];
        return $args;
    }
    add_filter('wp_mail', 'redirect_test_emails');
}
```

---

## 🔄 Workflow Sincronizzazione

### **Aggiornamento Test da Produzione**

**Frequenza consigliata:** Settimanale o prima di test importanti

```bash
# 1. Backup sito test attuale
# 2. Download nuovo pacchetto Duplicator da produzione
# 3. Upload e installazione su dfds.maxfet.cloud
# 4. Ripeti configurazioni questo documento
```

### **Deploy Modifiche da Test a Produzione**

**⚠️ ATTENZIONE:** Mai clonare direttamente test → produzione

**Processo sicuro:**
1. **Documenta modifiche** fatte in test
2. **Backup completo** sito produzione
3. **Applica modifiche manualmente** su produzione
4. **Test finale** su produzione

---

## 📊 Monitoraggio Ambiente Test

### **Log da Controllare Regolarmente**

```bash
# Log errori PHP
tail -f /path/to/error.log

# Log errori WordPress
tail -f /wp-content/debug.log

# Log accessi Apache
tail -f /path/to/access.log
```

### **Performance Monitoring**

```
Tools consigliati:
- GTmetrix per speed test
- Google PageSpeed Insights
- Query Monitor plugin per debug database
```

---

## 🆘 Contatti Emergenza

**Problemi tecnici sito test:**  
📧 massimo.fettucciari@libero.it

**Problemi contenuti/accesso:**  
📧 donnefuoridalsilenzio@gmail.com

**Documentazione aggiornata:** 9 ottobre 2025  
**Prossima verifica:** Gennaio 2026