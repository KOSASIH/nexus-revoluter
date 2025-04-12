import logging
import os
import json
import requests
import asyncio
import aiohttp
from hashlib import sha256

class IPFSStorage:
    def __init__(self, ipfs_url="http://localhost:5001"):
        self.logger = logging.getLogger("IPFSStorage")
        self.ipfs_url = ipfs_url
        self.local_cache = {}  # Cache for frequently accessed files

    async def upload_file(self, file_path):
        """Upload a file to IPFS and return its hash."""
        if not os.path.isfile(file_path):
            self.logger.error(f"File not found: {file_path}")
            return None

        async with aiohttp.ClientSession() as session:
            with open(file_path, 'rb') as file:
                data = file.read()
                file_hash = sha256(data).hexdigest()  # Calculate hash for integrity
                self.logger.info(f"Uploading {file_path} to IPFS...")

                async with session.post(f"{self.ipfs_url}/api/v0/add", data=data) as response:
                    if response.status == 200:
                        result = await response.json()
                        ipfs_hash = result['Hash']
                        self.local_cache[ipfs_hash] = file_path  # Cache the file path
                        self.logger.info(f"Uploaded {file_path} to IPFS with hash: {ipfs_hash}")
                        return ipfs_hash
                    else:
                        self.logger.error(f"Failed to upload {file_path}: {response.status} {await response.text()}")
                        return None

    async def retrieve_file(self, ipfs_hash, save_path):
        """Retrieve a file from IPFS using its hash."""
        if ipfs_hash in self.local_cache:
            self.logger.info(f"Retrieving {ipfs_hash} from local cache.")
            local_file_path = self.local_cache[ipfs_hash]
            os.rename(local_file_path, save_path)  # Move cached file to save path
            return save_path

        self.logger.info(f"Retrieving {ipfs_hash} from IPFS...")
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.ipfs_url}/api/v0/cat?arg={ipfs_hash}") as response:
                if response.status == 200:
                    with open(save_path, 'wb') as file:
                        file.write(await response.read())
                    self.local_cache[ipfs_hash] = save_path  # Cache the file path
                    self.logger.info(f"Retrieved {ipfs_hash} and saved to {save_path}")
                    return save_path
                else:
                    self.logger.error(f"Failed to retrieve {ipfs_hash}: {response.status} {await response.text()}")
                    return None

    async def upload_files(self, file_paths):
        """Upload multiple files to IPFS."""
        tasks = [self.upload_file(file_path) for file_path in file_paths]
        return await asyncio.gather(*tasks)

    async def retrieve_files(self, ipfs_hashes, save_dir):
        """Retrieve multiple files from IPFS."""
        tasks = [self.retrieve_file(ipfs_hash, os.path.join(save_dir, ipfs_hash)) for ipfs_hash in ipfs_hashes]
        return await asyncio.gather(*tasks)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    ipfs_storage = IPFSStorage()

    # Example usage
    async def main():
        # Upload a single file
        file_hash = await ipfs_storage.upload_file("example.txt")
        print(f"Uploaded file hash: {file_hash}")

        # Retrieve the file
        if file_hash:
            await ipfs_storage.retrieve_file(file_hash, "retrieved_example.txt")

        # Upload multiple files
        file_hashes = await ipfs_storage.upload_files(["example1.txt", "example2.txt"])
        print(f"Uploaded file hashes: {file_hashes}")

        # Retrieve multiple files
        await ipfs_storage.retrieve _files(file_hashes, "retrieved_files")

    asyncio.run(main())
