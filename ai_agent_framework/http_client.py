"""
Async HTTP Client for AI Agent Framework
"""
import httpx
import asyncio
import logging
from typing import Dict, Any, Optional, List
from urllib.parse import urljoin

logger = logging.getLogger(__name__)


class AsyncHTTPClient:
    """Async HTTP client using httpx for making requests"""
    
    def __init__(self, 
                 timeout: int = 30,
                 max_concurrent: int = 10,
                 user_agents: Optional[List[str]] = None):
        self.timeout = timeout
        self.max_concurrent = max_concurrent
        
        # Default user agents
        self.user_agents = user_agents or [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        ]
        
        # Semaphore for limiting concurrent requests
        self.semaphore = asyncio.Semaphore(max_concurrent)
        
        # HTTP client
        self.client = httpx.AsyncClient(
            timeout=httpx.Timeout(timeout),
            follow_redirects=True
        )
    
    async def get(self, url: str, headers: Optional[Dict[str, str]] = None) -> httpx.Response:
        """Perform async GET request"""
        async with self.semaphore:
            headers = headers or {}
            headers.setdefault("User-Agent", self._get_random_user_agent())
            
            try:
                logger.debug(f"Making GET request to {url}")
                response = await self.client.get(url, headers=headers)
                logger.debug(f"GET request to {url} completed with status {response.status_code}")
                return response
            except Exception as e:
                logger.error(f"GET request to {url} failed: {str(e)}")
                raise
    
    async def post(self, url: str, data: Optional[Dict[str, Any]] = None, 
                   json: Optional[Dict[str, Any]] = None, 
                   headers: Optional[Dict[str, str]] = None) -> httpx.Response:
        """Perform async POST request"""
        async with self.semaphore:
            headers = headers or {}
            headers.setdefault("User-Agent", self._get_random_user_agent())
            
            try:
                logger.debug(f"Making POST request to {url}")
                response = await self.client.post(url, data=data, json=json, headers=headers)
                logger.debug(f"POST request to {url} completed with status {response.status_code}")
                return response
            except Exception as e:
                logger.error(f"POST request to {url} failed: {str(e)}")
                raise
    
    async def request(self, method: str, url: str, **kwargs) -> httpx.Response:
        """Generic async request method"""
        async with self.semaphore:
            kwargs.setdefault("headers", {})
            kwargs["headers"].setdefault("User-Agent", self._get_random_user_agent())
            
            try:
                logger.debug(f"Making {method} request to {url}")
                response = await self.client.request(method, url, **kwargs)
                logger.debug(f"{method} request to {url} completed with status {response.status_code}")
                return response
            except Exception as e:
                logger.error(f"{method} request to {url} failed: {str(e)}")
                raise
    
    def _get_random_user_agent(self) -> str:
        """Get a random user agent from the list"""
        import random
        return random.choice(self.user_agents)
    
    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()


# Convenience functions
async def fetch_url(url: str, timeout: int = 30) -> httpx.Response:
    """Convenience function to fetch a single URL"""
    async with AsyncHTTPClient(timeout=timeout) as client:
        return await client.get(url)


async def fetch_multiple_urls(urls: List[str], timeout: int = 30, 
                             max_concurrent: int = 10) -> List[httpx.Response]:
    """Convenience function to fetch multiple URLs concurrently"""
    async with AsyncHTTPClient(timeout=timeout, max_concurrent=max_concurrent) as client:
        tasks = [client.get(url) for url in urls]
        return await asyncio.gather(*tasks, return_exceptions=True)
