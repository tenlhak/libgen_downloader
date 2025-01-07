import requests
import os
from urllib.parse import unquote
import time
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
from pathlib import Path
import logging
from typing import Tuple

class PDFDownloader:
    def __init__(self, output_dir: str, max_workers: int = 3, delay: float = 1.0):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.max_workers = max_workers
        self.delay = delay
        self.logger = self._setup_logging()
        
    def _setup_logging(self) -> logging.Logger:
        logging.basicConfig(
            filename='download_log.txt',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        return logging.getLogger(__name__)

    def download_pdf(self, url: str) -> bool:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        try:
            response = requests.get(url, headers=headers, stream=True)
            response.raise_for_status()
            
            filename = unquote(url.split('/')[-1])
            save_path = self.output_dir / filename
            
            with save_path.open('wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        
            self.logger.info(f"Successfully downloaded: {filename}")
            time.sleep(self.delay)
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to download {url}: {str(e)}")
            return False

    def download_all(self, links: list) -> Tuple[int, int]:
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            results = list(tqdm(
                executor.map(self.download_pdf, links),
                total=len(links),
                desc="Downloading PDFs"
            ))
            
        successful = sum(results)
        failed = len(results) - successful
        return successful, failed

def main():
    input_file = input("Enter input file name (default: download_links.txt): ") or "download_links.txt"
    output_dir = input("Enter output directory (default: downloaded_books): ") or "downloaded_books"
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            links = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"{input_file} not found!")
        return
        
    downloader = PDFDownloader(output_dir)
    successful, failed = downloader.download_all(links)
    
    print("\nDownload Summary:")
    print(f"Total links processed: {len(links)}")
    print(f"Successfully downloaded: {successful}")
    print(f"Failed downloads: {failed}")

if __name__ == "__main__":
    main()
