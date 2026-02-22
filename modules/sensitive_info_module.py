from base_module import BaseModule
from typing import Dict, Any, List
import asyncio
import logging
from urllib.parse import quote_plus

logger = logging.getLogger(__name__)


class SensitiveInfoModule(BaseModule):
    """使用Google Dorks和其他技术发现敏感信息的模块"""
    
    def __init__(self):
        super().__init__("sensitive_info")
        self.google_dorks = [
            "site:{} intitle:管理|后台|登陆|管理员|系统|内部",
            "site:{} inurl:login|admin|system|guanli|denglu|manage|admin_login|auth|dev",
            "site:{} filetype:doc OR filetype:ppt OR filetype:pps OR filetype:xls OR filetype:docx OR filetype:pptx OR filetype:ppsx OR filetype:xlsx OR filetype:odt OR filetype:ods OR filetype:odg OR filetype:odp OR filetype:pdf OR filetype:wpd OR filetype:svg OR filetype:svgz OR filetype:indd OR filetype:rdp OR filetype:sql OR filetype:xml OR filetype:db OR filetype:mdb OR filetype:sqlite OR filetype:log OR filetype:conf",
            "site:{} inurl:test|ceshi",
            "site:{} intitle:测试",
            "site:{} intitle:\"Outlook Web App\" OR intitle:\"邮件\" OR inurl:\"email\" OR inurl:\"webmail\"",
            "site:{} inurl:api|uid=|id=|userid=|token|session",
            "site:{} intitle:index.of \"server at\""
        ]
    
    async def execute(self, target: str) -> Dict[str, Any]:
        """
        执行敏感信息发现
        
        参数:
            target: 要搜索敏感信息的目标域名
            
        返回:
            包含敏感信息发现结果的字典
        """
        logger.info(f"开始对 {target} 进行敏感信息发现")
        
        # 清除之前的结果
        self.clear_results()
        
        # 使用Google Dorks搜索
        google_dork_results = await self._search_google_dorks(target)
        self.store_result("google_dorks", google_dork_results)
        
        # 搜索敏感文件
        sensitive_files = await self._search_sensitive_files(target)
        self.store_result("sensitive_files", sensitive_files)
        
        # 搜索暴露的凭证
        exposed_credentials = await self._search_exposed_credentials(target)
        self.store_result("exposed_credentials", exposed_credentials)
        
        self.store_result("target", target)
        
        logger.info(f"完成对 {target} 的敏感信息发现")
        return self.get_results()
    
    async def _search_google_dorks(self, target: str) -> List[Dict[str, Any]]:
        """
        使用Google Dorks搜索敏感信息
        
        参数:
            target: 目标域名
            
        返回:
            搜索结果列表
        """
        results = []
        
        # 为使用不同dorks搜索创建任务
        tasks = []
        for dork in self.google_dorks:
            task = self._execute_google_dork(dork, target)
            tasks.append(task)
        
        # 并发运行所有任务
        dork_results = await self.run_tasks(tasks)
        
        # 处理结果
        for i, result in enumerate(dork_results):
            if result:
                dork = self.google_dorks[i]
                results.append({
                    "dork": dork,
                    "results": result
                })
        
        return results
    
    async def _execute_google_dork(self, dork: str, target: str) -> List[str]:
        """
        执行特定的Google Dork搜索
        
        参数:
            dork: Google Dork查询
            target: 目标域名
            
        返回:
            找到的URL列表
        """
        try:
            # 出于演示目的，我们正在模拟响应
            # 在实际实现中，您将与搜索引擎交互
            # 或使用专门的工具来执行这些查询
            
            # 用目标格式化dork
            formatted_dork = dork.format(target)
            
            # 模拟搜索结果
            if "后台" in formatted_dork or "admin" in formatted_dork:
                return [
                    f"https://{target}/admin/login.php",
                    f"https://{target}/management/dashboard",
                    f"https://{target}/system/auth"
                ]
            elif "filetype" in formatted_dork:
                return [
                    f"https://{target}/documents/confidential.doc",
                    f"https://{target}/backup/database.sql",
                    f"https://{target}/config/app.conf"
                ]
            elif "test" in formatted_dork or "测试" in formatted_dork:
                return [
                    f"https://{target}/test/environment",
                    f"https://{target}/dev/api/debug"
                ]
            elif "邮件" in formatted_dork or "email" in formatted_dork:
                return [
                    f"https://{target}/owa/",
                    f"https://{target}/webmail/"
                ]
            elif "token" in formatted_dork or "session" in formatted_dork:
                return [
                    f"https://{target}/api/user?token=xyz123",
                    f"https://{target}/auth/session?id=abc456"
                ]
            elif "index.of" in formatted_dork:
                return [
                    f"https://{target}/files/",
                    f"https://{target}/downloads/"
                ]
            else:
                return [f"https://{target}/search/results?q={quote_plus(formatted_dork)}"]
                
        except Exception as e:
            logger.error(f"执行Google Dork '{dork}' 的 {target} 时出错: {str(e)}")
            return []
    
    async def _search_sensitive_files(self, target: str) -> List[Dict[str, Any]]:
        """
        在目标上搜索敏感文件
        
        参数:
            target: 目标域名
            
        返回:
            找到的敏感文件列表
        """
        try:
            # 出于演示目的，我们正在模拟响应
            # 在实际实现中，您将执行实际的文件发现
            
            # 要检查的常见敏感文件路径
            sensitive_paths = [
                "/.env",
                "/config/database.yml",
                "/appsettings.json",
                "/web.config",
                "/robots.txt",
                "/sitemap.xml",
                "/.git/config",
                "/.svn/entries",
                "/backup.tar.gz",
                "/database.sql"
            ]
            
            # 为检查每个路径创建任务
            tasks = []
            for path in sensitive_paths:
                url = f"https://{target}{path}"
                task = self._check_file_exists(url)
                tasks.append(task)
            
            # 并发运行所有任务
            results = await self.run_tasks(tasks)
            
            # 过滤掉None结果（未找到的文件）
            found_files = [result for result in results if result]
            
            return found_files
            
        except Exception as e:
            logger.error(f"搜索 {target} 的敏感文件时出错: {str(e)}")
            return []
    
    async def _check_file_exists(self, url: str) -> Dict[str, Any]:
        """
        检查给定URL处是否存在文件
        
        参数:
            url: 要检查的URL
            
        返回:
            如果找到则返回包含文件信息的字典，否则返回None
        """
        try:
            # 出于演示目的，我们正在模拟响应
            # 在实际实现中，您将发出HTTP请求来检查
            # 文件是否存在并分析其内容
            
            # 模拟文件存在性检查
            sensitive_files = {
                f"https://{url.split('/')[2]}/.env": {
                    "url": url,
                    "size": "1.2 KB",
                    "type": "环境配置",
                    "risk": "高"
                },
                f"https://{url.split('/')[2]}/config/database.yml": {
                    "url": url,
                    "size": "2.5 KB",
                    "type": "数据库配置",
                    "risk": "高"
                },
                f"https://{url.split('/')[2]}/backup.tar.gz": {
                    "url": url,
                    "size": "125 MB",
                    "type": "备份存档",
                    "risk": "严重"
                }
            }
            
            return sensitive_files.get(url)
            
        except Exception as e:
            logger.error(f"检查文件 {url} 时出错: {str(e)}")
            return None
    
    async def _search_exposed_credentials(self, target: str) -> List[Dict[str, Any]]:
        """
        搜索暴露的凭证
        
        参数:
            target: 目标域名
            
        返回:
            找到的暴露凭证列表
        """
        try:
            # 出于演示目的，我们正在模拟响应
            # 在实际实现中，您将在GitHub、代码仓库中搜索
            # 和其他来源寻找暴露的凭证
            
            # 模拟凭证发现
            return [
                {
                    "source": "GitHub",
                    "url": f"https://github.com/example/repo/blob/main/config.py",
                    "type": "API密钥",
                    "value": "sk-...XYZ",
                    "risk": "高"
                },
                {
                    "source": "JavaScript",
                    "url": f"https://{target}/js/app.js",
                    "type": "硬编码密码",
                    "value": "admin123",
                    "risk": "中"
                }
            ]
            
        except Exception as e:
            logger.error(f"搜索 {target} 的暴露凭证时出错: {str(e)}")
            return []
