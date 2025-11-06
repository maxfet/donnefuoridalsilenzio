#!/usr/bin/env python3
"""
Test semplificato Graph API - prova diversi endpoint
"""

import requests
import json

# Carica token
with open('../config/facebook_graph_token.txt', 'r') as f:
    token = f.read().strip()

page_id = "100066348746548"

print("🧪 TEST Graph API - Endpoint diversi")
print("=" * 50)

# Test diversi endpoint
tests = [
    {
        "name": "Info pagina base",
        "url": f"https://graph.facebook.com/{page_id}",
        "params": {"access_token": token}
    },
    {
        "name": "Info pagina + fields",
        "url": f"https://graph.facebook.com/{page_id}",
        "params": {
            "access_token": token,
            "fields": "id,name,about,category"
        }
    },
    {
        "name": "Feed pubblico",
        "url": f"https://graph.facebook.com/{page_id}/feed",
        "params": {"access_token": token, "limit": 5}
    },
    {
        "name": "Posts (standard)",
        "url": f"https://graph.facebook.com/{page_id}/posts",
        "params": {"access_token": token, "limit": 5}
    }
]

for test in tests:
    print(f"\n📡 Test: {test['name']}")
    try:
        response = requests.get(test['url'], params=test['params'])
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Successo! Keys: {list(data.keys())}")
            
            # Mostra primi dati se ci sono post
            if 'data' in data and data['data']:
                print(f"   📄 Trovati {len(data['data'])} elementi")
                first_item = data['data'][0]
                if 'message' in first_item:
                    print(f"   📝 Primo post: {first_item['message'][:100]}...")
                elif 'story' in first_item:
                    print(f"   📖 Storia: {first_item['story'][:100]}...")
        else:
            error_data = response.json() if response.content else {}
            error_msg = error_data.get('error', {}).get('message', 'Unknown error')
            print(f"❌ Errore {response.status_code}: {error_msg}")
            
    except Exception as e:
        print(f"❌ Eccezione: {e}")

print("\n" + "=" * 50)
print("💡 Se tutti falliscono, la pagina potrebbe richiedere permission specifiche")