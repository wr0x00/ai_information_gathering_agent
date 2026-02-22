from abc import ABC, abstractmethod
from typing import Dict, Any, List
from http_client import AsyncHTTPClient
import logging
import asyncio

logger = logging.getLogger(__name__)


class BaseModule(ABC):
    """所有信息收集模块的基类"""
    
    def __init__(self, name: str):
        self.name = name
        self.http_client = AsyncHTTPClient()
        self.results = {}
    
    @abstractmethod
    async def execute(self, target: str) -> Dict[str, Any]:
        """
        执行模块的主要功能
        
        参数:
            target: 要扫描的目标域名/IP
            
        返回:
            包含结果的字典
        """
        pass
    
    async def run_tasks(self, tasks: List[asyncio.Task]) -> List[Any]:
        """
        并发运行多个异步任务
        
        参数:
            tasks: 要运行的异步任务列表
            
        返回:
            来自任务的结果列表
        """
        results = []
        for task in asyncio.as_completed(tasks):
            try:
                result = await task
                results.append(result)
            except Exception as e:
                logger.error(f"任务中出现错误: {str(e)}")
                results.append(None)
        return results
    
    def store_result(self, key: str, value: Any):
        """
        在模块的结果字典中存储结果
        
        参数:
            key: 存储结果的键
            value: 要存储的结果值
        """
        self.results[key] = value
    
    def get_results(self) -> Dict[str, Any]:
        """
        获取所有存储的结果
        
        返回:
            所有存储结果的字典
        """
        return self.results
    
    def clear_results(self):
        """清除所有存储的结果"""
        self.results.clear()
