from base_module import BaseModule
from typing import Dict, Any, List
import asyncio
import logging
from urllib.parse import quote_plus

logger = logging.getLogger(__name__)


class GithubModule(BaseModule):
    """在GitHub上搜索敏感信息和代码的模块"""
    
    def __init__(self):
        super().__init__("github")
        self.github_search_url = "https://github.com/search"
        self.search_patterns = [
            "@{}.com password",
            "@{}.com secret",
            "@{}.com credentials",
            "@{}.com token",
            "@{}.com config",
            "@{}.com pass",
            "@{}.com login",
            "@{}.com ftp",
            "@{}.com ssh",
            "@{}.com pwd",
            "@{}.com security_credentials",
            "@{}.com connetionstring",
            "@{}.com JDBC",
            "@{}.com ssh2_auth_password",
            "@{}.com send_keys"
        ]
    
    async def execute(self, target: str) -> Dict[str, Any]:
        """
        执行GitHub代码搜索以查找敏感信息
        
        参数:
            target: 要在GitHub上搜索的目标域名/组织
            
        返回:
            包含GitHub搜索结果的字典
        """
        logger.info(f"开始对 {target} 进行GitHub代码搜索")
        
        # 清除之前的结果
        self.clear_results()
        
        # 搜索敏感信息
        sensitive_results = await self._search_sensitive_info(target)
        self.store_result("sensitive_info", sensitive_results)
        
        # 搜索代码片段
        code_results = await self._search_code_snippets(target)
        self.store_result("code_snippets", code_results)
        
        # 搜索配置文件
        config_results = await self._search_config_files(target)
        self.store_result("config_files", config_results)
        
        self.store_result("target", target)
        
        logger.info(f"完成对 {target} 的GitHub代码搜索")
        return self.get_results()
    
    async def _search_sensitive_info(self, target: str) -> List[Dict[str, Any]]:
        """
        在GitHub上搜索敏感信息
        
        参数:
            target: 目标域名/组织
            
        返回:
            敏感信息发现结果列表
        """
        results = []
        
        # 为使用不同模式搜索创建任务
        tasks = []
        for pattern in self.search_patterns:
            search_query = pattern.format(target)
            task = self._github_search(search_query)
            tasks.append(task)
        
        # 并发运行所有任务
        search_results = await self.run_tasks(tasks)
        
        # 处理结果
        for i, result in enumerate(search_results):
            if result:
                pattern = self.search_patterns[i]
                results.extend(result)
        
        return results
    
    async def _github_search(self, query: str) -> List[Dict[str, Any]]:
        """
        使用给定查询执行GitHub搜索
        
        参数:
            query: 搜索查询
            
        返回:
            搜索结果列表
        """
        try:
            # 出于演示目的，我们正在模拟响应
            # 在实际实现中，您将与GitHub API交互
            # 或抓取GitHub搜索结果
            
            # 模拟搜索结果
            if "password" in query or "pass" in query:
                return [
                    {
                        "url": "https://github.com/example/repo/blob/main/config.py",
                        "snippet": "password = 'supersecretpassword123'",
                        "file": "config.py",
                        "repo": "example/repo",
                        "stars": 42
                    },
                    {
                        "url": "https://github.com/company/project/blob/master/src/auth.js",
                        "snippet": "const PASS = 'adminPass2023!'",
                        "file": "auth.js",
                        "repo": "company/project",
                        "stars": 156
                    }
                ]
            elif "secret" in query or "token" in query:
                return [
                    {
                        "url": "https://github.com/dev/application/blob/main/.env",
                        "snippet": "API_SECRET=sk-1234567890abcdef",
                        "file": ".env",
                        "repo": "dev/application",
                        "stars": 89
                    },
                    {
                        "url": "https://github.com/team/service/blob/dev/settings.json",
                        "snippet": "\"access_token\": \"ghp_xyz789abcdef123456\"",
                        "file": "settings.json",
                        "repo": "team/service",
                        "stars": 210
                    }
                ]
            elif "credentials" in query:
                return [
                    {
                        "url": "https://github.com/org/project/blob/main/src/db.py",
                        "snippet": "creds = {'user': 'admin', 'password': 'dbpass456'}",
                        "file": "db.py",
                        "repo": "org/project",
                        "stars": 34
                    }
                ]
            elif "config" in query:
                return [
                    {
                        "url": "https://github.com/user/webapp/blob/master/config.xml",
                        "snippet": "<database><host>prod.db.internal</host><pass>prodpass789</pass></database>",
                        "file": "config.xml",
                        "repo": "user/webapp",
                        "stars": 67
                    }
                ]
            else:
                return [
                    {
                        "url": f"https://github.com/search?q={quote_plus(query)}",
                        "snippet": f"'{query}' 的搜索结果",
                        "file": "search",
                        "repo": "github",
                        "stars": 0
                    }
                ]
                
        except Exception as e:
            logger.error(f"执行 '{query}' 的GitHub搜索时出错: {str(e)}")
            return []
    
    async def _search_code_snippets(self, target: str) -> List[Dict[str, Any]]:
        """
        搜索与目标相关的代码片段
        
        参数:
            target: 目标域名/组织
            
        返回:
            代码片段发现结果列表
        """
        try:
            # 出于演示目的，我们正在模拟响应
            # 在实际实现中，您将搜索实际的代码片段
            
            # 常见的代码搜索查询
            queries = [
                f"filename:.env {target}",
                f"extension:.sql {target}",
                f"filename:config.php {target}",
                f"filename:wp-config.php {target}",
                f"filename:.htpasswd {target}"
            ]
            
            # 为每个查询创建任务
            tasks = []
            for query in queries:
                task = self._github_search(query)
                tasks.append(task)
            
            # 并发运行所有任务
            results = await self.run_tasks(tasks)
            
            # 展平结果
            flattened_results = []
            for result in results:
                if result:
                    flattened_results.extend(result)
            
            return flattened_results
            
        except Exception as e:
            logger.error(f"搜索 {target} 的代码片段时出错: {str(e)}")
            return []
    
    async def _search_config_files(self, target: str) -> List[Dict[str, Any]]:
        """
        搜索与目标相关的配置文件
        
        参数:
            target: 目标域名/组织
            
        返回:
            配置文件发现结果列表
        """
        try:
            # 出于演示目的，我们正在模拟响应
            # 在实际实现中，您将搜索实际的配置文件
            
            # 常见的配置文件搜索查询
            queries = [
                f"filename:config.json {target}",
                f"filename:settings.py {target}",
                f"filename:application.properties {target}",
                f"filename:web.config {target}",
                f"filename:.bashrc {target}"
            ]
            
            # 为每个查询创建任务
            tasks = []
            for query in queries:
                task = self._github_search(query)
                tasks.append(task)
            
            # 并发运行所有任务
            results = await self.run_tasks(tasks)
            
            # 展平结果
            flattened_results = []
            for result in results:
                if result:
                    flattened_results.extend(result)
            
            return flattened_results
            
        except Exception as e:
            logger.error(f"搜索 {target} 的配置文件时出错: {str(e)}")
            return []
