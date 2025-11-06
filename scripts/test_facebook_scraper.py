#!/usr/bin/env python3
"""
Test script per verificare facebook-scraper con diversi parametri
"""

import sys
from facebook_scraper import get_posts

# Test con pagine pubbliche note
test_pages = [
    "donnefuoridalsilenzio",
    "9gag"  # Pagina di test molto pubblica
]

print("🧪 Test Facebook Scraper - Versione Avanzata")
print("=" * 60)

for page in test_pages:
    print(f"\n📄 Testing pagina: {page}")
    
    # Test 1: Base
    print("   🔍 Test base...")
    try:
        posts = list(get_posts(page, pages=2))
        if posts:
            print(f"   ✅ Trovati {len(posts)} post (base)")
        else:
            print("   ❌ Nessun post (base)")
    except Exception as e:
        print(f"   ❌ Errore base: {e}")
    
    # Test 2: Con extra options
    print("   🔍 Test con extra options...")
    try:
        posts = list(get_posts(
            page, 
            pages=2,
            extra_info=True,
            youtube_dl=False
        ))
        if posts:
            print(f"   ✅ Trovati {len(posts)} post (extra)")
        else:
            print("   ❌ Nessun post (extra)")
    except Exception as e:
        print(f"   ❌ Errore extra: {e}")

print("\n" + "=" * 60)
print("💡 Se tutti i test falliscono, facebook-scraper potrebbe richiedere:")
print("   - Cookies di sessione autenticata")  
print("   - User agent specifici")
print("   - Gestione di rate limiting")
print("   - Aggiornamenti per nuove versioni di Facebook")
print("Test completato!")