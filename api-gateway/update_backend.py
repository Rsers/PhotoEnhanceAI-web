#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
后端服务地址更新工具
提供命令行和API两种方式更新后端服务地址
"""

import sys
import requests
import json
import argparse
from config import config

def update_via_file(new_url: str) -> bool:
    """通过配置文件更新"""
    print(f"正在更新后端服务地址为: {new_url}")
    success = config.update_backend_url(new_url)
    
    if success:
        print("✅ 配置文件更新成功")
        print(f"📁 配置文件位置: {config.CONFIG_FILE}")
        return True
    else:
        print("❌ 配置文件更新失败")
        return False

def update_via_api(new_url: str, gateway_url: str = "http://127.0.0.1:5000") -> bool:
    """通过API接口更新"""
    try:
        print(f"正在通过API更新后端服务地址为: {new_url}")
        
        # 发送更新请求
        response = requests.post(
            f"{gateway_url}/api/v1/config/backend",
            json={"backend_url": new_url},
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ API更新成功")
            print(f"📝 响应: {result.get('message', '')}")
            return True
        else:
            print(f"❌ API更新失败: {response.status_code}")
            print(f"📝 错误信息: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到API网关服务")
        print("💡 请确保API网关服务正在运行")
        return False
    except Exception as e:
        print(f"❌ API更新出错: {e}")
        return False

def show_current_config():
    """显示当前配置"""
    config_info = config.get_config_info()
    print("📋 当前配置信息:")
    print(f"  后端服务地址: {config_info['backend_url']}")
    print(f"  超时时间: {config_info['timeout']}秒")
    print(f"  最大文件大小: {config_info['max_file_size']}字节")
    print(f"  配置文件位置: {config_info['config_file']}")

def test_backend_connection(url: str) -> bool:
    """测试后端服务连接"""
    try:
        print(f"🔍 测试后端服务连接: {url}")
        response = requests.get(f"{url}/api/v1/status/test", timeout=5)
        if response.status_code == 200:
            print("✅ 后端服务连接正常")
            return True
        else:
            print(f"⚠️  后端服务响应异常: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到后端服务")
        return False
    except Exception as e:
        print(f"❌ 连接测试失败: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="API网关后端服务地址更新工具")
    parser.add_argument("--url", "-u", help="新的后端服务地址")
    parser.add_argument("--method", "-m", choices=["file", "api"], default="file", 
                       help="更新方式: file(配置文件) 或 api(API接口)")
    parser.add_argument("--gateway", "-g", default="http://127.0.0.1:5000",
                       help="API网关地址 (仅在使用api方式时)")
    parser.add_argument("--show", "-s", action="store_true", help="显示当前配置")
    parser.add_argument("--test", "-t", help="测试指定URL的连接")
    
    args = parser.parse_args()
    
    if args.show:
        show_current_config()
        return
    
    if args.test:
        test_backend_connection(args.test)
        return
    
    if not args.url:
        print("❌ 请提供新的后端服务地址")
        print("💡 使用方法: python3 update_backend.py --url http://新IP:8000")
        return
    
    # 验证URL格式
    if not args.url.startswith(('http://', 'https://')):
        print("❌ 无效的URL格式，请以 http:// 或 https:// 开头")
        return
    
    # 测试新地址连接
    if not test_backend_connection(args.url):
        print("⚠️  警告: 无法连接到新的后端服务地址")
        confirm = input("是否继续更新? (y/N): ")
        if confirm.lower() != 'y':
            print("❌ 更新已取消")
            return
    
    # 执行更新
    if args.method == "file":
        success = update_via_file(args.url)
    else:
        success = update_via_api(args.url, args.gateway)
    
    if success:
        print("\n🎉 更新完成!")
        print("💡 提示: 如果API网关服务正在运行，请重启服务以应用新配置")
        print("💡 重启命令: pkill -f 'python3 app.py' && cd /home/ubuntu/PhotoEnhanceAI-web/api-gateway && python3 app.py &")
    else:
        print("\n❌ 更新失败")
        sys.exit(1)

if __name__ == "__main__":
    main()
