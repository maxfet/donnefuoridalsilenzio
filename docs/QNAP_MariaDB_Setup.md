# 🏠 QNAP MariaDB Setup per WordPress - Guida Completa

**Target:** NAS QNAP con WordPress per donnefuoridalsilenzio  
**Database:** MariaDB 10 vs MariaDB 5  
**Data:** 9 ottobre 2025

---

## 🎯 **Risposta Diretta: MariaDB 10 (versione 1.2.1.31)**

### **❌ NON usare MariaDB 5 - Motivi:**

1. **🚨 Sicurezza CRITICA:**
   - MariaDB 5.x non riceve più patch di sicurezza
   - Vulnerabilità note non risolte
   - End-of-life dal 2017

2. **⚡ Performance Inferiori:**
   - Fino al 40% più lento di MariaDB 10
   - Gestione memoria obsoleta
   - Query optimizer meno efficiente

3. **🔧 Compatibilità Limitata:**
   - WordPress raccomanda MySQL 5.7+ o MariaDB 10.2+
   - Plugin moderni richiedono funzionalità MariaDB 10+
   - JSON support limitato o assente

### **✅ MariaDB 10 - Vantaggi:**

1. **🛡️ Sicurezza Attiva:**
   - Aggiornamenti regolari di sicurezza
   - Crittografia moderna
   - Autenticazione avanzata

2. **🚀 Performance Superiori:**
   - Query engine ottimizzato
   - Better memory management
   - Parallel replication

3. **📈 Funzionalità Moderne:**
   - JSON support completo
   - Window functions
   - Common Table Expressions (CTE)
   - Virtual columns

---

## 🔧 Installazione MariaDB 10 su QNAP

### **Configurazione SSH per Accesso Remoto**

**✅ SSH Key configurata per mfh-nas01:**
```bash
# Connessione SSH configurata
Host: mfh-nas01 (192.168.36.4)
User: webadmin
Key: ~/.ssh/id_ed25519_mfh-nas01
Status: ✅ Attiva e funzionante

# Test connessione
ssh webadmin@mfh-nas01 'whoami'
# Output: webadmin
```

**Configurazione SSH locale:**
```bash
# File: ~/.ssh/config
Host mfh-nas01
    HostName mfh-nas01
    User webadmin
    IdentityFile ~/.ssh/id_ed25519_mfh-nas01
    IdentitiesOnly yes
    PubkeyAuthentication yes
    PreferredAuthentications publickey,password
```

### **Step 1: App Center Installation**

**✅ MariaDB 10 già installato su mfh-nas01:**

**✅ MariaDB 10 già installato e configurato su mfh-nas01:**

```bash
# Via App Center QNAP
Status: ✅ Installato e inizializzato
Versione: MariaDB 10.5.8-log
Porta: 3307 (non standard 3306)
Binari: /share/CACHEDEV1_DATA/.qpkg/MariaDB10/bin/

# Credenziali configurate
Root password: WAKr8r*YEMep1fb
Database WordPress: donnefuori_qnap
User WordPress: wp_qnap
Password WordPress: WP_qnap2025!

# Test connessione
/share/CACHEDEV1_DATA/.qpkg/MariaDB10/bin/mysql \
  -u root -p"WAKr8r*YEMep1fb" \
  --protocol=TCP -h 127.0.0.1 -P 3307 \
  -e "SELECT VERSION();"
# Output: 10.5.8-MariaDB-log
```

**Database WordPress configurato:**
```sql
-- Database creato con charset ottimale
CREATE DATABASE donnefuori_qnap 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

-- Utente con privilegi minimi necessari
CREATE USER 'wp_qnap'@'localhost' IDENTIFIED BY 'WP_qnap2025!';
GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, ALTER, INDEX, 
      LOCK TABLES, CREATE TEMPORARY TABLES 
ON donnefuori_qnap.* TO 'wp_qnap'@'localhost';
```

### **Step 2: Configurazione Iniziale**

```bash
# Accesso via SSH QNAP (opzionale)
ssh admin@[IP-QNAP]

# Oppure tramite interfaccia web MariaDB
# URL: http://[IP-QNAP]:3307/phpmyadmin (porta può variare)
```

### **Step 3: Setup Security**

```sql
-- Connessione come root (password impostata durante installazione)
mysql -u root -p

-- Configurazione sicurezza base
-- Cambia password root se necessario
ALTER USER 'root'@'localhost' IDENTIFIED BY 'password_super_sicura';

-- Rimuovi utenti anonimi
DELETE FROM mysql.user WHERE User='';

-- Rimuovi database test
DROP DATABASE IF EXISTS test;
DELETE FROM mysql.db WHERE Db='test' OR Db='test\\_%';

-- Flush privilegi
FLUSH PRIVILEGES;
```

---

## 🗄️ Configurazione Database WordPress

### **Creazione Database Ottimizzato**

```sql
-- Database per sito test
CREATE DATABASE donnefuori_qnap
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

-- Utente dedicato WordPress
CREATE USER 'wp_qnap'@'localhost' IDENTIFIED BY 'password_wordpress_sicura';

-- Privilegi minimi necessari
GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, ALTER, INDEX, LOCK TABLES, CREATE TEMPORARY TABLES 
ON donnefuori_qnap.* TO 'wp_qnap'@'localhost';

-- Se usi plugin avanzati (backup, import/export)
GRANT CREATE ROUTINE, ALTER ROUTINE, EXECUTE 
ON donnefuori_qnap.* TO 'wp_qnap'@'localhost';

FLUSH PRIVILEGES;

-- Verifica creazione
SHOW DATABASES LIKE 'donnefuori_qnap';
SHOW GRANTS FOR 'wp_qnap'@'localhost';
```

### **Configurazione my.cnf per QNAP**

```ini
# File: /share/CACHEDEV1_DATA/.qpkg/MariaDB10/etc/my.cnf
# Modifica via SSH o File Station

[mariadb-10.6]
# === CONFIGURAZIONE QNAP OPTIMIZED ===

# === MEMORIA (adatta alla RAM QNAP) ===
# Per QNAP con 4GB RAM
innodb_buffer_pool_size = 256M
# Per QNAP con 2GB RAM
# innodb_buffer_pool_size = 128M  
# Per QNAP con 8GB+ RAM
# innodb_buffer_pool_size = 512M

innodb_log_file_size = 64M
innodb_log_buffer_size = 16M
innodb_flush_log_at_trx_commit = 2

# === CONNESSIONI (conservative per NAS) ===
max_connections = 75
max_user_connections = 70
thread_cache_size = 20

# === CACHE QUERY ===
query_cache_type = 1
query_cache_size = 32M
query_cache_limit = 2M

# === TABELLE ===
table_open_cache = 2048
table_definition_cache = 1024

# === CHARSET WORDPRESS ===
character_set_server = utf8mb4
collation_server = utf8mb4_unicode_ci
innodb_default_row_format = dynamic

# === SICUREZZA QNAP ===
local_infile = 0
symbolic_links = 0
bind_address = 127.0.0.1    # Solo accesso locale
skip_name_resolve = 1       # Evita DNS lookup
secure_file_priv = NULL

# === STORAGE OPTIMIZATION ===
# Ottimizzazioni per SSD QNAP
innodb_flush_neighbors = 0
innodb_io_capacity = 200
innodb_io_capacity_max = 400
innodb_read_io_threads = 2
innodb_write_io_threads = 2

# Reduce disk writes (preserva SSD)
innodb_flush_method = O_DIRECT
sync_binlog = 0
innodb_doublewrite = 0      # Safe on modern SSD

# === LOGGING (minimal per NAS) ===
# Disabilita log non essenziali per preservare storage
slow_query_log = 0
general_log = 0
log_error = /share/CACHEDEV1_DATA/.qpkg/MariaDB10/logs/error.log
log_error_verbosity = 2

# === PERFORMANCE TUNING ===
# Ottimizzazioni specifiche WordPress
tmp_table_size = 32M
max_heap_table_size = 32M

# Full-text search per WordPress
ft_min_word_len = 3
ft_boolean_syntax = '+ -><()~*:""&|'

[mysql]
default_character_set = utf8mb4

[mysqldump]
default_character_set = utf8mb4
single_transaction = 1
quick = 1
lock_tables = 0
```

---

## 🔧 WordPress wp-config.php per QNAP

```php
<?php
// === DATABASE CONFIGURATION QNAP mfh-nas01 ===
define('DB_NAME', 'donnefuori_qnap');
define('DB_USER', 'wp_qnap');
define('DB_PASSWORD', 'WP_qnap2025!');
define('DB_HOST', '127.0.0.1:3307'); // Porta specifica QNAP MariaDB

// Charset ottimizzato per MariaDB 10.5.8
define('DB_CHARSET', 'utf8mb4');
define('DB_COLLATE', 'utf8mb4_unicode_ci');

// === QNAP SPECIFIC OPTIMIZATIONS ===
// Aumenta timeout per NAS (storage può essere più lento)
define('DB_TIMEOUT', 60);

// Memoria per operazioni database complesse
ini_set('memory_limit', '256M');

// === WORDPRESS OPTIMIZATIONS ===
// Cache oggetti (attiva se installi Redis/Memcached su QNAP)
define('WP_CACHE', false); // Cambia in true se attivi cache

// Revisioni limitate (risparmia spazio QNAP)
define('WP_POST_REVISIONS', 3);
define('AUTOSAVE_INTERVAL', 300); // 5 minuti

// Garbage collection aggressivo
define('EMPTY_TRASH_DAYS', 7);
define('MEDIA_TRASH', true);

// === ENVIRONMENT CONFIGURATION ===
define('WP_ENVIRONMENT_TYPE', 'staging');

// Debug per ambiente test
define('WP_DEBUG', true);
define('WP_DEBUG_LOG', true);
define('WP_DEBUG_DISPLAY', false);
define('SCRIPT_DEBUG', false); // True solo per debug JS/CSS

// === SECURITY ===
// Disabilita file editing
define('DISALLOW_FILE_EDIT', true);
define('DISALLOW_FILE_MODS', false); // Permetti aggiornamenti plugin

// SSL se configurato
if (isset($_SERVER['HTTPS']) && $_SERVER['HTTPS'] === 'on') {
    define('FORCE_SSL_ADMIN', true);
}

// === QNAP PATHS ===
// Assicurati che i path siano corretti per QNAP
// define('WP_CONTENT_DIR', '/share/Web/wordpress/wp-content');
// define('WP_CONTENT_URL', 'http://[IP-QNAP]/wordpress/wp-content');

/* Il resto della configurazione WordPress standard */
```

---

## 📊 Monitoring MariaDB su QNAP

### **Via QTS Resource Monitor**

```bash
# Accesso: QTS > Resource Monitor > Database
# Monitora:
- CPU usage MariaDB
- Memory consumption  
- Disk I/O database
- Network connections
```

### **Via MariaDB Commands**

```sql
-- Status generale
SHOW GLOBAL STATUS LIKE 'Uptime';
SHOW GLOBAL STATUS LIKE 'Connections';
SHOW GLOBAL STATUS LIKE 'Questions';

-- Performance
SHOW GLOBAL STATUS LIKE 'Slow_queries';
SHOW GLOBAL STATUS LIKE 'Innodb_buffer_pool_read%';

-- Cache efficiency
SHOW GLOBAL STATUS LIKE 'Qcache%';

-- Storage usage
SELECT 
    table_schema as 'Database',
    ROUND(SUM(data_length + index_length) / 1024 / 1024, 2) as 'Size (MB)'
FROM information_schema.tables 
WHERE table_schema = 'donnefuori_qnap'
GROUP BY table_schema;
```

### **Script Monitoring Automatico**

```bash
#!/bin/bash
# /share/scripts/mariadb_monitor.sh

QNAP_DB_PATH="/share/CACHEDEV1_DATA/.qpkg/MariaDB10"
LOG_FILE="/share/logs/mariadb_monitor.log"
DB_NAME="donnefuori_qnap"
DB_USER="wp_qnap"
DB_PASS="password"

echo "=== MariaDB QNAP Monitor - $(date) ===" >> $LOG_FILE

# Database size
mysql -u $DB_USER -p$DB_PASS -e "
SELECT 
    ROUND(SUM(data_length + index_length) / 1024 / 1024, 2) as 'DB_Size_MB'
FROM information_schema.tables 
WHERE table_schema = '$DB_NAME';" >> $LOG_FILE

# Performance stats
mysql -u $DB_USER -p$DB_PASS -e "
SHOW GLOBAL STATUS LIKE 'Connections';
SHOW GLOBAL STATUS LIKE 'Slow_queries';
SHOW GLOBAL STATUS LIKE 'Uptime';" >> $LOG_FILE

# Disk space check
df -h $QNAP_DB_PATH >> $LOG_FILE

echo "=== End Monitor ===" >> $LOG_FILE
```

---

## 🔄 Backup Strategy QNAP

### **Backup Automatico Database**

```bash
#!/bin/bash
# /share/scripts/backup_mariadb.sh

DB_NAME="donnefuori_qnap"
DB_USER="wp_qnap" 
DB_PASS="password"
BACKUP_DIR="/share/backup/database"
DATE=$(date +%Y%m%d_%H%M%S)

# Crea directory backup
mkdir -p $BACKUP_DIR

# Backup completo con compressione
mysqldump -u $DB_USER -p$DB_PASS \
    --single-transaction \
    --routines \
    --triggers \
    --events \
    --opt \
    $DB_NAME | gzip > $BACKUP_DIR/donnefuori_backup_$DATE.sql.gz

# Mantieni solo 14 giorni di backup
find $BACKUP_DIR -name "donnefuori_backup_*.sql.gz" -mtime +14 -delete

# Log risultato
echo "$(date): Backup completato - donnefuori_backup_$DATE.sql.gz" >> /share/logs/backup.log
```

### **Configurazione Cron QNAP**

```bash
# Accesso: QTS > Control Panel > System > Hardware > General > External Device
# Oppure via SSH:

# Edit crontab
crontab -e

# Backup giornaliero alle 02:00
0 2 * * * /share/scripts/backup_mariadb.sh >/dev/null 2>&1

# Monitor ogni ora
0 * * * * /share/scripts/mariadb_monitor.sh >/dev/null 2>&1
```

---

## 🔧 Ottimizzazioni Hardware QNAP

### **Storage Configuration**

```bash
# Per SSD Cache (se disponibile)
# QTS > Storage & Snapshots > Cache Acceleration
# Abilita SSD cache per volume database

# RAID Configuration ottimale:
# RAID 1: Per sicurezza massima (mirror)
# RAID 5: Per bilanciamento spazio/sicurezza
# RAID 10: Per performance massime (se 4+ dischi)
```

### **Network Optimization**

```bash
# QTS > Control Panel > Network & File Services > Network
# Abilita Jumbo Frames se rete lo supporta
# MTU: 9000 per rete Gigabit interna

# Port Trunking se disponibile per aggregazione banda
```

### **Memory Management**

```bash
# Verifica RAM disponibile
free -h

# Se possibile, aumenta RAM dedicata a MariaDB
# QTS > Resource Monitor > Memory
# Target: 70% RAM disponibile per innodb_buffer_pool_size
```

---

## 🚀 Performance Tuning Specifico QNAP

### **1. Ottimizzazioni Sistema**

```bash
# Disabilita servizi non necessari per liberare RAM
# QTS > Control Panel > Applications > Service Binding

# Servizi da considerare disabilitare per server database:
- iTunes Server (se non usato)
- DLNA Media Server (se non necessario)  
- Time Machine (se non usato per backup Mac)
```

### **2. Snapshot Strategy**

```bash
# QTS > Storage & Snapshots > Snapshots
# Configura snapshot prima di aggiornamenti:

# Before MariaDB updates
Frequency: Manual before changes
Retention: 3 snapshots

# Daily snapshots  
Frequency: Daily at 01:00
Retention: 7 days
```

### **3. Network Services**

```bash
# Ottimizza servizi rete per database access
# QTS > Control Panel > Network & File Services

# SSH: Abilita per admin remoto
# FTP: Disabilita se non necessario
# Telnet: Disabilita per sicurezza
# SNMP: Abilita per monitoring se necessario
```

---

## ⚠️ Troubleshooting Comune QNAP

### **Problema: MariaDB non si avvia**

```bash
# Verifica status servizio
# QTS > App Center > MariaDB 10 > Status

# Check log errori
tail -f /share/CACHEDEV1_DATA/.qpkg/MariaDB10/logs/error.log

# Restart forzato
# QTS > MariaDB 10 > Stop > Start

# Se problema persiste, verifica spazio disco
df -h /share/CACHEDEV1_DATA/
```

### **Problema: WordPress lento con database**

```sql
-- Verifica query lente
SHOW GLOBAL STATUS LIKE 'Slow_queries';

-- Ottimizza tabelle WordPress
USE donnefuori_qnap;
OPTIMIZE TABLE wp_posts, wp_postmeta, wp_options;

-- Verifica indici
SHOW INDEX FROM wp_postmeta;
```

### **Problema: Connessione database timeout**

```php
// wp-config.php - Aumenta timeout
define('DB_TIMEOUT', 120);
ini_set('mysql.connect_timeout', 120);
ini_set('default_socket_timeout', 120);
```

---

## 📋 Checklist Setup Completo

### **Pre-installazione:**
- [ ] ✅ Verificata RAM disponibile QNAP (min 2GB)
- [ ] ✅ Spazio storage sufficiente (min 10GB liberi)  
- [ ] ✅ Backup configurazione QNAP esistente
- [ ] ✅ Aggiornato QTS alla versione latest

### **Installazione:**
- [ ] ✅ Installato MariaDB 10 (NON MariaDB 5)
- [ ] ✅ Verificata versione 1.2.1.31 o superiore
- [ ] ✅ Configurata password root sicura
- [ ] ✅ Testato accesso MariaDB

### **Configurazione:**
- [ ] ✅ Creato database donnefuori_qnap
- [ ] ✅ Creato utente wp_qnap con privilegi limitati
- [ ] ✅ Configurato my.cnf ottimizzato QNAP
- [ ] ✅ Aggiornato wp-config.php WordPress

### **Sicurezza:**
- [ ] ✅ Rimossi utenti anonimi MariaDB
- [ ] ✅ Configurato bind_address locale only
- [ ] ✅ Disabilitato local_infile
- [ ] ✅ Configurato firewall QNAP se necessario

### **Backup:**
- [ ] ✅ Script backup automatico configurato
- [ ] ✅ Cron job attivato per backup giornalieri
- [ ] ✅ Testato restore da backup
- [ ] ✅ Configurati snapshot QNAP

### **Monitoring:**
- [ ] ✅ Script monitoring configurato
- [ ] ✅ Log rotation attivato
- [ ] ✅ Alert configurati per spazio disco
- [ ] ✅ Resource Monitor QTS verificato

---

## ✅ Conclusione

**🏆 MariaDB 10 su QNAP è la configurazione ottimale per:**
- Sicurezza enterprise-grade
- Performance superiori a MySQL
- Supporto futuro garantito  
- Integrazione perfetta con WordPress
- Gestione semplificata via QTS

**📈 Benefici specifici QNAP:**
- Backup automatici integrati
- Snapshot per rollback istantaneo
- Monitoring via Resource Monitor
- Accesso remoto sicuro
- Scalabilità storage RAID

---

**📞 Supporto tecnico:** massimo.fettucciari@libero.it  
**📅 Prossima review:** Gennaio 2026