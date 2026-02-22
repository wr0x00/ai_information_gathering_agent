import asyncio
import logging
from typing import Dict, Any, List
from config import module_config
from modules.whois_module import WhoisModule
from modules.domain_module import DomainModule
from modules.port_module import PortModule
from modules.sensitive_info_module import SensitiveInfoModule
from modules.github_module import GithubModule

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class InformationGatheringAgent:
    """用于信息收集的主AI代理"""
    
    def __init__(self):
        self.modules = {}
        self.results = {}
        self._initialize_modules()
    
    def _initialize_modules(self):
        """初始化所有启用的模块"""
        enabled_modules = module_config.get_enabled_modules()
        
        if "whois" in enabled_modules:
            self.modules["whois"] = WhoisModule()
        
        if "domain" in enabled_modules:
            self.modules["domain"] = DomainModule()
        
        if "port" in enabled_modules:
            self.modules["port"] = PortModule()
        
        if "sensitive" in enabled_modules:
            self.modules["sensitive"] = SensitiveInfoModule()
        
        if "github" in enabled_modules:
            self.modules["github"] = GithubModule()
        
        logger.info(f"已初始化 {len(self.modules)} 个模块: {list(self.modules.keys())}")
    
    async def run_scan(self, target: str) -> Dict[str, Any]:
        """
        对目标运行完整的信息收集扫描
        
        参数:
            target: 要扫描的目标域名/IP
            
        返回:
            包含所有扫描结果的字典
        """
        logger.info(f"开始对 {target} 进行信息收集扫描")
        
        # 清除之前的结果
        self.results.clear()
        
        # 为所有启用的模块创建任务
        tasks = []
        for module_name, module in self.modules.items():
            task = self._run_module(module_name, module, target)
            tasks.append(task)
        
        # 并发运行所有任务
        await asyncio.gather(*tasks)
        
        logger.info(f"完成对 {target} 的信息收集扫描")
        return self.results
    
    async def _run_module(self, module_name: str, module, target: str):
        """
        运行特定模块并存储其结果
        
        参数:
            module_name: 模块名称
            module: 模块实例
            target: 要扫描的目标
        """
        try:
            logger.info(f"正在运行 {target} 的 {module_name} 模块")
            result = await module.execute(target)
            self.results[module_name] = result
            logger.info(f"完成 {target} 的 {module_name} 模块")
        except Exception as e:
            logger.error(f"运行 {target} 的 {module_name} 模块时出错: {str(e)}")
            self.results[module_name] = {"error": str(e)}
    
    async def run_specific_modules(self, target: str, module_names: List[str]) -> Dict[str, Any]:
        """
        仅运行特定模块
        
        参数:
            target: 要扫描的目标域名/IP
            module_names: 要运行的模块名称列表
            
        返回:
            包含指定模块结果的字典
        """
        logger.info(f"开始使用特定模块 {module_names} 对 {target} 进行扫描")
        
        # 清除之前的结果
        self.results.clear()
        
        # 筛选出仅启用和请求的模块
        modules_to_run = {
            name: module for name, module in self.modules.items()
            if name in module_names
        }
        
        # 为选定的模块创建任务
        tasks = []
        for module_name, module in modules_to_run.items():
            task = self._run_module(module_name, module, target)
            tasks.append(task)
        
        # 并发运行所有任务
        await asyncio.gather(*tasks)
        
        logger.info(f"完成使用特定模块对 {target} 的扫描")
        return self.results
    
    def get_results(self) -> Dict[str, Any]:
        """
        获取所有存储的结果
        
        返回:
            包含所有结果的字典
        """
        return self.results
    
    def clear_results(self):
        """清除所有存储的结果"""
        self.results.clear()


async def main():
    """用于测试代理的主函数"""
    # 创建代理实例
    agent = InformationGatheringAgent()
    
    # 对example.com运行扫描
    target = "example.com"
    results = await agent.run_scan(target)
    
    # 打印结果摘要
    print(f"\n=== {target} 的扫描结果 ===")
    for module_name, result in results.items():
        if "error" in result:
            print(f"{module_name}: 错误 - {result['error']}")
        else:
            print(f"{module_name}: 成功完成")
    
    print("\n=== 详细结果 ===")
    for module_name, result in results.items():
        print(f"\n{module_name.upper()} 模块:")
        print(f"  目标: {result.get('target', 'N/A')}")
        if "error" in result:
            print(f"  错误: {result['error']}")
        else:
            # 打印每个模块的一些关键信息
            if module_name == "whois":
                whois_data = result.get("whois_data", {})
                print(f"  查询的来源: {len(whois_data)}")
            elif module_name == "domain":
                subdomains = result.get("subdomains", [])
                print(f"  发现的子域名: {len(subdomains)}")
            elif module_name == "port":
                open_ports = result.get("open_ports", [])
                print(f"  发现的开放端口: {len(open_ports)}")
            elif module_name == "sensitive":
                dorks = result.get("google_dorks", [])
                files = result.get("sensitive_files", [])
                print(f"  执行的Google dorks: {len(dorks)}")
                print(f"  发现的敏感文件: {len(files)}")
            elif module_name == "github":
                sensitive = result.get("sensitive_info", [])
                print(f"  发现的敏感信息: {len(sensitive)}")


if __name__ == "__main__":
    asyncio.run(main())
