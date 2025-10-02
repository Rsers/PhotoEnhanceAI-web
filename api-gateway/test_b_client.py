#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
B服务器测试客户端
用于测试webhook注册功能
"""

import os
import time
import requests
import argparse
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BServerClient:
    """B服务器客户端"""
    
    def __init__(self, gateway_url: str, server_id: str, ip: str, port: int, secret: str):
        self.gateway_url = gateway_url.rstrip('/')
        self.server_id = server_id
        self.ip = ip
        self.port = port
        self.secret = secret
    
    def register(self) -> bool:
        """注册到A服务器"""
        try:
            url = f"{self.gateway_url}/webhook/register"
            data = {
                "server_id": self.server_id,
                "ip": self.ip,
                "port": self.port,
                "secret": self.secret
            }
            
            response = requests.post(url, json=data, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    logger.info(f"✓ 服务器 {self.server_id} 注册成功")
                    logger.info(f"  地址: {self.ip}:{self.port}")
                    return True
                else:
                    logger.error(f"✗ 注册失败: {result.get('error')}")
                    return False
            else:
                logger.error(f"✗ 注册请求失败: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"✗ 注册失败: {e}")
            return False
    
    def unregister(self) -> bool:
        """从A服务器注销"""
        try:
            url = f"{self.gateway_url}/webhook/unregister"
            data = {
                "server_id": self.server_id,
                "secret": self.secret
            }
            
            response = requests.post(url, json=data, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    logger.info(f"✓ 服务器 {self.server_id} 已注销")
                    return True
                else:
                    logger.error(f"✗ 注销失败: {result.get('error')}")
                    return False
            else:
                logger.error(f"✗ 注销请求失败: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"✗ 注销失败: {e}")
            return False
    
    def get_all_servers(self) -> dict:
        """获取所有服务器信息"""
        try:
            url = f"{self.gateway_url}/webhook/servers"
            params = {"secret": self.secret}
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    return result.get('data', {})
                else:
                    logger.error(f"✗ 获取服务器信息失败: {result.get('error')}")
                    return {}
            else:
                logger.error(f"✗ 请求失败: HTTP {response.status_code}")
                return {}
                
        except Exception as e:
            logger.error(f"✗ 获取服务器信息失败: {e}")
            return {}

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='B服务器测试客户端')
    parser.add_argument('action', choices=['register', 'unregister', 'list'], 
                       help='操作: register(注册), unregister(注销), list(列表)')
    parser.add_argument('--gateway', default='https://www.gongjuxiang.work',
                       help='A服务器网关地址')
    parser.add_argument('--server-id', default='B1',
                       help='服务器ID (例如: B1, B2, B3)')
    parser.add_argument('--ip', default='192.168.1.100',
                       help='B服务器IP地址')
    parser.add_argument('--port', type=int, default=8000,
                       help='B服务器端口')
    parser.add_argument('--secret', default='default-secret-2024',
                       help='预设密码')
    
    args = parser.parse_args()
    
    client = BServerClient(
        gateway_url=args.gateway,
        server_id=args.server_id,
        ip=args.ip,
        port=args.port,
        secret=args.secret
    )
    
    if args.action == 'register':
        logger.info(f"正在注册服务器 {args.server_id}...")
        if client.register():
            logger.info("✓ 注册成功")
        else:
            logger.error("✗ 注册失败")
    
    elif args.action == 'unregister':
        logger.info(f"正在注销服务器 {args.server_id}...")
        if client.unregister():
            logger.info("✓ 注销成功")
        else:
            logger.error("✗ 注销失败")
    
    elif args.action == 'list':
        logger.info("正在获取所有服务器信息...")
        stats = client.get_all_servers()
        if stats:
            logger.info(f"\n{'='*50}")
            logger.info(f"总服务器数: {stats.get('total_servers', 0)}")
            logger.info(f"健康服务器: {stats.get('healthy_servers', 0)}")
            logger.info(f"不健康服务器: {stats.get('unhealthy_servers', 0)}")
            logger.info(f"健康检查运行中: {stats.get('health_check_running', False)}")
            logger.info(f"{'='*50}\n")
            
            servers = stats.get('servers', [])
            for server in servers:
                logger.info(f"服务器: {server['server_id']}")
                logger.info(f"  地址: {server['ip']}:{server['port']}")
                logger.info(f"  URL: {server['url']}")
                logger.info(f"  状态: {'健康' if server['is_healthy'] else '不健康'}")
                logger.info(f"  失败次数: {server['fail_count']}")
                logger.info(f"  最后检查: {server['last_check_time']}")
                logger.info("")
        else:
            logger.error("✗ 获取服务器信息失败")

if __name__ == '__main__':
    main()

