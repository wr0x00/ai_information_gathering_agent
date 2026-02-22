from base_module import BaseModule
from typing import Dict, Any
import asyncio
import logging

logger = logging.getLogger(__name__)


class WhoisModule(BaseModule):
    """WHOIS信息收集模块"""
    
    def __init__(self):
        super().__init__("whois")
        self.sources = [
            "https://whois.chinaz.com",
            "https://bgp.he.net"
        ]
    
    async def execute(self, target: str) -> Dict[str, Any]:
        """
        执行WHOIS信息收集
        
        参数:
            target: 要查询WHOIS信息的目标域名
            
        返回:
            包含WHOIS信息的字典
        """
        logger.info(f"开始对 {target} 进行WHOIS查询")
        
        # 清除之前的结果
        self.clear_results()
        
        # 为查询不同来源创建任务
        tasks = []
        for source in self.sources:
            task = self._query_source(source, target)
            tasks.append(task)
        
        # 并发运行所有任务
        results = await self.run_tasks(tasks)
        
        # 处理并存储结果
        whois_data = {}
        for i, result in enumerate(results):
            if result:
                source = self.sources[i]
                whois_data[source] = result
        
        self.store_result("whois_data", whois_data)
        self.store_result("target", target)
        
        logger.info(f"完成对 {target} 的WHOIS查询")
        return self.get_results()
    
    async def _query_source(self, source: str, target: str) -> Dict[str, Any]:
        """
        查询特定的WHOIS来源
        
        参数:
            source: WHOIS来源URL
            target: 目标域名
            
        返回:
            包含来自此来源的WHOIS数据的字典
        """
        try:
            # 出于演示目的，我们正在模拟响应
            # 在实际实现中，您将向WHOIS服务发出实际的HTTP请求并解析其响应
            
            if "chinaz" in source:
                # 模拟chinaz WHOIS响应
                return {
                    "registrar": "注册商名称",
                    "creation_date": "2020-01-01",
                    "expiration_date": "2025-01-01",
                    "nameservers": ["ns1.example.com", "ns2.example.com"],
                    "registrant": "注册人姓名"
                }
            elif "bgp" in source:
                # 模拟bgp.he.net WHOIS响应
                return {
                    "asn": "AS12345",
                    "org": "组织名称",
                    "ip_range": "192.168.0.0/24",
                    "country": "CN"
                }
            else:
                return {"raw_response": f"来自 {source} 的响应"}
                
        except Exception as e:
            logger.error(f"查询 {source} 的 {target} 时出错: {str(e)}")
            return {"error": str(e)}
