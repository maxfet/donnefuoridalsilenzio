# 🏠 Clonazione Sito WordPress su NAS QNAP

**Sito live:** donnefuoridalsilenzioaps.it  
**Ambiente test:** NAS QNAP con WordPress pre-installato  
**Data:** 9 ottobre 2025

---

## 🎯 Vantaggi del NAS QNAP come Ambiente Test

### ✅ **B### **Configurazione Database**

1. **MariaDB 10 Setup (RACCOMANDATO su QNAP):**
   ```sql
   -- Installa MariaDB 10 via App Center QNAP (NON MariaDB 5)
   -- App Center > MariaDB 10 (versione 1.2.1.31+)
   
   -- Crea database per test
   CREATE DATABASE donnefuori_qnap
   CHARACTER SET utf8mb4 
   COLLATE utf8mb4_unicode_ci;
   
   -- Utente dedicato
   CREATE USER 'wp_qnap'@'localhost' IDENTIFIED BY 'password_sicura';
   GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, ALTER, INDEX 
   ON donnefuori_qnap.* TO 'wp_qnap'@'localhost';
   FLUSH PRIVILEGES;
   ```

2. **wp-config.php per QNAP:**
   ```php
   // Database MariaDB 10
   define('DB_NAME', 'donnefuori_qnap');
   define('DB_USER', 'wp_qnap');
   define('DB_PASSWORD', 'password_sicura');
   define('DB_HOST', 'localhost:3306');
   define('DB_CHARSET', 'utf8mb4');
   define('DB_COLLATE', 'utf8mb4_unicode_ci');
   
   // Ottimizzazioni QNAP
   define('DB_TIMEOUT', 60);
   define('WP_POST_REVISIONS', 3);
   define('AUTOSAVE_INTERVAL', 300);
   ``` Specifici:**

- **🔧 WordPress già configurato** - Web Station pronto all'uso
- **🌐 Accesso remoto sicuro** - Disponibile 24/7 per il team
- **💾 Storage dedicato** - Spazio illimitato per backup e test
- **📊 Monitoraggio integrato** - QTS Dashboard per performance
- **🔒 Sicurezza enterprise** - Firewall e controllo accessi
- **⚡ Sempre disponibile** - Server dedicato senza interferenze

---

## 🔧 Configurazione Ambiente QNAP

### **Verifica Prerequisiti QNAP**

1. **Accedi a QTS** (interfaccia QNAP)
2. **Verifica Web Station:**
   ```
   App Center > Web Station > Verifica installazione
   ```

3. **Controlla versioni:**
   ```
   Web Station > Impostazioni generali
   - Apache/Nginx versione
   - PHP versione (minimo 7.4, consigliato 8.0+)
   - MySQL/MariaDB versione
   ```

4. **Verifica WordPress esistente:**
   ```
   Web Station > WordPress > Gestione siti
   ```

### **Configurazione Ottimale PHP**

Accedi a **Web Station > PHP > Impostazioni avanzate:**

```ini
# Impostazioni consigliate per WordPress
upload_max_filesize = 256M
post_max_size = 256M
max_execution_time = 300
memory_limit = 512M
max_input_vars = 5000

# Estensioni necessarie (verificare siano abilitate)
extension=mysqli
extension=gd
extension=curl
extension=zip
extension=xml
extension=mbstring
```

**⚠️ PERCORSI VERIFICATI SU QNAP:**
```bash
# File configurazione PHP principale
/etc/config/php.ini

# File configurazione Apache
/etc/config/apache/apache.conf

# PHP-FPM configuration  
/etc/config/apache/php-fpm.conf
/etc/config/apache/php-fpm-qweb.conf

# Directory PHP aggiuntiva
/etc/config/php.d/

# Per verificare estensioni PHP caricate:
# Accedi via Web Station > PHP > Informazioni
# oppure crea file info.php con: <?php phpinfo(); ?>
```

---

## 📦 Procedura Clonazione su QNAP

### **Metodo 1: Duplicator Plugin (Consigliato)**

#### **Sul sito live (donnefuoridalsilenzioaps.it):**

1. **Installa Duplicator:**
   ```
   Dashboard WordPress > Plugin > Aggiungi nuovo > "Duplicator"
   ```

2. **Crea pacchetto:**
   ```
   Duplicator > Packages > Create New
   ```

3. **Configurazione esclusioni:**
   ```
   Files: 
   - /wp-content/cache/
   - /wp-content/uploads/backup-*
   
   Database:
   - Tabelle cache (se presenti)
   ```

4. **Genera e scarica:**
   - `[site]_archive.zip` (files completi)
   - `installer.php` (script installazione)

#### **Sul NAS QNAP:**

1. **Crea nuovo sito WordPress:**
   ```
   Web Station > WordPress > Crea
   Nome sito: donnefuori-test
   Dominio: [IP-QNAP]/donnefuori-test
   ```

2. **Accedi via File Manager QNAP:**
   ```
   File Station > Web2 > [nome-sito]
   ```

3. **Carica files Duplicator:**
   - Copia `installer.php` nella root
   - Copia `[site]_archive.zip` nella root

4. **Avvia installazione:**
   ```
   Browser: http://[IP-QNAP]/donnefuori-test/installer.php
   ```

5. **Configurazione database:**
   ```
   Host: localhost
   Database: [nome-db-creato-da-QNAP]
   User: [utente-mysql-qnap]
   Password: [password-mysql-qnap]
   ```

### **Metodo 2: Backup Manuale su QNAP**

#### **Download dal sito live:**

1. **Files via FTP/cPanel:**
   ```bash
   # Scarica tutti i files WordPress
   public_html/ → download completo
   ```

2. **Database via phpMyAdmin:**
   ```sql
   Export → Formato SQL → Scarica
   ```

#### **Upload su QNAP:**

1. **Files WordPress:**
   ```
   File Station > Web2 > [sito-test] > Upload files
   ```

2. **Database import:**
   ```
   phpMyAdmin QNAP > Import > Seleziona file .sql
   ```

3. **Modifica wp-config.php:**
   ```php
   // Credenziali database QNAP
   define('DB_NAME', '[database-name-qnap]');
   define('DB_USER', '[mysql-user-qnap]');
   define('DB_PASSWORD', '[mysql-password-qnap]');
   define('DB_HOST', 'localhost');
   
   // URL per ambiente test
   define('WP_HOME','http://[IP-QNAP]/donnefuori-test');
   define('WP_SITEURL','http://[IP-QNAP]/donnefuori-test');
   
   // Debug per testing
   define('WP_DEBUG', true);
   define('WP_DEBUG_LOG', true);
   ```

4. **Aggiorna URL nel database:**
   ```sql
   UPDATE wp_options 
   SET option_value = 'http://[IP-QNAP]/donnefuori-test' 
   WHERE option_name = 'home';
   
   UPDATE wp_options 
   SET option_value = 'http://[IP-QNAP]/donnefuori-test' 
   WHERE option_name = 'siteurl';
   ```

---

## 🔐 Configurazione Accesso e Sicurezza

### **Accesso Interno (Rete Locale)**

```
URL principale QNAP: http://[IP-QNAP]:8080/donnefuori-test
URL alternativo: http://[NOME-QNAP].local/donnefuori-test
Admin WordPress: http://[IP-QNAP]:8080/donnefuori-test/wp-admin
```

**Se configurato dominio esterno (esempio dfds.maxfet.cloud):**
```
URL pubblico: https://dfds.maxfet.cloud
Admin WordPress: https://dfds.maxfet.cloud/wp-admin
```

### **Accesso Esterno (Opzionale)**

1. **Router Port Forwarding:**
   ```
   Porta esterna: 8080
   IP interno: [IP-QNAP]
   Porta interna: 8080
   ```

2. **Dynamic DNS (consigliato):**
   ```
   QNAP > myQNAPcloud > Configura DDNS
   Esempio: donnefuori-test.myqnapcloud.com
   ```

3. **SSL Certificate (per HTTPS):**
   ```
   QTS > Pannello controllo > Sistema > Sicurezza > SSL
   Let's Encrypt gratuito disponibile
   ```

### **Sicurezza QNAP per Test**

```ini
# File .htaccess per protezione
AuthType Basic
AuthName "Area Test Donnefuori"
AuthUserFile /path/to/.htpasswd
Require valid-user

# Blocco accessi non autorizzati
<Files wp-config.php>
Order allow,deny
Deny from all
</Files>
```

---

## 🔄 Workflow di Testing su QNAP

### **Configurazione Ambiente Test**

1. **Database separato per test:**
   ```
   phpMyAdmin > Crea database: donnefuori_test
   Utente dedicato: test_user (permessi limitati)
   ```

2. **Plugin per ambiente test:**
   ```php
   // wp-config.php - Identificazione ambiente
   define('WP_ENVIRONMENT_TYPE', 'development');
   
   // Disabilita plugin produzione
   if (WP_ENVIRONMENT_TYPE === 'development') {
       define('WP_CACHE', false);
       // Disabilita Wordfence, analytics, etc.
   }
   ```

3. **Email testing:**
   ```php
   // Evita invio email reali durante test
   define('WP_MAIL_SMTP_ON', false);
   
   // Log email invece di inviarle
   add_action('wp_mail', 'log_emails_instead_of_sending');
   ```

### **Procedura Testing Standard**

1. **🔄 Sincronizzazione periodica:**
   ```
   Frequenza: Settimanale o prima di modifiche importanti
   Metodo: Duplicator o backup manuale
   ```

2. **🧪 Test delle modifiche:**
   ```
   - Test funzionalità nuove
   - Verifica compatibilità plugin
   - Test responsive design
   - Performance testing
   ```

3. **📋 Checklist pre-deploy:**
   ```
   ✅ Backup sito live completo
   ✅ Test funzionalità critiche
   ✅ Verifica URL e link
   ✅ Controllo errori PHP
   ✅ Test velocità pagina
   ✅ Verifica SEO (Yoast)
   ```

### **Monitoraggio QNAP durante Test**

```
Resource Monitor > CPU, RAM, Network usage
System Logs > Web Server, MySQL errors  
Storage Analytics > Spazio utilizzato
```

---

## 🔧 Configurazioni Specifiche QNAP

### **Ottimizzazione Web Station**

1. **Apache Virtual Hosts:**
   ```apache
   # File: /etc/config/apache/apache.conf
   <VirtualHost *:8080>
       DocumentRoot "/share/Web/donnefuori-test"
       ServerName donnefuori-test.local
       
       <Directory "/share/Web/donnefuori-test">
           AllowOverride All
           Options FollowSymLinks
           Require all granted
       </Directory>
   </VirtualHost>
   ```

2. **MariaDB 10 Optimization (RACCOMANDATO):**
   ```ini
   # File: /share/CACHEDEV1_DATA/.qpkg/MariaDB10/etc/my.cnf
   [mariadb-10.6]
   # QNAP ottimizzazioni specifiche
   innodb_buffer_pool_size = 256M        # Adatta alla RAM QNAP
   innodb_log_file_size = 64M
   innodb_flush_log_at_trx_commit = 2
   
   # Connessioni conservative per NAS
   max_connections = 75
   query_cache_size = 32M
   
   # UTF8MB4 per WordPress
   character_set_server = utf8mb4
   collation_server = utf8mb4_unicode_ci
   
   # Sicurezza QNAP
   bind_address = 127.0.0.1
   local_infile = 0
   
   # SSD optimization
   innodb_flush_neighbors = 0
   innodb_io_capacity = 200
   ```

   **⚠️ IMPORTANTE: Usa MariaDB 10 (v1.2.1.31), NON MariaDB 5**
   - MariaDB 5.x è obsoleto e insicuro (end-of-life 2017)
   - MariaDB 10 offre performance 40% superiori
   - Compatibilità piena con WordPress moderno

3. **PHP OpCache:**
   ```ini
   ; php.ini ottimizzazioni
   opcache.enable=1
   opcache.memory_consumption=128
   opcache.max_accelerated_files=4000
   opcache.validate_timestamps=0
   ```

---

## 📊 Backup e Restore su QNAP

### **Backup Automatici**

1. **Snapshot QNAP:**
   ```
   Storage & Snapshots > Snapshots > 
   Configura snapshot automatici giornalieri
   ```

2. **Backup Database:**
   ```bash
   # Script automatico via cron
   #!/bin/bash
   mysqldump -u [user] -p[pass] donnefuori_test > /share/backup/db_$(date +%Y%m%d).sql
   ```

3. **Backup Files:**
   ```bash
   # Rsync periodico
   rsync -av /share/Web/donnefuori-test/ /share/backup/site_$(date +%Y%m%d)/
   ```

### **Restore Procedure**

1. **Da Snapshot:**
   ```
   Storage & Snapshots > Ripristina da snapshot
   ```

2. **Da Backup manuale:**
   ```bash
   # Restore database
   mysql -u [user] -p[pass] donnefuori_test < backup_file.sql
   
   # Restore files
   cp -r /share/backup/site_backup/* /share/Web/donnefuori-test/
   ```

---

## 🔍 Troubleshooting QNAP

### **Problemi Comuni e Soluzioni**

1. **Errore 500 - Internal Server Error:**
   ```bash
   # Controlla log Apache
   tail -f /var/log/apache2/error.log
   
   # Verifica permessi files
   chown -R httpdusr:everyone /share/Web/donnefuori-test/
   chmod -R 755 /share/Web/donnefuori-test/
   ```

2. **MySQL Connection Error:**
   ```sql
   -- Verifica utente database
   SHOW GRANTS FOR 'user'@'localhost';
   
   -- Ricrea utente se necessario
   CREATE USER 'test_user'@'localhost' IDENTIFIED BY 'password';
   GRANT ALL PRIVILEGES ON donnefuori_test.* TO 'test_user'@'localhost';
   ```

3. **Memoria PHP insufficiente:**
   ```ini
   ; php.ini
   memory_limit = 512M
   max_execution_time = 300
   ```

4. **Upload files troppo grandi:**
   ```ini
   ; php.ini
   upload_max_filesize = 256M
   post_max_size = 256M
   ```

---

## 📱 Accesso Mobile e Team

### **Configurazione Accesso Team**

1. **App QNAP Mobile:**
   ```
   Qfile, Qmanager per gestione files
   myQNAPcloud per accesso esterno
   ```

2. **VPN Access:**
   ```
   QVPN Service per accesso sicuro esterno
   OpenVPN o L2TP configurazione
   ```

3. **Condivisione Credenziali:**
   ```
   URL test: http://[IP-QNAP]:8080/donnefuori-test
   Admin WP: test_admin / [password-sicura]
   Database: test_user / [password-db]
   ```

---

## 📋 Checklist Setup Completo

### **Prima Configurazione:**
- [ ] ✅ Verificata installazione Web Station
- [ ] ✅ Configurato PHP ottimale (8.0+)
- [ ] ✅ Creato database test dedicato
- [ ] ✅ Configurato accesso sicuro
- [ ] ✅ Testata connettività interna/esterna

### **Clonazione Sito:**
- [ ] ✅ Backup completo sito live
- [ ] ✅ Upload files via Duplicator/manuale
- [ ] ✅ Import database completato
- [ ] ✅ Aggiornati URL nel database
- [ ] ✅ Configurato wp-config.php

### **Testing Environment:**
- [ ] ✅ Disabilitati plugin produzione
- [ ] ✅ Configurato debug WordPress
- [ ] ✅ Impostato backup automatico
- [ ] ✅ Verificato accesso team
- [ ] ✅ Documentato workflow testing

---

**🏠 Ambiente QNAP pronto per testing sicuro e professionale!**

**📞 Supporto tecnico:** massimo.fettucciari@libero.it  
**📅 Ultimo aggiornamento:** 9 ottobre 2025