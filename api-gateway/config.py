#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API网关配置文件
支持动态修改后端服务地址和多GPU服务器管理
"""

import os
import json
import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

# 默认配置
DEFAULT_CONFIG = {
    "backend_api_base": None,  # 不再硬编码IP，由GPU服务器动态提供
    "backend_timeout": 300,
    "gateway_port": 443,
    "max_file_size": 100 * 1024 * 1024,  # 100MB
    "supported_endpoints": {
        "enhance": "/api/v1/enhance",
        "status": "/api/v1/status",
        "download": "/api/v1/download"
    },
    # 多GPU服务器配置
    "multi_backend": {
        "enabled": True,  # 是否启用多GPU服务器模式
        "fallback_to_default": False,  # 没有GPU服务器时不回退，直接报错
    }
}

# 配置文件路径
CONFIG_FILE = os.path.join(os.path.dirname(__file__), "gateway_config.json")

class GatewayConfig:
    """API网关配置管理类"""
    
    def __init__(self):
        self.config = self.load_config()
        self.backend_manager = None  # 延迟导入避免循环依赖
    
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
    
    def _get_backend_manager(self):
        """延迟导入backend_manager避免循环依赖"""
        if self.backend_manager is None:
            try:
                from backend_manager import backend_manager
                self.backend_manager = backend_manager
            except ImportError:
                logger.warning("backend_manager未找到，使用默认配置")
                self.backend_manager = None
        return self.backend_manager
    
    def get_backend_url(self) -> Optional[str]:
        """获取后端服务地址（支持多GPU服务器）"""
        # 检查是否启用多GPU服务器模式
        if not self.config.get("multi_backend", {}).get("enabled", False):
            # 如果禁用了多GPU服务器模式，检查是否有配置的默认地址
            default_url = self.config.get("backend_api_base")
            if default_url:
                return default_url
            else:
                logger.error("多GPU服务器模式已禁用且未配置默认后端地址")
                return None
        
        # 尝试从backend_manager获取服务器
        backend_manager = self._get_backend_manager()
        if backend_manager:
            selected_server = backend_manager.get_next_server()
            if selected_server:
                logger.debug(f"使用GPU服务器: {selected_server.server_id} ({selected_server.ip})")
                return selected_server.url
        
        # 没有可用的GPU服务器，检查是否回退到默认配置
        if self.config.get("multi_backend", {}).get("fallback_to_default", False):
            default_url = self.config.get("backend_api_base")
            if default_url:
                logger.warning("没有可用的GPU服务器，回退到默认配置")
                return default_url
            else:
                logger.error("没有可用的GPU服务器且未配置默认地址")
                return None
        else:
            logger.error("没有可用的GPU服务器且未启用回退模式")
            return None
    
    def get_all_backend_urls(self) -> List[str]:
        """获取所有可用的后端服务器地址"""
        backend_manager = self._get_backend_manager()
        if backend_manager:
            return backend_manager.get_server_urls()
        else:
            default_url = self.config.get("backend_api_base")
            return [default_url] if default_url else []
    
    def update_backend_url(self, new_url: str) -> bool:
        """更新默认后端服务地址"""
        try:
            # 验证URL格式
            if not new_url.startswith(('http://', 'https://')):
                logger.error(f"无效的URL格式: {new_url}")
                return False
            
            # 更新配置
            self.config["backend_api_base"] = new_url
            success = self.save_config(self.config)
            
            if success:
                logger.info(f"默认后端服务地址已更新: {new_url}")
            
            return success
        except Exception as e:
            logger.error(f"更新后端服务地址失败: {e}")
            return False
    
    def enable_multi_backend(self, enabled: bool = True) -> bool:
        """启用/禁用多GPU服务器模式"""
        try:
            if "multi_backend" not in self.config:
                self.config["multi_backend"] = {}
            
            self.config["multi_backend"]["enabled"] = enabled
            success = self.save_config(self.config)
            
            if success:
                status = "启用" if enabled else "禁用"
                logger.info(f"多GPU服务器模式已{status}")
            
            return success
        except Exception as e:
            logger.error(f"设置多GPU服务器模式失败: {e}")
            return False
    
    def set_fallback_to_default(self, fallback: bool = True) -> bool:
        """设置是否回退到默认配置"""
        try:
            if "multi_backend" not in self.config:
                self.config["multi_backend"] = {}
            
            self.config["multi_backend"]["fallback_to_default"] = fallback
            success = self.save_config(self.config)
            
            if success:
                status = "启用" if fallback else "禁用"
                logger.info(f"回退到默认配置已{status}")
            
            return success
        except Exception as e:
            logger.error(f"设置回退模式失败: {e}")
            return False
    
    def get_timeout(self) -> int:
        """获取超时时间"""
        return self.config.get("backend_timeout", DEFAULT_CONFIG["backend_timeout"])
    
    def get_max_file_size(self) -> int:
        """获取最大文件大小"""
        return self.config.get("max_file_size", DEFAULT_CONFIG["max_file_size"])
    
    def get_endpoints(self) -> Dict[str, str]:
        """获取支持的端点"""
        return self.config.get("supported_endpoints", DEFAULT_CONFIG["supported_endpoints"])
    
    def is_multi_backend_enabled(self) -> bool:
        """检查是否启用多GPU服务器模式"""
        return self.config.get("multi_backend", {}).get("enabled", False)
    
    def is_fallback_enabled(self) -> bool:
        """检查是否启用回退模式"""
        return self.config.get("multi_backend", {}).get("fallback_to_default", False)
    
    def get_config_info(self) -> Dict[str, Any]:
        """获取配置信息"""
        backend_manager = self._get_backend_manager()
        backend_stats = None
        if backend_manager:
            backend_stats = backend_manager.get_stats()
        
        return {
            "backend_url": self.get_backend_url(),
            "default_backend_url": self.config.get("backend_api_base"),
            "timeout": self.get_timeout(),
            "max_file_size": self.get_max_file_size(),
            "endpoints": self.get_endpoints(),
            "config_file": CONFIG_FILE,
            "multi_backend": {
                "enabled": self.is_multi_backend_enabled(),
                "fallback_to_default": self.is_fallback_enabled()
            },
            "backend_servers": backend_stats
        }

# 全局配置实例
config = GatewayConfig()
