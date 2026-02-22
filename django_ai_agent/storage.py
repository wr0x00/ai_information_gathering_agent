import json
import aiofiles
import os
from typing import Dict, Any
from config import settings
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class ResultsStorage:
    """处理扫描结果的存储"""
    
    def __init__(self):
        self.output_dir = settings.output_dir
        self._ensure_output_directory()
    
    def _ensure_output_directory(self):
        """确保存储目录存在"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            logger.info(f"已创建存储目录: {self.output_dir}")
    
    async def save_results(self, target: str, results: Dict[str, Any]) -> str:
        """
        将扫描结果保存到JSON文件
        
        参数:
            target: 被扫描的目标域名/IP
            results: 扫描结果字典
            
        返回:
            保存文件的路径
        """
        try:
            # 使用时间戳创建文件名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{target.replace('.', '_')}_{timestamp}.json"
            filepath = os.path.join(self.output_dir, filename)
            
            # 添加元数据
            output_data = {
                "target": target,
                "scan_timestamp": datetime.now().isoformat(),
                "results": results
            }
            
            # 异步写入文件
            async with aiofiles.open(filepath, 'w', encoding='utf-8') as f:
                await f.write(json.dumps(output_data, indent=2, ensure_ascii=False))
            
            logger.info(f"结果已保存到 {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"保存 {target} 的结果时出错: {str(e)}")
            raise
    
    async def save_results_as_text(self, target: str, results: Dict[str, Any]) -> str:
        """
        将扫描结果保存为人类可读的文本文件
        
        参数:
            target: 被扫描的目标域名/IP
            results: 扫描结果字典
            
        返回:
            保存文件的路径
        """
        try:
            # 使用时间戳创建文件名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{target.replace('.', '_')}_{timestamp}.txt"
            filepath = os.path.join(self.output_dir, filename)
            
            # 将结果格式化为文本
            text_content = self._format_results_as_text(target, results)
            
            # 异步写入文件
            async with aiofiles.open(filepath, 'w', encoding='utf-8') as f:
                await f.write(text_content)
            
            logger.info(f"文本结果已保存到 {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"保存 {target} 的文本结果时出错: {str(e)}")
            raise
    
    def _format_results_as_text(self, target: str, results: Dict[str, Any]) -> str:
        """
        将扫描结果格式化为人类可读的文本
        
        参数:
            target: 被扫描的目标域名/IP
            results: 扫描结果字典
            
        返回:
            格式化的文本字符串
        """
        lines = []
        lines.append("=" * 60)
        lines.append(f"信息收集报告")
        lines.append("=" * 60)
        lines.append(f"目标: {target}")
        lines.append(f"扫描时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")
        
        for module_name, module_results in results.items():
            lines.append("-" * 40)
            lines.append(f"{module_name.upper()} 模块结果")
            lines.append("-" * 40)
            
            if "error" in module_results:
                lines.append(f"错误: {module_results['error']}")
            else:
                # 根据模块类型格式化
                if module_name == "whois":
                    whois_data = module_results.get("whois_data", {})
                    lines.append(f"查询的来源: {len(whois_data)}")
                    for source, data in whois_data.items():
                        lines.append(f"  来源: {source}")
                        for key, value in data.items():
                            lines.append(f"    {key}: {value}")
                
                elif module_name == "domain":
                    subdomains = module_results.get("subdomains", [])
                    root_info = module_results.get("root_domain_info", {})
                    
                    lines.append(f"发现的子域名: {len(subdomains)}")
                    for subdomain in subdomains[:10]:  # 限制前10个
                        lines.append(f"  - {subdomain}")
                    if len(subdomains) > 10:
                        lines.append(f"  ... 还有 {len(subdomains) - 10} 个")
                    
                    lines.append(f"域名信息来源: {len(root_info)}")
                    for source, data in root_info.items():
                        lines.append(f"  来源: {source}")
                        for key, value in data.items():
                            lines.append(f"    {key}: {value}")
                
                elif module_name == "port":
                    open_ports = module_results.get("open_ports", [])
                    c_segment = module_results.get("c_segment", {})
                    
                    lines.append(f"发现的开放端口: {len(open_ports)}")
                    for port_info in open_ports:
                        port = port_info.get("port", "N/A")
                        service = port_info.get("service", "未知")
                        banner = port_info.get("banner", "N/A")
                        lines.append(f"  端口 {port}: {service} ({banner})")
                    
                    alive_hosts = c_segment.get("alive_hosts", [])
                    lines.append(f"C段活跃主机: {len(alive_hosts)}")
                    for host in alive_hosts:
                        lines.append(f"  - {host}")
                
                elif module_name == "sensitive":
                    dorks = module_results.get("google_dorks", [])
                    files = module_results.get("sensitive_files", [])
                    credentials = module_results.get("exposed_credentials", [])
                    
                    lines.append(f"执行的Google dorks: {len(dorks)}")
                    lines.append(f"发现的敏感文件: {len(files)}")
                    lines.append(f"发现的暴露凭证: {len(credentials)}")
                    
                    if files:
                        lines.append("  敏感文件:")
                        for file_info in files:
                            if file_info:
                                url = file_info.get("url", "N/A")
                                risk = file_info.get("risk", "未知")
                                lines.append(f"    {url} (风险: {risk})")
                    
                    if credentials:
                        lines.append("  暴露的凭证:")
                        for cred in credentials:
                            source = cred.get("source", "N/A")
                            ctype = cred.get("type", "未知")
                            lines.append(f"    {source}: {ctype}")
                
                elif module_name == "github":
                    sensitive = module_results.get("sensitive_info", [])
                    code_snippets = module_results.get("code_snippets", [])
                    config_files = module_results.get("config_files", [])
                    
                    lines.append(f"发现的敏感信息: {len(sensitive)}")
                    lines.append(f"发现的代码片段: {len(code_snippets)}")
                    lines.append(f"发现的配置文件: {len(config_files)}")
                    
                    if sensitive:
                        lines.append("  敏感信息:")
                        for item in sensitive[:5]:  # 限制前5个
                            url = item.get("url", "N/A")
                            snippet = item.get("snippet", "N/A")
                            lines.append(f"    {url}")
                            lines.append(f"      {snippet}")
                
                else:
                    # 其他模块的通用格式化
                    lines.append(json.dumps(module_results, indent=2, ensure_ascii=False))
            
            lines.append("")  # 模块之间的空行
        
        return "\n".join(lines)
    
    async def load_results(self, filepath: str) -> Dict[str, Any]:
        """
        从JSON文件加载扫描结果
        
        参数:
            filepath: JSON文件的路径
            
        返回:
            包含扫描结果的字典
        """
        try:
            async with aiofiles.open(filepath, 'r', encoding='utf-8') as f:
                content = await f.read()
                return json.loads(content)
                
        except Exception as e:
            logger.error(f"从 {filepath} 加载结果时出错: {str(e)}")
            raise
    
    def list_saved_results(self) -> list:
        """
        列出所有保存的结果文件
        
        返回:
            保存的结果文件列表
        """
        try:
            files = []
            if os.path.exists(self.output_dir):
                for filename in os.listdir(self.output_dir):
                    if filename.endswith('.json') or filename.endswith('.txt'):
                        filepath = os.path.join(self.output_dir, filename)
                        files.append({
                            "filename": filename,
                            "filepath": filepath,
                            "modified": datetime.fromtimestamp(os.path.getmtime(filepath)).isoformat()
                        })
            return files
            
        except Exception as e:
            logger.error(f"列出保存的结果时出错: {str(e)}")
            return []
