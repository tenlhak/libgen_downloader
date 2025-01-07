import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, quote
import logging
from typing import List, Optional

class LibGenSearcher:
    def __init__(self):
        self.logger = self._setup_logging()

    def _setup_logging(self) -> logging.Logger:
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        return logging.getLogger(__name__)

    def fetch(self, url: str) -> str:
        response = requests.get(url)
        response.raise_for_status()
        return response.text

    def process_page(self, url: str) -> List[str]:
        html = self.fetch(url)
        soup = BeautifulSoup(html, 'html.parser')
        links = []
        for tr in soup.find_all('tr', valign="top"):
            a_tag = tr.find('a', title="Libgen & IPFS & Tor")
            if a_tag:
                links.append(urljoin(url, a_tag['href']))
        return links

    def get_download_link(self, url: str) -> Optional[str]:
        html = self.fetch(url)
        soup = BeautifulSoup(html, 'html.parser')
        
        a_tag = soup.find('a', string="GET")
        if a_tag:
            return a_tag['href']
            
        elements = soup.find_all(string=lambda text: "GET" in text)
        for element in elements:
            parent = element.parent
            if parent.name == 'a':
                return parent['href']
            a_tag = parent.find('a')
            if a_tag:
                return a_tag['href']
                
        self.logger.warning(f"Could not find 'GET' link in {url}")
        return None

    def search(self, search_term: str, num_pages: int) -> List[str]:
        encoded_term = quote(search_term)
        base_url = f'https://libgen.is/search.php?&res=100&req={encoded_term}&phrase=1&view=simple&column=def&sort=def&sortmode=ASC&page='
        
        all_links = []
        for i in range(num_pages):
            self.logger.info(f"Processing page {i+1}/{num_pages}...")
            page_links = self.process_page(f'{base_url}{i}')
            all_links.extend(page_links)
            
        self.logger.info(f"Found {len(all_links)} initial links. Getting download links...")
        
        download_links = []
        for i, link in enumerate(all_links):
            self.logger.info(f"Processing link {i+1}/{len(all_links)}...")
            download_link = self.get_download_link(link)
            if download_link:
                download_links.append(download_link)
                
        return list(set(download_links))

def main():
    searcher = LibGenSearcher()
    search_term = input("Enter search term: ")
    num_pages = int(input("Enter number of pages to search (default 25): ") or 25)
    
    download_links = searcher.search(search_term, num_pages)
    
    filename = f'{search_term.replace(" ", "_")}_download_links.txt'
    with open(filename, 'w') as f:
        for link in download_links:
            f.write(f"{link}\n")
            
    print(f'\nDownload links saved to {filename}. Total: {len(download_links)}')

if __name__ == "__main__":
    main()
