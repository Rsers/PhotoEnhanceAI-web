#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
多GPU服务器管理模块
支持动态添加/删除GPU服务器，负载均衡，健康检测
"""

import os
import json
import logging
import threading
import time
import requests
from typing import Dict, Any, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

# 预设密码
WEBHOOK_SECRET = os.getenv('WEBHOOK_SECRET', 'gpu-server-register-to-api-gateway-2024')

class BackendServer:
    """GPU服务器信息"""
    def __init__(self, server_id: str, ip: str, port: int):
        self.server_id = server_id
        self.ip = ip
        self.port = port
        self.url = f"http://{ip}:{port}"
        self.is_healthy = True
        self.fail_count = 0
        self.last_check_time = datetime.now()
        self.last_used_time = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "server_id": self.server_id,
            "ip": self.ip,
            "port": self.port,
            "url": self.url,
            "is_healthy": self.is_healthy,
            "fail_count": self.fail_count,
            "last_check_time": self.last_check_time.isoformat(),
            "last_used_time": self.last_used_time.isoformat()
        }

class BackendManager:
    """后端服务器管理器"""
    
    def __init__(self):
        self.servers: Dict[str, BackendServer] = {}
        self.current_index = 0
        self.health_check_interval = 30  # 30秒检测间隔
        self.max_fail_count = 3  # 3次失败后标记为不可用
        self.health_check_thread = None
        self.running = False
        
        # 加载已保存的服务器列表
        self.load_servers()
        
        # 启动健康检测
        self.start_health_check()
    
    def load_servers(self):
        """加载服务器列表"""
        try:
            config_file = os.path.join(os.path.dirname(__file__), "backend_servers.json")
            if os.path.exists(config_file):
                with open(config_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for server_data in data:
                        server = BackendServer(
                            server_id=server_data['server_id'],
                            ip=server_data['ip'],
                            port=server_data['port']
                        )
                        self.servers[server.server_id] = server
                logger.info(f"加载了 {len(self.servers)} 台GPU服务器")
        except Exception as e:
            logger.error(f"加载服务器列表失败: {e}")
    
    def save_servers(self):
        """保存服务器列表"""
        try:
            config_file = os.path.join(os.path.dirname(__file__), "backend_servers.json")
            data = [server.to_dict() for server in self.servers.values()]
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            logger.info("服务器列表已保存")
        except Exception as e:
            logger.error(f"保存服务器列表失败: {e}")
    
    def verify_secret(self, secret: str) -> bool:
        """验证密码"""
        return secret == WEBHOOK_SECRET
    
    def generate_server_id(self) -> str:
        """自动生成服务器ID"""
        # 查找下一个可用的GPU编号
        existing_ids = set(self.servers.keys())
        for i in range(1, 1000):  # 最多支持999台服务器
            server_id = f"GPU-{i:03d}"
            if server_id not in existing_ids:
                return server_id
        raise Exception("服务器数量已达上限")
    
    def add_or_update_server(self, ip: str, port: int, secret: str, server_id: str = None) -> tuple[bool, str]:
        """添加或更新GPU服务器，返回(是否成功, server_id)"""
        try:
            # 验证密码
            if not self.verify_secret(secret):
                logger.warning(f"服务器密码验证失败")
                return False, ""
            
            # 检查是否已存在相同IP的服务器
            existing_server = None
            for sid, server in self.servers.items():
                if server.ip == ip and server.port == port:
                    existing_server = sid
                    break
            
            if existing_server:
                # 更新现有服务器
                server = self.servers[existing_server]
                server.ip = ip
                server.port = port
                server.url = f"http://{ip}:{port}"
                server.is_healthy = True
                server.fail_count = 0
                logger.info(f"服务器 {existing_server} 已更新: {ip}:{port}")
                server_id = existing_server
            else:
                # 添加新服务器，自动分配ID
                if not server_id:
                    server_id = self.generate_server_id()
                elif server_id in self.servers:
                    # 如果指定的ID已存在，自动生成新的
                    server_id = self.generate_server_id()
                
                server = BackendServer(server_id, ip, port)
                self.servers[server_id] = server
                logger.info(f"服务器 {server_id} 已添加: {ip}:{port}")
            
            # 保存配置
            self.save_servers()
            
            # 如果这是第一台服务器，启动健康检测
            if len(self.servers) == 1 and not self.running:
                self.start_health_check()
            
            return True, server_id
        except Exception as e:
            logger.error(f"添加/更新服务器失败: {e}")
            return False, ""
    
    def remove_server(self, server_id: str) -> bool:
        """删除GPU服务器"""
        try:
            if server_id in self.servers:
                del self.servers[server_id]
                logger.info(f"服务器 {server_id} 已删除")
                self.save_servers()
                
                # 如果没有服务器了，停止健康检测
                if len(self.servers) == 0:
                    self.stop_health_check()
                
                return True
            return False
        except Exception as e:
            logger.error(f"删除服务器失败: {e}")
            return False
    
    def get_next_server(self) -> Optional[BackendServer]:
        """获取下一个可用的服务器（负载均衡）"""
        if not self.servers:
            return None
        
        # 获取所有健康的服务器
        healthy_servers = [s for s in self.servers.values() if s.is_healthy]
        
        if not healthy_servers:
            logger.warning("没有可用的GPU服务器")
            return None
        
        # 顺序选择服务器（轮询）
        server = healthy_servers[self.current_index % len(healthy_servers)]
        self.current_index += 1
        server.last_used_time = datetime.now()
        
        return server
    
    def check_server_health(self, server: BackendServer) -> bool:
        """检查单个服务器健康状态"""
        try:
            # 尝试访问健康检查端点
            response = requests.get(f"{server.url}/health", timeout=5)
            
            if response.status_code == 200:
                # 健康检查成功
                server.fail_count = 0
                if not server.is_healthy:
                    server.is_healthy = True
                    logger.info(f"服务器 {server.server_id} 重新上线")
                return True
            else:
                server.fail_count += 1
                logger.warning(f"服务器 {server.server_id} 健康检查失败: {response.status_code}")
                return False
                
        except Exception as e:
            server.fail_count += 1
            logger.warning(f"服务器 {server.server_id} 健康检查失败: {e}")
            return False
        finally:
            server.last_check_time = datetime.now()
            
            # 如果失败次数达到阈值，标记为不健康
            if server.fail_count >= self.max_fail_count:
                if server.is_healthy:
                    server.is_healthy = False
                    logger.error(f"服务器 {server.server_id} 已标记为不可用")
    
    def health_check_loop(self):
        """健康检查循环"""
        while self.running:
            try:
                if self.servers:
                    for server in list(self.servers.values()):
                        self.check_server_health(server)
                
                time.sleep(self.health_check_interval)
            except Exception as e:
                logger.error(f"健康检查循环出错: {e}")
                time.sleep(self.health_check_interval)
    
    def start_health_check(self):
        """启动健康检查"""
        if self.servers and not self.running:
            self.running = True
            self.health_check_thread = threading.Thread(target=self.health_check_loop, daemon=True)
            self.health_check_thread.start()
            logger.info("健康检查已启动")
    
    def stop_health_check(self):
        """停止健康检查"""
        self.running = False
        if self.health_check_thread:
            self.health_check_thread.join(timeout=5)
        logger.info("健康检查已停止")
    
    def get_all_servers(self) -> List[Dict[str, Any]]:
        """获取所有服务器信息"""
        return [server.to_dict() for server in self.servers.values()]
    
    def get_server_urls(self) -> List[str]:
        """获取所有健康服务器的URL列表"""
        return [server.url for server in self.servers.values() if server.is_healthy]
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        total = len(self.servers)
        healthy = len([s for s in self.servers.values() if s.is_healthy])
        unhealthy = total - healthy
        
        return {
            "total_servers": total,
            "healthy_servers": healthy,
            "unhealthy_servers": unhealthy,
            "health_check_running": self.running,
            "servers": self.get_all_servers()
        }

# 全局实例
backend_manager = BackendManager()

