from base_module import BaseModule
from typing import Dict, Any, List
import asyncio
import logging

logger = logging.getLogger(__name__)


class DomainModule(BaseModule):
    """域名信息收集模块，包括子域名枚举"""
    
    def __init__(self):
        super().__init__("domain")
        self.sources = [
            "https://github.com/wgpsec/ENScan_GO",
            "https://www.xiaolanben.com/pc",
            "https://www.qichacha.com",
            "https://www.tianyancha.com",
            "https://aiqicha.baidu.com"
        ]
        self.subdomain_tools = [
            "https://github.com/shmilylty/OneForAll",
            "https://github.com/OWASP/Amass",
            "https://github.com/projectdiscovery/subfinder"
        ]
    
    async def execute(self, target: str) -> Dict[str, Any]:
        """
        执行域名信息收集
        
        参数:
            target: 要收集信息的目标域名
            
        返回:
            包含域名信息的字典
        """
        logger.info(f"开始对 {target} 进行域名信息收集")
        
        # 清除之前的结果
        self.clear_results()
        
        # 收集根域名信息
        root_domain_info = await self._gather_root_domain_info(target)
        self.store_result("root_domain_info", root_domain_info)
        
        # 收集子域名信息
        subdomains = await self._enumerate_subdomains(target)
        self.store_result("subdomains", subdomains)
        
        self.store_result("target", target)
        
        logger.info(f"完成对 {target} 的域名信息收集")
        return self.get_results()
    
    async def _gather_root_domain_info(self, target: str) -> Dict[str, Any]:
        """
        从各种来源收集根域名信息
        
        参数:
            target: 目标域名
            
        返回:
            包含根域名信息的字典
        """
        # 为查询不同来源创建任务
        tasks = []
        for source in self.sources:
            task = self._query_domain_source(source, target)
            tasks.append(task)
        
        # 并发运行所有任务
        results = await self.run_tasks(tasks)
        
        # 处理并合并结果
        domain_info = {}
        for i, result in enumerate(results):
            if result:
                source = self.sources[i]
                domain_info[source] = result
        
        return domain_info
    
    async def _enumerate_subdomains(self, target: str) -> List[str]:
        """
        使用各种工具枚举子域名
        
        参数:
            target: 目标域名
            
        返回:
            发现的子域名列表
        """
        # 为使用不同工具枚举子域名创建任务
        tasks = []
        for tool in self.subdomain_tools:
            task = self._run_subdomain_tool(tool, target)
            tasks.append(task)
        
        # 并发运行所有任务
        results = await self.run_tasks(tasks)
        
        # 合并并去重子域名
        subdomains = set()
        for result in results:
            if result and isinstance(result, list):
                subdomains.update(result)
        
        return list(subdomains)
    
    async def _query_domain_source(self, source: str, target: str) -> Dict[str, Any]:
        """
        查询特定的域名信息来源
        
        参数:
            source: 域名信息来源URL
            target: 目标域名
            
        返回:
            包含来自此来源的域名信息的字典
        """
        try:
            # 出于演示目的，我们正在模拟响应
            # 在实际实现中，您将向域名信息服务发出实际的HTTP请求并解析其响应
            
            if "ENScan" in source:
                return {
                    "company_name": "示例公司",
                    "registration_number": "123456789",
                    "legal_representative": "张三",
                    "registered_capital": "1000000 元",
                    "establishment_date": "2010-01-01"
                }
            elif "xiaolanben" in source:
                return {
                    "company_name": "示例公司",
                    "industry": "科技",
                    "staff_range": "50-100人",
                    "contact_info": {
                        "phone": "010-12345678",
                        "email": "contact@example.com"
                    }
                }
            elif "qichacha" in source:
                return {
                    "credit_code": "912345678901234567",
                    "taxpayer_identification": "123456789012345",
                    "registration_authority": "北京市市场监督管理局",
                    "business_scope": "软件开发、技术服务"
                }
            elif "tianyancha" in source:
                return {
                    "company_type": "有限责任公司",
                    "operating_status": "在业",
                    "paid_in_capital": "500000 元"
                }
            elif "aiqicha" in source:
                return {
                    "company_name": "示例公司",
                    "unified_social_credit_code": "912345678901234567",
                    "tax_number": "123456789012345",
                    "registration_date": "2010-01-01"
                }
            else:
                return {"raw_response": f"来自 {source} 的响应"}
                
        except Exception as e:
            logger.error(f"查询 {source} 的 {target} 时出错: {str(e)}")
            return {"error": str(e)}
    
    async def _run_subdomain_tool(self, tool: str, target: str) -> List[str]:
        """
        运行子域名枚举工具
        
        参数:
            tool: 子域名枚举工具
            target: 目标域名
            
        返回:
            发现的子域名列表
        """
        try:
            # 出于演示目的，我们正在模拟响应
            # 在实际实现中，您将执行实际的工具并解析其输出
            
            if "OneForAll" in tool:
                return [
                    f"www.{target}",
                    f"mail.{target}",
                    f"admin.{target}",
                    f"blog.{target}"
                ]
            elif "Amass" in tool:
                return [
                    f"api.{target}",
                    f"dev.{target}",
                    f"test.{target}",
                    f"staging.{target}"
                ]
            elif "subfinder" in tool:
                return [
                    f"shop.{target}",
                    f"support.{target}",
                    f"portal.{target}",
                    f"vpn.{target}"
                ]
            else:
                return []
                
        except Exception as e:
            logger.error(f"运行 {tool} 的 {target} 时出错: {str(e)}")
            return []
