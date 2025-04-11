import requests
from urllib.parse import urlparse
from ipfshttpclient import connect
import logging
import asyncio
import aiohttp
import json

class URLValidator:
    def __init__(self, ipfs_node="/ip4/127.0.0.1/tcp/5001", timeout=5):
        self.logger = logging.getLogger("URLValidator")
        self.ipfs = connect(ipfs_node)
        self.fallback_urls = {}
        self.cache = {}
        self.timeout = timeout

    async def check_url_async(self, url):
        """Asynchronously check if a URL is valid and accessible."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.head(url, timeout=self.timeout) as response:
                    return response.status == 200
        except Exception as e:
            self.logger.error(f"URL {url} failed: {e}")
            return False

    async def repair_url_async(self, url):
        """Repair a broken URL by searching for a backup in IPFS."""
        if await self.check_url_async(url):
            return url
        
        # Try to find in IPFS based on domain or path
        parsed = urlparse(url)
        ipfs_key = f"{parsed.netloc}{parsed.path}"
        try:
            ipfs_data = self.ipfs.get(ipfs_key)
            self.logger.info(f"URL {url} restored from IPFS: {ipfs_data}")
            return ipfs_data["url"]
        except Exception as e:
            self.logger.error(f"Cannot restore URL {url}: {e}")
            return self.fallback_urls.get(url, None)

    async def store_url_backup_async(self, url, content):
        """Store a backup URL in IPFS with metadata."""
        try:
            metadata = {
                "url": url,
                "content": content,
                "timestamp": self.get_current_timestamp()
            }
            ipfs_hash = self.ipfs.add_str(json.dumps(metadata))
            self.logger.info(f"URL {url} backed up to IPFS: {ipfs_hash}")
            return ipfs_hash
        except Exception as e:
            self.logger.error(f"Failed to back up URL {url}: {e}")
            return None

    def get_current_timestamp(self):
        """Get the current timestamp."""
        from datetime import datetime
        return datetime.now().isoformat()

    async def process_urls(self, urls):
        """Process a list of URLs for validation and repair."""
        tasks = []
        for url in urls:
            tasks.append(self.check_and_repair_url(url))
        return await asyncio.gather(*tasks)

    async def check_and_repair_url(self, url):
        """Check and repair a single URL."""
        if url in self.cache:
            self.logger.info(f"Cache hit for URL: {url}")
            return self.cache[url]
        
        is_valid = await self.check_url_async(url)
        if not is_valid:
            repaired = await self.repair_url_async(url)
            self.cache[url] = repaired
            return repaired
        else:
            self.cache[url] = url
            return url

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    validator = URLValidator()
    test_urls = ["https://example.com", "https://invalid-url.com"]

    async def main():
        results = await validator.process_urls(test_urls)
        for url, result in zip(test_urls, results):
            print(f"Processed URL: {url}, Result: {result}")

    asyncio.run(main())
