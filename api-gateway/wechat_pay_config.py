# 微信支付配置文件
import os

class WeChatPayConfig:
    """微信支付配置类"""
    
    # 允许环境变量覆盖配置
    _ENV_MCH_ID = os.getenv("WECHAT_MCH_ID")
    _ENV_APPID = os.getenv("WECHAT_APPID")
    _ENV_API_KEY = os.getenv("WECHAT_API_KEY")
    _ENV_NOTIFY_URL = os.getenv("WECHAT_NOTIFY_URL")
    _ENV_CERT_DIR = os.getenv("WECHAT_CERT_DIR")

    # 微信支付商户号 (请替换为您的实际商户号)
    MCH_ID = _ENV_MCH_ID or "1581082441"
    
    # 小程序APPID (请替换为您的实际APPID)
    APPID = _ENV_APPID or "wx3b37b90a51e1612d"
    
    # 微信支付API密钥 (请替换为您的实际密钥)
    API_KEY = _ENV_API_KEY or "k8Xp2Aq9LmN5rT7vEwZ1sY4uH6cBnJ3d"
    
    # 证书目录优先级：环境变量 -> 项目根 certificates/ -> 模块 certs/
    _THIS_DIR = os.path.dirname(__file__)
    _PROJECT_ROOT = os.path.abspath(os.path.join(_THIS_DIR, os.pardir))
    _CANDIDATE_CERT_DIRS = [
        _ENV_CERT_DIR,
        os.path.join(_PROJECT_ROOT, "certificates"),
        os.path.join(_THIS_DIR, "certs"),
    ]
    _CERT_DIR = next((d for d in _CANDIDATE_CERT_DIRS if d and os.path.isdir(d)), os.path.join(_THIS_DIR, "certs"))

    # 微信支付证书路径（参考 @certificates/）
    CERT_PATH = os.path.join(_CERT_DIR, "apiclient_cert.pem")
    KEY_PATH = os.path.join(_CERT_DIR, "apiclient_key.pem")
    
    # 微信支付API地址
    UNIFIED_ORDER_URL = "https://api.mch.weixin.qq.com/pay/unifiedorder"
    ORDER_QUERY_URL = "https://api.mch.weixin.qq.com/pay/orderquery"
    CLOSE_ORDER_URL = "https://api.mch.weixin.qq.com/pay/closeorder"
    
    # 支付回调通知URL
    NOTIFY_URL = _ENV_NOTIFY_URL or "https://your-domain.com/api/wechat/pay/notify"
    
    # 交易类型
    TRADE_TYPE_JSAPI = "JSAPI"  # 小程序支付
    
    # 签名类型
    SIGN_TYPE_MD5 = "MD5"
    SIGN_TYPE_HMAC_SHA256 = "HMAC-SHA256"
    
    # 货币类型
    FEE_TYPE_CNY = "CNY"
    
    # 订单状态
    ORDER_STATUS_PENDING = "PENDING"      # 待支付
    ORDER_STATUS_PAID = "PAID"            # 已支付
    ORDER_STATUS_CANCELLED = "CANCELLED"  # 已取消
    ORDER_STATUS_REFUNDED = "REFUNDED"    # 已退款
    ORDER_STATUS_FAILED = "FAILED"        # 支付失败
