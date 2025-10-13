#!/usr/bin/env python3
"""
Script per scaricare post da Facebook della pagina "Donne Fuori Dal Silenzio"
Utilizza facebook-scraper per ottenere testo e media dei post
Salva i dati in formato JSON nella cartella locale Post-facebook

Data creazione: 13 ottobre 2025
Autore: GitHub Copilot per Donne Fuori Dal Silenzio
"""

import os
import json
import datetime
from pathlib import Path
from facebook_scraper import get_posts
import requests
from urllib.parse import urlparse
import time
import logging

# Configurazione logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('facebook_scraper.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class DonneFuoriScraper:
    def __init__(self):
        """Inizializza lo scraper per Donne Fuori Dal Silenzio"""
        self.page_name = "donnefuoridalsilenziociampino"  # Nome pagina Facebook
        self.output_dir = Path("Post-facebook")
        self.media_dir = self.output_dir / "media"
        self.posts_file = self.output_dir / "posts.json"
        
        # Crea le directory se non esistono
        self.output_dir.mkdir(exist_ok=True)
        self.media_dir.mkdir(exist_ok=True)
        
        # Lista per raccogliere tutti i post
        self.posts_data = []
        
        logger.info(f"Inizializzato scraper per pagina: {self.page_name}")
        logger.info(f"Directory output: {self.output_dir.absolute()}")

    def download_media(self, media_url, post_id, media_type="image"):
        """
        Scarica media (immagini/video) da un post
        
        Args:
            media_url (str): URL del media da scaricare
            post_id (str): ID del post per naming del file
            media_type (str): Tipo di media ('image' o 'video')
            
        Returns:
            str: Path locale del file scaricato o None se errore
        """
        try:
            if not media_url:
                return None
                
            # Determina estensione file dall'URL
            parsed_url = urlparse(media_url)
            extension = Path(parsed_url.path).suffix
            if not extension:
                extension = '.jpg' if media_type == 'image' else '.mp4'
            
            # Nome file basato su post_id e timestamp
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{post_id}_{timestamp}_{media_type}{extension}"
            filepath = self.media_dir / filename
            
            # Download del file
            logger.info(f"Scaricando {media_type}: {media_url}")
            response = requests.get(media_url, stream=True, timeout=30)
            response.raise_for_status()
            
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            logger.info(f"Media salvato: {filepath}")
            return str(filepath.relative_to(self.output_dir))
            
        except Exception as e:
            logger.error(f"Errore download media {media_url}: {e}")
            return None

    def process_post(self, post):
        """
        Processa un singolo post estraendo tutte le informazioni utili
        
        Args:
            post: Oggetto post da facebook-scraper
            
        Returns:
            dict: Dati del post strutturati
        """
        try:
            post_id = post.get('post_id', '')
            logger.info(f"Processando post ID: {post_id}")
            
            # Estrai dati base del post
            post_data = {
                'post_id': post_id,
                'timestamp': post.get('time', ''),
                'text': post.get('text', ''),
                'user_id': post.get('user_id', ''),
                'username': post.get('username', ''),
                'post_url': post.get('post_url', ''),
                'likes': post.get('likes', 0),
                'comments': post.get('comments', 0),
                'shares': post.get('shares', 0),
                'reactions': post.get('reactions', {}),
                'scraped_at': datetime.datetime.now().isoformat(),
                'media_files': []
            }
            
            # Scarica immagini se presenti
            if post.get('images'):
                for i, image_url in enumerate(post['images']):
                    media_path = self.download_media(image_url, f"{post_id}_img{i}", "image")
                    if media_path:
                        post_data['media_files'].append({
                            'type': 'image',
                            'url': image_url,
                            'local_path': media_path
                        })
                    time.sleep(1)  # Pausa tra download
            
            # Scarica video se presente
            if post.get('video'):
                media_path = self.download_media(post['video'], f"{post_id}_video", "video")
                if media_path:
                    post_data['media_files'].append({
                        'type': 'video',
                        'url': post['video'],
                        'local_path': media_path
                    })
            
            # Informazioni aggiuntive se disponibili
            if post.get('shared_text'):
                post_data['shared_text'] = post['shared_text']
            
            if post.get('link'):
                post_data['external_link'] = post['link']
                
            return post_data
            
        except Exception as e:
            logger.error(f"Errore processando post: {e}")
            return None

    def scrape_posts(self, pages=5, sleep_time=2):
        """
        Scarica i post dalla pagina Facebook
        
        Args:
            pages (int): Numero di pagine da scaricare (circa 2-10 post per pagina)
            sleep_time (int): Secondi di pausa tra le richieste
        """
        try:
            logger.info(f"Inizio scraping pagina {self.page_name}")
            logger.info(f"Pagine da scaricare: {pages}")
            
            # Configurazione facebook-scraper
            posts = get_posts(
                self.page_name,
                pages=pages,
                extra_info=True,
                options={
                    "comments": True,
                    "reactors": True,
                    "allow_extra_requests": True
                }
            )
            
            post_count = 0
            for post in posts:
                try:
                    # Processa il post
                    post_data = self.process_post(post)
                    if post_data:
                        self.posts_data.append(post_data)
                        post_count += 1
                        logger.info(f"Post #{post_count} processato: {post_data['post_id']}")
                    
                    # Pausa tra i post per evitare rate limiting
                    time.sleep(sleep_time)
                    
                except Exception as e:
                    logger.error(f"Errore processando post: {e}")
                    continue
            
            logger.info(f"Scraping completato. Post raccolti: {len(self.posts_data)}")
            
        except Exception as e:
            logger.error(f"Errore durante scraping: {e}")
            raise

    def save_data(self):
        """Salva tutti i dati raccolti in formato JSON"""
        try:
            # Prepara metadati
            metadata = {
                'page_name': self.page_name,
                'scraped_at': datetime.datetime.now().isoformat(),
                'total_posts': len(self.posts_data),
                'script_version': '1.0',
                'posts': self.posts_data
            }
            
            # Salva in JSON con formattazione leggibile
            with open(self.posts_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, ensure_ascii=False, indent=2)
            
            logger.info(f"Dati salvati in: {self.posts_file}")
            logger.info(f"Post totali: {len(self.posts_data)}")
            
            # Crea anche un file di riepilogo
            summary_file = self.output_dir / "summary.txt"
            with open(summary_file, 'w', encoding='utf-8') as f:
                f.write(f"RIEPILOGO SCRAPING FACEBOOK\n")
                f.write(f"==========================\n\n")
                f.write(f"Pagina: {self.page_name}\n")
                f.write(f"Data scraping: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
                f.write(f"Post raccolti: {len(self.posts_data)}\n")
                f.write(f"File JSON: {self.posts_file.name}\n")
                f.write(f"Directory media: {self.media_dir.name}\n\n")
                
                f.write("ELENCO POST:\n")
                f.write("-" * 50 + "\n")
                for i, post in enumerate(self.posts_data, 1):
                    f.write(f"{i:2d}. {post['post_id']} - {post['timestamp']} - Media: {len(post['media_files'])}\n")
                    if post['text']:
                        preview = post['text'][:100].replace('\n', ' ')
                        f.write(f"    {preview}{'...' if len(post['text']) > 100 else ''}\n")
                    f.write("\n")
            
            logger.info(f"Riepilogo salvato in: {summary_file}")
            
        except Exception as e:
            logger.error(f"Errore salvando dati: {e}")
            raise

    def run(self, pages=5):
        """
        Esegue l'intero processo di scraping
        
        Args:
            pages (int): Numero di pagine da scaricare
        """
        try:
            start_time = datetime.datetime.now()
            logger.info("=== INIZIO SCRAPING DONNE FUORI DAL SILENZIO ===")
            
            # Scraping dei post
            self.scrape_posts(pages=pages)
            
            # Salvataggio dati
            if self.posts_data:
                self.save_data()
            else:
                logger.warning("Nessun post raccolto")
            
            # Statistiche finali
            end_time = datetime.datetime.now()
            duration = end_time - start_time
            
            logger.info("=== SCRAPING COMPLETATO ===")
            logger.info(f"Durata: {duration}")
            logger.info(f"Post raccolti: {len(self.posts_data)}")
            logger.info(f"Directory output: {self.output_dir.absolute()}")
            
        except Exception as e:
            logger.error(f"Errore durante l'esecuzione: {e}")
            raise


def main():
    """Funzione principale"""
    try:
        # Crea e avvia lo scraper
        scraper = DonneFuoriScraper()
        
        # Scarica gli ultimi 5 pagine di post (circa 25-50 post)
        scraper.run(pages=5)
        
        print("\n✅ Scraping completato con successo!")
        print(f"📁 Controlla la cartella: {scraper.output_dir.absolute()}")
        print(f"📄 File JSON: {scraper.posts_file}")
        print(f"🖼️  Media scaricati in: {scraper.media_dir}")
        
    except Exception as e:
        print(f"\n❌ Errore durante l'esecuzione: {e}")
        print("📋 Controlla il file facebook_scraper.log per dettagli")


if __name__ == "__main__":
    main()