#!/usr/bin/env python3
"""
Test avanzato per debug Facebook scraper con diversi parametri
"""

import sys
from facebook_scraper import get_posts
import json

# Carica cookies
def load_cookies():
    try:
        with open('../config/facebook_cookies.json', 'r') as f:
            return json.load(f)
    except:
        return None

print("🔍 DEBUG Facebook Scraper - Test Avanzato")
print("=" * 60)

cookies = load_cookies()
if cookies:
    print("✅ Cookies caricati")
else:
    print("❌ Nessun cookies")

# Test con diversi nomi e parametri
test_configs = [
    {
        "name": "donnefuoridalsilenziociampino",
        "desc": "Nome completo pagina"
    },
    {
        "name": "100064896891856",  # Esempio di Page ID numerico
        "desc": "Page ID numerico (se conosci l'ID)"
    }
]

for config in test_configs:
    page_name = config["name"]
    print(f"\n📄 Test: {page_name} ({config['desc']})")
    
    try:
        # Test con parametri diversi
        print("   🔍 Test standard...")
        posts = list(get_posts(
            page_name, 
            pages=3,
            cookies=cookies if cookies else None
        ))
        
        if posts:
            print(f"   ✅ Trovati {len(posts)} post!")
            post = posts[0]
            print(f"   📝 Primo post: {post.get('text', 'N/A')[:100]}")
            break
        else:
            print("   ❌ Nessun post")
            
    except Exception as e:
        print(f"   ❌ Errore: {e}")

print(f"\n💡 SUGGERIMENTI:")
print("1. Verifica che la pagina sia pubblica")
print("2. Prova a trovare il Page ID numerico della pagina")
print("3. Alcuni social network bloccano tutti gli scraper")
print("4. Considera alternative come RSS feed o API ufficiali")