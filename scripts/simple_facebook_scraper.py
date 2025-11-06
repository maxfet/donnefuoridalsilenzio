#!/usr/bin/env python3
"""
Scraper alternativo per Facebook usando requests + cookies
Approccio diretto senza dipendere da facebook-scraper
"""

import requests
import json
from pathlib import Path
import logging
from bs4 import BeautifulSoup
import re

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SimpleFacebookScraper:
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.cookies_file = self.project_root / "config" / "facebook_cookies.json"
        self.session = requests.Session()
        
        # User agent realistico
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'it-IT,it;q=0.9,en;q=0.8',
        })
        
        self.load_cookies()
        
    def load_cookies(self):
        """Carica cookies dal file JSON"""
        try:
            with open(self.cookies_file, 'r') as f:
                cookies_data = json.load(f)
                
            # Converti in formato requests
            for key, value in cookies_data.items():
                if not key.startswith('_'):  # Salta commenti
                    self.session.cookies.set(key, str(value), domain='.facebook.com')
                    
            logger.info(f"✅ Caricati {len(self.session.cookies)} cookies")
            return True
        except Exception as e:
            logger.error(f"❌ Errore caricando cookies: {e}")
            return False
    
    def test_login(self):
        """Verifica se i cookies funzionano"""
        try:
            response = self.session.get('https://www.facebook.com/')
            
            if 'login' in response.url.lower():
                logger.error("❌ Cookies non validi - redirect al login")
                return False
            
            # Cerca il tuo nome nella pagina
            if 'massimo' in response.text.lower() or 'fettucciari' in response.text.lower():
                logger.info("✅ Login verificato - cookies validi!")
                return True
            
            logger.warning("⚠️ Login incerto - potrebbe funzionare")
            return True
            
        except Exception as e:
            logger.error(f"❌ Errore test login: {e}")
            return False
    
    def get_page_url(self, page_name):
        """Ottieni URL della pagina"""
        return f"https://www.facebook.com/{page_name}"
    
    def scrape_page(self, page_name="donnefuoridalsilenziociampino"):
        """Scraping base della pagina"""
        logger.info(f"🚀 Scaricando pagina: {page_name}")
        
        url = self.get_page_url(page_name)
        
        try:
            response = self.session.get(url)
            logger.info(f"📡 Status: {response.status_code}")
            
            if response.status_code == 200:
                # Salva HTML per debug
                html_file = self.project_root / "Post-facebook" / "page_source.html"
                html_file.parent.mkdir(exist_ok=True)
                html_file.write_text(response.text, encoding='utf-8')
                logger.info(f"💾 HTML salvato in: {html_file}")
                
                # Cerca pattern di post
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Cerca elementi comuni nei post
                articles = soup.find_all(['article', 'div'], attrs={'data-ad-preview': True})
                logger.info(f"📝 Trovati {len(articles)} potenziali post")
                
                # Estrai testo visibile
                text_content = soup.get_text()
                
                # Cerca menzioni della pagina
                mentions = re.findall(r'donne fuori dal silenzio', text_content, re.IGNORECASE)
                logger.info(f"🔍 Trovate {len(mentions)} menzioni della pagina")
                
                return {
                    'status': 'success',
                    'url': url,
                    'html_saved': str(html_file),
                    'potential_posts': len(articles),
                    'mentions': len(mentions)
                }
            else:
                logger.error(f"❌ Errore HTTP: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"❌ Errore scraping: {e}")
            return None

if __name__ == "__main__":
    print("🧪 Test Scraper Alternativo Facebook")
    print("=" * 60)
    
    scraper = SimpleFacebookScraper()
    
    # Test login
    if scraper.test_login():
        # Prova scraping
        result = scraper.scrape_page()
        
        if result:
            print("\n✅ RISULTATI:")
            print(f"  URL: {result['url']}")
            print(f"  HTML salvato: {result['html_saved']}")
            print(f"  Potenziali post: {result['potential_posts']}")
            print(f"  Menzioni: {result['mentions']}")
            print("\n💡 Controlla il file HTML salvato per vedere cosa viene scaricato")
    else:
        print("\n❌ I cookies non sono validi - aggiornali!")
    
    print("=" * 60)