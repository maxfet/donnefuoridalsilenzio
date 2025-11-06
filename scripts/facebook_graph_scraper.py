#!/usr/bin/env python3
"""
Facebook Graph API Scraper per Donne Fuori Dal Silenzio
Utilizza l'API ufficiale Facebook per scaricare post pubblici
"""

import requests
import json
import os
from pathlib import Path
import time
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class FacebookGraphScraper:
    def __init__(self):
        """Inizializza scraper Graph API"""
        self.project_root = Path(__file__).parent.parent
        self.output_dir = self.project_root / "Post-facebook"
        self.media_dir = self.output_dir / "media"
        
        # File di configurazione
        self.token_file = self.project_root / "config" / "facebook_graph_token.txt"
        self.page_id_file = self.project_root / "config" / "facebook_page_id.txt"
        self.posts_file = self.output_dir / "posts_graph_api.json"
        
        # Crea directory
        self.output_dir.mkdir(exist_ok=True)
        self.media_dir.mkdir(exist_ok=True)
        
        # Carica configurazione
        self.access_token = self.load_access_token()
        self.page_id = self.load_page_id()
        
        # Lista post
        self.posts_data = []
        
        logger.info("🚀 Facebook Graph API Scraper inizializzato")
        logger.info(f"📁 Output: {self.output_dir}")
        
    def load_access_token(self):
        """Carica access token da file"""
        if self.token_file.exists():
            token = self.token_file.read_text().strip()
            logger.info("✅ Access token caricato")
            return token
        else:
            logger.error("❌ File access token non trovato!")
            logger.info(f"💡 Crea file: {self.token_file}")
            return None
    
    def load_page_id(self):
        """Carica page ID da file"""
        if self.page_id_file.exists():
            page_id = self.page_id_file.read_text().strip()
            logger.info(f"✅ Page ID caricato: {page_id}")
            return page_id
        else:
            logger.warning("⚠️ File page ID non trovato - usando nome pagina")
            return "donnefuoridalsilenziociampino"
    
    def test_token(self):
        """Testa se l'access token è valido"""
        if not self.access_token:
            return False
            
        url = "https://graph.facebook.com/me"
        params = {
            'access_token': self.access_token
        }
        
        try:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                logger.info(f"✅ Token valido - User: {data.get('name', 'N/A')}")
                return True
            else:
                logger.error(f"❌ Token non valido: {response.text}")
                return False
        except Exception as e:
            logger.error(f"❌ Errore test token: {e}")
            return False
    
    def get_page_posts(self, limit=25):
        """Scarica post dalla pagina usando Graph API"""
        if not self.access_token:
            logger.error("❌ Access token mancante")
            return []
            
        # Prova prima con endpoint feed (meno restrittivo)
        url = f"https://graph.facebook.com/{self.page_id}/feed"
        
        # Usa campi base che non richiedono permission speciali
        params = {
            'access_token': self.access_token,
            'fields': 'id,message,created_time,story,permalink_url,from',
            'limit': limit
        }
        
        try:
            logger.info(f"📡 Scaricando post da pagina ID: {self.page_id}")
            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                posts = data.get('data', [])
                logger.info(f"✅ Scaricati {len(posts)} post")
                return posts
            else:
                logger.error(f"❌ Errore API: {response.status_code}")
                logger.error(f"Risposta: {response.text}")
                return []
                
        except Exception as e:
            logger.error(f"❌ Errore richiesta: {e}")
            return []
    
    def process_post(self, post):
        """Processa un singolo post"""
        try:
            post_id = post.get('id', '')
            
            # Estrai dati del post
            processed_post = {
                'post_id': post_id,
                'message': post.get('message', ''),
                'created_time': post.get('created_time', ''),
                'updated_time': post.get('updated_time', ''),
                'permalink_url': post.get('permalink_url', ''),
                'likes_count': post.get('likes', {}).get('summary', {}).get('total_count', 0),
                'comments_count': post.get('comments', {}).get('summary', {}).get('total_count', 0),
                'shares_count': post.get('shares', {}).get('count', 0),
                'attachments': [],
                'scraped_at': datetime.now().isoformat()
            }
            
            # Processa allegati (immagini/video)
            attachments = post.get('attachments', {}).get('data', [])
            for attachment in attachments:
                media_info = {
                    'type': attachment.get('type', ''),
                    'url': attachment.get('url', ''),
                    'title': attachment.get('title', ''),
                    'description': attachment.get('description', '')
                }
                
                # Aggiungi info media se presente
                if 'media' in attachment:
                    media_info['media_url'] = attachment['media'].get('image', {}).get('src', '')
                    
                processed_post['attachments'].append(media_info)
            
            logger.info(f"✅ Post processato: {post_id}")
            return processed_post
            
        except Exception as e:
            logger.error(f"❌ Errore processando post: {e}")
            return None
    
    def scrape_posts(self, limit=25):
        """Funzione principale per scaricare i post"""
        logger.info("🚀 === INIZIO SCRAPING GRAPH API ===")
        
        # Test token
        if not self.test_token():
            logger.error("❌ Token non valido - interrompo")
            return
        
        # Scarica post
        posts = self.get_page_posts(limit)
        
        if not posts:
            logger.warning("⚠️ Nessun post scaricato")
            return
        
        # Processa ogni post
        for post in posts:
            processed_post = self.process_post(post)
            if processed_post:
                self.posts_data.append(processed_post)
        
        # Salva risultati
        self.save_posts()
        
        logger.info("✅ === SCRAPING COMPLETATO ===")
        logger.info(f"📊 Post raccolti: {len(self.posts_data)}")
    
    def save_posts(self):
        """Salva i post in file JSON"""
        try:
            with open(self.posts_file, 'w', encoding='utf-8') as f:
                json.dump(self.posts_data, f, indent=2, ensure_ascii=False)
            logger.info(f"💾 Post salvati in: {self.posts_file}")
        except Exception as e:
            logger.error(f"❌ Errore salvando post: {e}")

if __name__ == "__main__":
    scraper = FacebookGraphScraper()
    scraper.scrape_posts(limit=10)  # Scarica gli ultimi 10 post
    
    print("\n" + "="*60)
    print("✅ Scraping Graph API completato!")
    print(f"📁 Controlla: {scraper.output_dir}")
    print(f"📄 File JSON: {scraper.posts_file}")
    print("="*60)