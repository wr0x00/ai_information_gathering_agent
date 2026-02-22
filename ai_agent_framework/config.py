"""
Configuration Management for AI Agent Framework
"""
import yaml
import os
from typing import Dict, Any, List, Optional
from pathlib import Path

class ConfigManager:
    """Manages configuration for the AI agent framework"""
    
    def __init__(self, config_path: str = "config.yaml"):
        self.config_path = Path(config_path)
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        if self.config_path.exists():
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f) or {}
        else:
            # Create default configuration
            default_config = self._get_default_config()
            self._save_config(default_config)
            return default_config
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration"""
        return {
            "ai_models": {
                "openai": {
                    "api_key": "your_openai_api_key",
                    "base_url": "https://api.openai.com/v1",
                    "models": [
                        {"name": "gpt-4", "enabled": False},
                        {"name": "gpt-3.5-turbo", "enabled": False}
                    ]
                },
                "anthropic": {
                    "api_key": "your_anthropic_api_key",
                    "base_url": "https://api.anthropic.com/v1",
                    "models": [
                        {"name": "claude-3-opus-20240229", "enabled": False},
                        {"name": "claude-3-sonnet-20240229", "enabled": False}
                    ]
                },
                "google": {
                    "api_key": "your_google_api_key",
                    "base_url": "https://generativelanguage.googleapis.com/v1beta",
                    "models": [
                        {"name": "gemini-pro", "enabled": False}
                    ]
                }
            },
            "http": {
                "timeout": 30,
                "max_concurrent_requests": 10,
                "user_agents": [
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
                ]
            },
            "modules": {
                "whois": {"enabled": True},
                "dns": {"enabled": True},
                "port_scan": {"enabled": True},
                "github_search": {"enabled": True}
            }
        }
    
    def _save_config(self, config: Dict[str, Any]):
        """Save configuration to YAML file"""
        with open(self.config_path, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, default_flow_style=False, allow_unicode=True)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by key (dot notation supported)"""
        keys = key.split('.')
        value = self.config
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key: str, value: Any):
        """Set configuration value by key (dot notation supported)"""
        keys = key.split('.')
        config = self.config
        
        # Navigate to the parent of the target key
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        # Set the value
        config[keys[-1]] = value
        
        # Save the updated configuration
        self._save_config(self.config)
    
    def get_ai_models(self) -> List[Dict[str, Any]]:
        """Get all AI models configuration"""
        return self.config.get("ai_models", {})
    
    def get_enabled_modules(self) -> List[str]:
        """Get list of enabled modules"""
        modules = self.config.get("modules", {})
        return [name for name, config in modules.items() if config.get("enabled", False)]
    
    def get_http_config(self) -> Dict[str, Any]:
        """Get HTTP configuration"""
        return self.config.get("http", {})


# Global configuration manager instance
config_manager = ConfigManager()
