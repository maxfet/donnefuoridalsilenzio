#!/usr/bin/env python3
"""
GUIDA: Setup Facebook Graph API per Donne Fuori Dal Silenzio
Procedura completa per ottenere Access Token
"""

print("🚀 FACEBOOK GRAPH API SETUP - Guida Completa")
print("=" * 70)
print()

print("👤 PREREQUISITI:")
print("✅ Account Facebook personale (il tuo)")
print("✅ Seguire la pagina 'Donne Fuori Dal Silenzio Ciampino'")
print("✅ Browser web")
print()

print("📋 PASSO 1 - Creare App Facebook Developer")
print("1. Vai su: https://developers.facebook.com/")
print("2. Fai login con il tuo account Facebook")
print("3. Clicca 'My Apps' > 'Create App'")
print("4. Scegli 'Other' > 'Next'")
print("5. Nome app: 'Scraper Donne Fuori Dal Silenzio'")
print("6. Email: la tua email")
print("7. Clicca 'Create App'")
print()

print("📋 PASSO 2 - Generare Access Token")
print("1. Nell'app creata, vai su 'Tools' > 'Graph API Explorer'")
print("2. Seleziona la tua app dal dropdown")
print("3. Clicca 'Generate Access Token'")
print("4. Autorizza le permission richieste")
print("5. COPIA il token generato (inizia con 'EAAG...')")
print()

print("📋 PASSO 3 - Trovare Page ID")
print("1. Vai su: https://www.facebook.com/donnefuoridalsilenziociampino")
print("2. Clicca destro > 'Visualizza sorgente pagina'")
print("3. Cerca 'page_id' o 'entity_id'")
print("4. Oppure usa Graph API Explorer:")
print("   - Query: ?id=https://www.facebook.com/donnefuoridalsilenziociampino")
print("   - Ti darà l'ID numerico")
print()

print("📋 PASSO 4 - Testare API")
print("1. In Graph API Explorer:")
print("2. Query: {PAGE_ID}/posts")
print("3. Se vedi i post, tutto funziona!")
print()

print("🔐 SICUREZZA:")
print("- Il token è personale e sensibile")
print("- Ha scadenza (default: 1-2 ore)")
print("- Può essere esteso a 60 giorni")
print("- Non condividerlo mai")
print()

print("💾 DOVE SALVARE:")
print("- config/facebook_graph_token.txt")
print("- config/facebook_page_id.txt")
print()

print("🎯 PROSSIMO PASSO:")
print("Dopo aver ottenuto token e page ID, esegui:")
print("python3 facebook_graph_scraper.py")