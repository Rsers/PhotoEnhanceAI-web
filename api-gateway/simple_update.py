#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的后端服务地址更新工具（非交互式）
"""

import sys
import json
import os
from config import config

def update_backend_url(new_url: str):
    """更新后端服务地址"""
    print(f"🔄 正在更新后端服务地址为: {new_url}")
    
    # 验证URL格式
    if not new_url.startswith(('http://', 'https://')):
        print("❌ 无效的URL格式，请以 http:// 或 https:// 开头")
        return False
    
    # 更新配置
    success = config.update_backend_url(new_url)
    
    if success:
        print("✅ 配置更新成功")
        config_info = config.get_config_info()
        print(f"📁 配置文件: {config_info['config_file']}")
        return True
    else:
        print("❌ 配置更新失败")
        return False

def main():
    if len(sys.argv) != 2:
        print("❌ 请提供新的后端服务地址")
        print("💡 使用方法: python3 simple_update.py <新IP地址:端口>")
        print("💡 示例: python3 simple_update.py 192.168.1.100:8000")
        return
    
    new_url = sys.argv[1]
    
    # 如果只提供了IP，自动添加http://前缀
    if not new_url.startswith(('http://', 'https://')):
        new_url = f"http://{new_url}"
    
    success = update_backend_url(new_url)
    
    if success:
        print("\n🎉 更新完成!")
        print("💡 提示: 请重启API网关服务以应用新配置")
        print("💡 重启命令: pkill -f 'python3 app.py' && cd /home/ubuntu/PhotoEnhanceAI-web/api-gateway && python3 app.py &")
    else:
        print("\n❌ 更新失败")
        sys.exit(1)

if __name__ == "__main__":
    main()
