#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信支付配置测试脚本
用于验证配置是否正确
"""

from wechat_pay_config import WeChatPayConfig
import os

def test_config():
    """测试配置"""
    print("=== 微信支付配置测试 ===")
    
    # 显示基本配置
    print(f"商户号: {WeChatPayConfig.MCH_ID}")
    print(f"APPID: {WeChatPayConfig.APPID}")
    print(f"API密钥: {WeChatPayConfig.API_KEY[:8]}...{WeChatPayConfig.API_KEY[-8:]}")
    print(f"回调URL: {WeChatPayConfig.NOTIFY_URL}")
    
    # 显示证书路径
    print(f"\n证书目录: {WeChatPayConfig._CERT_DIR}")
    print(f"证书文件: {WeChatPayConfig.CERT_PATH}")
    print(f"私钥文件: {WeChatPayConfig.KEY_PATH}")
    
    # 检查证书文件是否存在
    cert_exists = os.path.exists(WeChatPayConfig.CERT_PATH)
    key_exists = os.path.exists(WeChatPayConfig.KEY_PATH)
    
    print(f"\n证书文件存在: {cert_exists}")
    print(f"私钥文件存在: {key_exists}")
    
    if not cert_exists or not key_exists:
        print("\n⚠️  警告: 证书文件缺失!")
        print("请将以下文件放到相应目录:")
        print(f"  - {WeChatPayConfig.CERT_PATH}")
        print(f"  - {WeChatPayConfig.KEY_PATH}")
        print("\n证书文件获取方法:")
        print("1. 登录微信支付商户平台")
        print("2. 进入 '验证商户身份' 页面")
        print("3. 点击 '商户API证书' 的 '管理证书' 按钮")
        print("4. 下载 apiclient_cert.pem 和 apiclient_key.pem")
    else:
        print("\n✅ 证书文件检查通过!")
    
    # 显示API地址
    print(f"\nAPI地址:")
    print(f"  统一下单: {WeChatPayConfig.UNIFIED_ORDER_URL}")
    print(f"  订单查询: {WeChatPayConfig.ORDER_QUERY_URL}")
    print(f"  关闭订单: {WeChatPayConfig.CLOSE_ORDER_URL}")

if __name__ == "__main__":
    test_config()
