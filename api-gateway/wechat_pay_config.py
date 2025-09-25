# 微信支付配置文件
import os

class WeChatPayConfig:
    """微信支付配置类"""
    
    # 微信支付商户号 - 从环境变量获取
    MCH_ID = os.getenv("WECHAT_MCH_ID", "")
    
    # 小程序APPID - 从环境变量获取
    APPID = os.getenv("WECHAT_APPID", "")
    
    # 小程序Secret - 从环境变量获取
    SECRET = os.getenv("WECHAT_SECRET", "")
    
    # 微信支付API密钥 - 从环境变量获取
    API_KEY = os.getenv("WECHAT_API_KEY", "")
    
    # 证书目录：优先使用项目根目录的 certificates/，否则使用本地 certs/
    _THIS_DIR = os.path.dirname(__file__)
    _PROJECT_ROOT = os.path.abspath(os.path.join(_THIS_DIR, os.pardir))
    _CERTIFICATES_DIR = os.path.join(_PROJECT_ROOT, "certificates")
    _LOCAL_CERTS_DIR = os.path.join(_THIS_DIR, "certs")
    
    # 优先使用 certificates/ 目录，如果不存在则使用 certs/ 目录
    _CERT_DIR = _CERTIFICATES_DIR if os.path.isdir(_CERTIFICATES_DIR) else _LOCAL_CERTS_DIR

    # 微信支付证书路径（参考 @certificates/）
    CERT_PATH = os.path.join(_CERT_DIR, "apiclient_cert.pem")
    KEY_PATH = os.path.join(_CERT_DIR, "apiclient_key.pem")
    
    # 微信支付API地址
    UNIFIED_ORDER_URL = "https://api.mch.weixin.qq.com/pay/unifiedorder"
    ORDER_QUERY_URL = "https://api.mch.weixin.qq.com/pay/orderquery"
    CLOSE_ORDER_URL = "https://api.mch.weixin.qq.com/pay/closeorder"
    
    # 支付回调通知URL - 从环境变量获取
    NOTIFY_URL = os.getenv("WECHAT_NOTIFY_URL", "https://www.gongjuxiang.work/api/wechat/pay/notify/")
    
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
