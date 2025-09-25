# 微信支付配置文件
import os

class WeChatPayConfig:
    """微信支付配置类"""
    
    # 微信支付商户号 (请替换为您的实际商户号)
    MCH_ID = "1900000109"
    
    # 小程序APPID (请替换为您的实际APPID)
    APPID = "wx1234567890abcdef"
    
    # 微信支付API密钥 (请替换为您的实际密钥)
    API_KEY = "your_wechat_pay_api_key_here_32_chars"
    
    # 微信支付证书路径
    CERT_PATH = os.path.join(os.path.dirname(__file__), "certs", "apiclient_cert.pem")
    KEY_PATH = os.path.join(os.path.dirname(__file__), "certs", "apiclient_key.pem")
    
    # 微信支付API地址
    UNIFIED_ORDER_URL = "https://api.mch.weixin.qq.com/pay/unifiedorder"
    ORDER_QUERY_URL = "https://api.mch.weixin.qq.com/pay/orderquery"
    CLOSE_ORDER_URL = "https://api.mch.weixin.qq.com/pay/closeorder"
    
    # 支付回调通知URL
    NOTIFY_URL = "https://your-domain.com/api/wechat/pay/notify"
    
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
