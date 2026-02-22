import httpx
import asyncio
import random
from typing import Optional, Dict, Any, List
from config import settings
import logging

logger = logging.getLogger(__name__)


class AsyncHTTPClient:
    def __init__(self):
        self.timeout = settings.timeout
        self.user_agents = settings.user_agents
        self.semaphore = asyncio.Semaphore(settings.max_concurrent_requests)
    
    async def get_random_user_agent(self) -> str:
        return random.choice(self.user_agents)
    
    async def get(self, url: str, headers: Optional[Dict[str, str]] = None, 
                  params: Optional[Dict[str, Any]] = None) -> httpx.Response:
        async with self.semaphore:
            user_agent = await self.get_random_user_agent()
            default_headers = {"User-Agent": user_agent}
            
            if headers:
                default_headers.update(headers)
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                try:
                    response = await client.get(url, headers=default_headers, params=params)
                    logger.debug(f"GET {url} - 状态: {response.status_code}")
                    return response
                except Exception as e:
                    logger.error(f"获取 {url} 时出错: {str(e)}")
                    raise
    
    async def post(self, url: str, headers: Optional[Dict[str, str]] = None,
                   data: Optional[Dict[str, Any]] = None, json: Optional[Dict[str, Any]] = None) -> httpx.Response:
        async with self.semaphore:
            user_agent = await self.get_random_user_agent()
            default_headers = {"User-Agent": user_agent}
            
            if headers:
                default_headers.update(headers)
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                try:
                    response = await client.post(url, headers=default_headers, data=data, json=json)
                    logger.debug(f"POST {url} - 状态: {response.status_code}")
                    return response
                except Exception as e:
                    logger.error(f"向 {url} 发送POST请求时出错: {str(e)}")
                    raise
    
    async def fetch_multiple(self, urls: List[str], method: str = "GET", 
                           headers: Optional[Dict[str, str]] = None) -> List[Dict[str, Any]]:
        """
        并发获取多个URL
        
        参数:
            urls: 要获取的URL列表
            method: HTTP方法 ("GET" 或 "POST")
            headers: 可选的请求头
            
        返回:
            包含URL、状态码、请求头和内容的字典列表
        """
        tasks = []
        for url in urls:
            if method.upper() == "GET":
                task = self.get(url, headers)
            elif method.upper() == "POST":
                task = self.post(url, headers)
            else:
                raise ValueError(f"不支持的方法: {method}")
            
            tasks.append(task)
        
        responses = []
        for i, coroutine in enumerate(asyncio.as_completed(tasks)):
            try:
                response = await coroutine
                responses.append({
                    "url": str(response.url),
                    "status_code": response.status_code,
                    "headers": dict(response.headers),
                    "content": response.text
                })
            except Exception as e:
                url = urls[i] if i < len(urls) else "未知URL"
                responses.append({
                    "url": url,
                    "error": str(e)
                })
        
        return responses
