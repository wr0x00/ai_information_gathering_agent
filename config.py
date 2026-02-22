from pydantic_settings import BaseSettings
from typing import List, Dict, Optional
import yaml
import os


class Settings(BaseSettings):
    # HTTP设置
    timeout: int = 30
    max_concurrent_requests: int = 10
    user_agents: List[str] = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    ]
    
    # 输出设置
    output_dir: str = "results"
    log_level: str = "INFO"
    
    # API密钥（如果需要）
    github_token: Optional[str] = None
    fofa_email: Optional[str] = None
    fofa_key: Optional[str] = None
    
    class Config:
        env_file = ".env"


class ModuleConfig:
    def __init__(self, config_file: str = "modules.yaml"):
        self.config_file = config_file
        self.modules = self._load_modules()
    
    def _load_modules(self) -> Dict:
        default_config = {
            "whois": {
                "enabled": True,
                "sources": [
                    "https://whois.chinaz.com",
                    "https://bgp.he.net"
                ]
            },
            "domain": {
                "enabled": True,
                "sources": [
                    "https://github.com/wgpsec/ENScan_GO",
                    "https://www.xiaolanben.com/pc",
                    "https://www.qichacha.com",
                    "https://www.tianyancha.com",
                    "https://aiqicha.baidu.com"
                ],
                "subdomain_tools": [
                    "https://github.com/shmilylty/OneForAll",
                    "https://github.com/OWASP/Amass",
                    "https://github.com/projectdiscovery/subfinder"
                ]
            },
            "port": {
                "enabled": True,
                "tools": [
                    "https://nmap.org",
                    "https://github.com/robertdavidgraham/masscan"
                ]
            },
            "sensitive": {
                "enabled": True,
                "google_dorks": [
                    "site:{} intitle:管理|后台|登陆|管理员|系统|内部",
                    "site:{} inurl:login|admin|system|guanli|denglu|manage|admin_login|auth|dev"
                ]
            },
            "github": {
                "enabled": True,
                "sources": [
                    "https://github.com/search?type=code&q={}"
                ]
            }
        }
        
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        else:
            # 创建默认配置文件
            with open(self.config_file, 'w', encoding='utf-8') as f:
                yaml.dump(default_config, f, default_flow_style=False, allow_unicode=True)
            return default_config
    
    def get_enabled_modules(self) -> List[str]:
        return [name for name, config in self.modules.items() if config.get("enabled", False)]
    
    def get_module_config(self, module_name: str) -> Dict:
        return self.modules.get(module_name, {})


settings = Settings()
module_config = ModuleConfig()
