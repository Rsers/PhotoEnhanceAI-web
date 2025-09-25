#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API网关配置文件
支持动态修改后端服务地址
"""

import os
import json
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

# 默认配置
DEFAULT_CONFIG = {
    "backend_api_base": "http://43.143.246.112:8000",
    "backend_timeout": 300,
    "gateway_port": 443,
    "max_file_size": 100 * 1024 * 1024,  # 100MB
    "supported_endpoints": {
        "enhance": "/api/v1/enhance",
        "status": "/api/v1/status",
        "download": "/api/v1/download"
    }
}

# 配置文件路径
CONFIG_FILE = os.path.join(os.path.dirname(__file__), "gateway_config.json")

class GatewayConfig:
    """API网关配置管理类"""
    
    def __init__(self):
        self.config = self.load_config()
    
    def load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        try:
            if os.path.exists(CONFIG_FILE):
                with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    logger.info(f"加载配置文件: {CONFIG_FILE}")
                    return {**DEFAULT_CONFIG, **config}  # 合并默认配置
            else:
                logger.info("配置文件不存在，使用默认配置")
                self.save_config(DEFAULT_CONFIG)
                return DEFAULT_CONFIG.copy()
        except Exception as e:
            logger.error(f"加载配置文件失败: {e}")
            return DEFAULT_CONFIG.copy()
    
    def save_config(self, config: Dict[str, Any]) -> bool:
        """保存配置文件"""
        try:
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            logger.info(f"配置文件已保存: {CONFIG_FILE}")
            return True
        except Exception as e:
            logger.error(f"保存配置文件失败: {e}")
            return False
    
    def update_backend_url(self, new_url: str) -> bool:
        """更新后端服务地址"""
        try:
            # 验证URL格式
            if not new_url.startswith(('http://', 'https://')):
                logger.error(f"无效的URL格式: {new_url}")
                return False
            
            # 更新配置
            self.config["backend_api_base"] = new_url
            success = self.save_config(self.config)
            
            if success:
                logger.info(f"后端服务地址已更新: {new_url}")
            
            return success
        except Exception as e:
            logger.error(f"更新后端服务地址失败: {e}")
            return False
    
    def get_backend_url(self) -> str:
        """获取后端服务地址"""
        return self.config.get("backend_api_base", DEFAULT_CONFIG["backend_api_base"])
    
    def get_timeout(self) -> int:
        """获取超时时间"""
        return self.config.get("backend_timeout", DEFAULT_CONFIG["backend_timeout"])
    
    def get_max_file_size(self) -> int:
        """获取最大文件大小"""
        return self.config.get("max_file_size", DEFAULT_CONFIG["max_file_size"])
    
    def get_endpoints(self) -> Dict[str, str]:
        """获取支持的端点"""
        return self.config.get("supported_endpoints", DEFAULT_CONFIG["supported_endpoints"])
    
    def get_config_info(self) -> Dict[str, Any]:
        """获取配置信息"""
        return {
            "backend_url": self.get_backend_url(),
            "timeout": self.get_timeout(),
            "max_file_size": self.get_max_file_size(),
            "endpoints": self.get_endpoints(),
            "config_file": CONFIG_FILE
        }

# 全局配置实例
config = GatewayConfig()
