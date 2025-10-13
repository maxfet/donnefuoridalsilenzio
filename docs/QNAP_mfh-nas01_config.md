# 🏠 Configurazione MariaDB per WordPress su QNAP mfh-nas01

**Data configurazione:** 9 ottobre 2025  
**Host:** mfh-nas01 (192.168.36.4)  
**SSH configurato:** webadmin@mfh-nas01

---

## ✅ **MariaDB 10 - Configurazione Completa**

### **🔧 Informazioni Sistema**
```bash
Versione MariaDB: 10.5.8-MariaDB-log
Porta: 3307 (non standard)
Binari: /share/CACHEDEV1_DATA/.qpkg/MariaDB10/bin/
Socket: TCP only (non socket Unix)
```

### **🗄️ Database WordPress**
```sql
Database: donnefuori_qnap
Charset: utf8mb4
Collation: utf8mb4_unicode_ci
Status: ✅ Creato e pronto
```

### **👤 Credenziali**
```bash
# Root MariaDB
User: root
Password: WAKr8r*YEMep1fb
Porta: 3307

# WordPress User
User: wp_qnap  
Password: WP_qnap2025!
Database: donnefuori_qnap
Privilegi: SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, ALTER, INDEX, LOCK TABLES, CREATE TEMPORARY TABLES
```

### **⚙️ wp-config.php**
```php
// Database configuration per QNAP
define('DB_NAME', 'donnefuori_qnap');
define('DB_USER', 'wp_qnap');
define('DB_PASSWORD', 'WP_qnap2025!');
define('DB_HOST', '127.0.0.1:3307');
define('DB_CHARSET', 'utf8mb4');
define('DB_COLLATE', 'utf8mb4_unicode_ci');
```

### **🔧 Comandi Utili**

**Connessione Root:**
```bash
ssh webadmin@mfh-nas01
/share/CACHEDEV1_DATA/.qpkg/MariaDB10/bin/mysql \
  -u root -p"WAKr8r*YEMep1fb" \
  --protocol=TCP -h 127.0.0.1 -P 3307
```

**Connessione WordPress:**
```bash
/share/CACHEDEV1_DATA/.qpkg/MariaDB10/bin/mysql \
  -u wp_qnap -p"WP_qnap2025!" \
  --protocol=TCP -h 127.0.0.1 -P 3307 \
  -D donnefuori_qnap
```

**Test Connessione:**
```bash
/share/CACHEDEV1_DATA/.qpkg/MariaDB10/bin/mysql \
  -u wp_qnap -p"WP_qnap2025!" \
  --protocol=TCP -h 127.0.0.1 -P 3307 \
  -D donnefuori_qnap \
  -e "SELECT VERSION(), DATABASE();"
```

### **📊 Verifiche Sistema**
```sql
-- Verifica database
SHOW DATABASES;

-- Verifica utenti
SELECT User, Host FROM mysql.user;

-- Verifica privilegi
SHOW GRANTS FOR 'wp_qnap'@'localhost';

-- Verifica charset
SELECT DEFAULT_CHARACTER_SET_NAME, DEFAULT_COLLATION_NAME 
FROM information_schema.SCHEMATA 
WHERE SCHEMA_NAME = 'donnefuori_qnap';
```

---

## 🚀 **Prossimi Passi per WordPress**

1. **Installazione WordPress su Web Station**
2. **Upload file Duplicator da sito live**
3. **Configurazione URL per ambiente test**
4. **Test funzionalità complete**

---

**📝 Note:**
- SSH key configurata per accesso senza password
- MariaDB 10.5.8 ottimizzato per WordPress
- Database pronto per clone da donnefuoridalsilenzioaps.it
- Porta 3307 da ricordare per connessioni esterne

**🔐 Sicurezza:**
- Utente WordPress con privilegi minimi
- Accesso solo via localhost/127.0.0.1
- Password complesse configurate

---

**📞 Supporto:** massimo.fettucciari@libero.it  
**📅 Configurazione:** 9 ottobre 2025