# 🗄️ MariaDB vs MySQL per WordPress - Guida Completa

**Ambiente:** dfds.maxfet.cloud  
**WordPress:** donnefuoridalsilenzioaps.it clone  
**Data:** 9 ottobre 2025

---

## ✅ **Risposta Diretta: SÌ, MariaDB è Perfetto!**

**MariaDB è non solo compatibile, ma spesso preferibile a MySQL per WordPress.**

---

## 🎯 Confronto MySQL vs MariaDB

### **📊 Tabella Comparativa**

| Aspetto | MySQL | MariaDB | Vincitore |
|---------|-------|---------|-----------|
| **Compatibilità WordPress** | ✅ Nativa | ✅ Completa | 🤝 Pari |
| **Performance** | ⭐⭐⭐ | ⭐⭐⭐⭐ | 🏆 MariaDB |
| **Sicurezza** | ⭐⭐⭐ | ⭐⭐⭐⭐ | 🏆 MariaDB |
| **Licenza** | GPL + Commercial | GPL Pura | 🏆 MariaDB |
| **Storage Engines** | InnoDB, MyISAM | InnoDB, Aria, ColumnStore+ | 🏆 MariaDB |
| **Sviluppo Attivo** | Oracle-controlled | Community-driven | 🏆 MariaDB |
| **Costo** | Gratis (licenza dual) | Totalmente gratis | 🏆 MariaDB |

### **🚀 Vantaggi Specifici MariaDB per WordPress**

1. **Performance WordPress:**
   - Query SELECT fino al 15% più veloci
   - Ottimizzazioni specifiche per CMS
   - Migliore gestione di tabelle grandi (wp_posts, wp_postmeta)

2. **Sicurezza Avanzata:**
   - Crittografia at-rest nativa
   - Plugin di autenticazione avanzati
   - Audit logging integrato

3. **Storage Engines:**
   - **Aria:** Alternativa a MyISAM più robusta
   - **ColumnStore:** Per analytics e reporting
   - **Spider:** Per sharding automatico

4. **Funzionalità WordPress-friendly:**
   - JSON migliore supporto (WordPress 5.0+)
   - Full-text search migliorato
   - Virtual columns per metadati

---

## 🔧 Installazione MariaDB per dfds.maxfet.cloud

### **Ubuntu/Debian (Raccomandato)**

```bash
# Aggiorna repository
sudo apt update

# Installa MariaDB server
sudo apt install mariadb-server mariadb-client

# Verifica installazione
sudo systemctl status mariadb

# Sicurezza iniziale
sudo mysql_secure_installation
```

### **CentOS/RHEL/Fedora**

```bash
# CentOS 8+/RHEL 8+
sudo dnf install mariadb-server mariadb

# CentOS 7/RHEL 7
sudo yum install mariadb-server mariadb

# Avvia servizi
sudo systemctl start mariadb
sudo systemctl enable mariadb
```

### **Arch Linux**

```bash
# Installa MariaDB
sudo pacman -S mariadb

# Inizializza database
sudo mysql_install_db --user=mysql --basedir=/usr --datadir=/var/lib/mysql

# Avvia servizio
sudo systemctl start mariadb
sudo systemctl enable mariadb
```

---

## ⚙️ Configurazione Ottimale WordPress

### **1. Creazione Database WordPress**

```sql
-- Connessione come root
mysql -u root -p

-- Crea database con ottimizzazioni WordPress
-- Per ambiente locale
CREATE DATABASE donnefuori_locale 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

-- Per server test (QNAP/dfds.maxfet.cloud)
CREATE DATABASE donnefuori_test 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

-- Per ambiente QNAP specifico
CREATE DATABASE donnefuori_qnap
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

-- Utenti dedicati per diversi ambienti
-- Locale
CREATE USER 'wp_locale'@'localhost' IDENTIFIED BY 'password_locale';
GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, ALTER, INDEX, LOCK TABLES, CREATE TEMPORARY TABLES 
ON donnefuori_locale.* TO 'wp_locale'@'localhost';

-- Test server (dfds.maxfet.cloud)
CREATE USER 'wp_test'@'localhost' IDENTIFIED BY 'password_test_sicura';
GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, ALTER, INDEX, LOCK TABLES, CREATE TEMPORARY TABLES 
ON donnefuori_test.* TO 'wp_test'@'localhost';

-- QNAP
CREATE USER 'wp_qnap'@'localhost' IDENTIFIED BY 'password_qnap_sicura';
GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, ALTER, INDEX, LOCK TABLES, CREATE TEMPORARY TABLES 
ON donnefuori_qnap.* TO 'wp_qnap'@'localhost';

-- Privilegi specifici WordPress (principio least privilege)
GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, ALTER, INDEX, LOCK TABLES, CREATE TEMPORARY TABLES 
ON donnefuori_test.* TO 'wp_dfds'@'localhost';

-- Privilegi aggiuntivi per plugin avanzati (opzionale)
GRANT CREATE ROUTINE, ALTER ROUTINE, EXECUTE 
ON donnefuori_test.* TO 'wp_dfds'@'localhost';

FLUSH PRIVILEGES;

-- Verifica creazione
SHOW DATABASES LIKE 'donnefuori_test';
SHOW GRANTS FOR 'wp_dfds'@'localhost';
```

### **2. Configurazione my.cnf Ottimizzata**

```ini
# /etc/mysql/mariadb.conf.d/50-wordpress.cnf
[mariadb]

# === PRESTAZIONI WORDPRESS ===
# Buffer pool (70% RAM disponibile per server dedicato)
innodb_buffer_pool_size = 512M
innodb_buffer_pool_instances = 2

# Log files (25% del buffer pool)
innodb_log_file_size = 128M
innodb_log_buffer_size = 32M
innodb_flush_log_at_trx_commit = 2

# Connessioni
max_connections = 200
max_user_connections = 190
thread_cache_size = 50

# Query cache (utile per WordPress)
query_cache_type = 1
query_cache_size = 64M
query_cache_limit = 4M

# Tabelle
table_open_cache = 4096
table_definition_cache = 2048
open_files_limit = 8192

# === CHARSET WORDPRESS ===
character_set_server = utf8mb4
collation_server = utf8mb4_unicode_ci
innodb_default_row_format = dynamic
innodb_file_format = Barracuda

# === SICUREZZA ===
local_infile = 0
symbolic_links = 0
secure_file_priv = NULL
skip_name_resolve = 1

# === LOGGING PER DEBUG ===
slow_query_log = 1
slow_query_log_file = /var/log/mysql/slow.log
long_query_time = 2
log_queries_not_using_indexes = 1

# === OTTIMIZZAZIONI SPECIFICHE ===
# Per wp_options (autoload)
tmp_table_size = 64M
max_heap_table_size = 64M

# Per wp_posts ricerche
ft_min_word_len = 3
ft_boolean_syntax = '+ -><()~*:""&|'

[mysql]
default_character_set = utf8mb4

[mysqldump]
default_character_set = utf8mb4
single_transaction = 1
routines = 1
triggers = 1
```

### **3. wp-config.php per MariaDB**

```php
<?php
// === CONFIGURAZIONE DATABASE MARIADB ===
define('DB_NAME', 'donnefuori_test');
define('DB_USER', 'wp_dfds');
define('DB_PASSWORD', 'password_super_sicura');
define('DB_HOST', 'localhost');

// Charset ottimizzato per MariaDB
define('DB_CHARSET', 'utf8mb4');
define('DB_COLLATE', 'utf8mb4_unicode_ci');

// === OTTIMIZZAZIONI MARIADB ===
// Cache oggetti (se disponibile Redis/Memcached)
define('WP_CACHE', true);

// Revisioni (limita crescita wp_posts)
define('WP_POST_REVISIONS', 5);
define('AUTOSAVE_INTERVAL', 300);

// Trash cleanup
define('EMPTY_TRASH_DAYS', 7);
define('MEDIA_TRASH', true);

// Database repair (solo per debug)
// define('WP_ALLOW_REPAIR', true);

// === OTTIMIZZAZIONI QUERY ===
// Aumenta memoria per query complesse
ini_set('memory_limit', '512M');

// Timeout per connessioni lunghe
define('DB_TIMEOUT', 30);

// === AMBIENTE TEST ===
define('WP_ENVIRONMENT_TYPE', 'staging');
define('WP_DEBUG', true);
define('WP_DEBUG_LOG', true);
define('WP_DEBUG_DISPLAY', false);

// Il resto della configurazione WordPress...
```

---

## 📈 Monitoring e Ottimizzazione

### **Query Performance Analysis**

```sql
-- Abilita performance schema
SET GLOBAL performance_schema = ON;

-- Query più lente
SELECT 
    DIGEST_TEXT as query,
    COUNT_STAR as exec_count,
    AVG_TIMER_WAIT/1000000000 as avg_time_sec,
    SUM_TIMER_WAIT/1000000000 as total_time_sec
FROM performance_schema.events_statements_summary_by_digest 
ORDER BY total_time_sec DESC 
LIMIT 10;

-- Tabelle più utilizzate
SELECT 
    OBJECT_SCHEMA,
    OBJECT_NAME,
    COUNT_READ,
    COUNT_WRITE,
    COUNT_READ + COUNT_WRITE as total_io
FROM performance_schema.table_io_waits_summary_by_table 
WHERE OBJECT_SCHEMA = 'donnefuori_test'
ORDER BY total_io DESC;
```

### **WordPress Specific Monitoring**

```sql
-- Analisi wp_options (spesso collo di bottiglia)
SELECT 
    option_name,
    LENGTH(option_value) as size_bytes,
    autoload
FROM wp_options 
WHERE autoload = 'yes' 
ORDER BY size_bytes DESC 
LIMIT 20;

-- Query su wp_postmeta (performance critica)
SELECT 
    meta_key,
    COUNT(*) as count,
    AVG(LENGTH(meta_value)) as avg_size
FROM wp_postmeta 
GROUP BY meta_key 
ORDER BY count DESC 
LIMIT 15;

-- Analisi wp_posts per type
SELECT 
    post_type,
    post_status,
    COUNT(*) as count
FROM wp_posts 
GROUP BY post_type, post_status;
```

---

## 🔧 Tools Utili MariaDB + WordPress

### **1. MySQLTuner per MariaDB**

```bash
# Installa MySQLTuner
wget http://mysqltuner.pl/ -O mysqltuner.pl
chmod +x mysqltuner.pl

# Analizza configurazione
./mysqltuner.pl

# Con credenziali specifiche
./mysqltuner.pl --user wp_dfds --pass password --database donnefuori_test
```

### **2. Plugin WordPress per MariaDB**

**Query Monitor:** Analisi query in tempo reale
```bash
wp plugin install query-monitor --activate
```

**WP-Optimize:** Pulizia database specifica MariaDB
```bash
wp plugin install wp-optimize --activate
```

**WP-DBManager:** Gestione avanzata database
```bash
wp plugin install wp-dbmanager --activate
```

### **3. Script Manutenzione Automatica**

```bash
#!/bin/bash
# /home/user/scripts/mariadb_maintenance.sh

DB_NAME="donnefuori_test"
DB_USER="wp_dfds"
DB_PASS="password"

echo "=== MANUTENZIONE MARIADB WORDPRESS ==="
echo "Database: $DB_NAME"
echo "Data: $(date)"

# Ottimizza tabelle WordPress principali
mysql -u $DB_USER -p$DB_PASS $DB_NAME << EOF
OPTIMIZE TABLE wp_posts;
OPTIMIZE TABLE wp_postmeta;
OPTIMIZE TABLE wp_options;
OPTIMIZE TABLE wp_comments;
OPTIMIZE TABLE wp_commentmeta;
OPTIMIZE TABLE wp_users;
OPTIMIZE TABLE wp_usermeta;
EOF

# Pulizia spam e trash
mysql -u $DB_USER -p$DB_PASS $DB_NAME << EOF
DELETE FROM wp_comments WHERE comment_approved = 'spam';
DELETE FROM wp_posts WHERE post_status = 'trash' AND post_modified < DATE_SUB(NOW(), INTERVAL 30 DAY);
DELETE FROM wp_postmeta WHERE post_id NOT IN (SELECT id FROM wp_posts);
DELETE FROM wp_commentmeta WHERE comment_id NOT IN (SELECT comment_ID FROM wp_comments);
EOF

# Analizza tabelle
mysql -u $DB_USER -p$DB_PASS $DB_NAME << EOF
ANALYZE TABLE wp_posts, wp_postmeta, wp_options, wp_comments;
EOF

echo "Manutenzione completata: $(date)"
```

---

## 🔄 Migrazione MySQL → MariaDB

### **Procedura Sicura per dfds.maxfet.cloud**

```bash
# 1. BACKUP COMPLETO MySQL esistente
mysqldump -u root -p --single-transaction --routines --triggers --events \
  donnefuori_test > backup_mysql_$(date +%Y%m%d).sql

# 2. Verifica backup
mysql -u root -p -e "SELECT COUNT(*) FROM wp_posts" donnefuori_test

# 3. Stop MySQL
sudo systemctl stop mysql

# 4. Installa MariaDB (mantiene dati in /var/lib/mysql)
sudo apt remove mysql-server mysql-client
sudo apt install mariadb-server mariadb-client

# 5. Aggiorna system tables
sudo mysql_upgrade -u root -p

# 6. Verifica migrazione
mysql -u root -p -e "SELECT VERSION();"
mysql -u root -p -e "SELECT COUNT(*) FROM wp_posts" donnefuori_test

# 7. Test WordPress
curl -I https://dfds.maxfet.cloud
```

---

## 🆘 Troubleshooting MariaDB + WordPress

### **Problema: WordPress non si connette dopo migrazione**

```php
// Test connessione in wp-config.php
// Esempi per diversi ambienti:

// Locale
$test = new mysqli('localhost', 'wp_locale', 'password_locale', 'donnefuori_locale');

// Test server (dfds.maxfet.cloud)  
$test = new mysqli('localhost', 'wp_test', 'password_test_sicura', 'donnefuori_test');

// QNAP
$test = new mysqli('localhost', 'wp_qnap', 'password_qnap_sicura', 'donnefuori_qnap');

if ($test->connect_error) {
    die('Connection failed: ' . $test->connect_error);
} else {
    echo 'MariaDB connection successful!';
}
$test->close();
```

### **Problema: Charset errors dopo migrazione**

```sql
-- Verifica e correggi charset
SELECT 
    TABLE_NAME,
    TABLE_COLLATION
FROM information_schema.TABLES 
WHERE TABLE_SCHEMA = 'donnefuori_test';

-- Converti tutte le tabelle
ALTER TABLE wp_posts CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE wp_postmeta CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
-- Ripeti per tutte le tabelle WordPress
```

### **Problema: Performance degradate**

```sql
-- Ricostruisci statistiche
ANALYZE TABLE wp_posts, wp_postmeta, wp_options;

-- Verifica indici
SHOW INDEX FROM wp_posts;
SHOW INDEX FROM wp_postmeta;

-- Ricostruisci se necessario
ALTER TABLE wp_postmeta DROP INDEX meta_key, ADD INDEX meta_key (meta_key(191));
```

---

## 📊 Benchmark MariaDB vs MySQL

### **Test Performance WordPress**

```bash
# Install WordPress benchmarking
wp package install git@github.com:wp-cli/profile-command.git

# Test database performance
wp profile stage --all --spotlight

# Query timing comparison
time wp db query "SELECT COUNT(*) FROM wp_posts WHERE post_status = 'publish'"
```

### **Risultati Tipici per WordPress**

```
MariaDB 10.6:
- SELECT queries: ~15% più veloci
- INSERT/UPDATE: ~10% più veloci  
- Complex JOINs: ~20% più veloci
- Full-text search: ~25% più veloci

Memoria:
- Buffer pool efficiency: +5-10%
- Query cache hit rate: +8-12%
```

---

## ✅ Raccomandazione Finale

**🏆 Per dfds.maxfet.cloud consiglio vivamente MariaDB:**

1. **Performance superiori** per WordPress
2. **Sicurezza avanzata** out-of-the-box
3. **Licenza più libera** (GPL pura)
4. **Sviluppo più attivo** della community
5. **Compatibilità perfetta** con tutto l'ecosistema WordPress

**📅 Roadmap suggerita:**
- **Immediate:** Installa MariaDB 10.6+ o 10.11 LTS
- **Configurazione:** Usa la configurazione ottimizzata fornita
- **Monitoring:** Implementa script manutenzione automatica
- **Futuro:** Considera storage engine Aria per tabelle log

---

**📞 Supporto tecnico MariaDB:** massimo.fettucciari@libero.it  
**📅 Documento aggiornato:** 9 ottobre 2025