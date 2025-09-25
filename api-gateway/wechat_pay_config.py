# 微信支付配置文件
import os
import json
from pathlib import Path

class WeChatPayConfig:
    """微信支付配置类"""
    
    def __init__(self):
        self._load_config()
    
    def _load_config(self):
        """加载配置：优先环境变量，其次配置文件"""
        # 优先从环境变量获取
        self.MCH_ID = os.getenv("WECHAT_MCH_ID", "")
        self.APPID = os.getenv("WECHAT_APPID", "")
        self.SECRET = os.getenv("WECHAT_SECRET", "")
        self.API_KEY = os.getenv("WECHAT_API_KEY", "")
        self.NOTIFY_URL = os.getenv("WECHAT_NOTIFY_URL", "https://www.gongjuxiang.work/api/wechat/pay/notify/")
        
        # 如果环境变量为空，尝试从配置文件读取
        if not all([self.MCH_ID, self.APPID, self.SECRET, self.API_KEY]):
            config_file = os.getenv("WECHAT_CONFIG_FILE", "wechat_config.json")
            config_path = Path(__file__).parent / config_file
            
            if config_path.exists():
                try:
                    with open(config_path, 'r', encoding='utf-8') as f:
                        config_data = json.load(f)
                        
                    self.MCH_ID = self.MCH_ID or config_data.get("mch_id", "")
                    self.APPID = self.APPID or config_data.get("appid", "")
                    self.SECRET = self.SECRET or config_data.get("secret", "")
                    self.API_KEY = self.API_KEY or config_data.get("api_key", "")
                    self.NOTIFY_URL = self.NOTIFY_URL or config_data.get("notify_url", "https://www.gongjuxiang.work/api/wechat/pay/notify/")
                except (json.JSONDecodeError, KeyError) as e:
                    print(f"配置文件解析失败: {e}")
                    pass
    
    # 证书目录配置
    @property
    def cert_dir(self):
        """证书目录路径"""
        # 优先级：环境变量 > 项目根目录certificates/ > api-gateway/certs/
        env_cert_dir = os.getenv("WECHAT_CERT_DIR")
        if env_cert_dir and Path(env_cert_dir).exists():
            return env_cert_dir
            
        project_root = Path(__file__).parent.parent
        certificates_dir = project_root / "certificates"
        if certificates_dir.exists():
            return str(certificates_dir)
            
        local_certs_dir = Path(__file__).parent / "certs"
        return str(local_certs_dir)
    
    @property
    def cert_path(self):
        """证书文件路径"""
        return str(Path(self.cert_dir) / "apiclient_cert.pem")
    
    @property
    def key_path(self):
        """私钥文件路径"""
        return str(Path(self.cert_dir) / "apiclient_key.pem")
    
    # 微信支付API地址
    UNIFIED_ORDER_URL = "https://api.mch.weixin.qq.com/pay/unifiedorder"
    ORDER_QUERY_URL = "https://api.mch.weixin.qq.com/pay/orderquery"
    CLOSE_ORDER_URL = "https://api.mch.weixin.qq.com/pay/closeorder"
    
    def validate(self):
        """验证配置是否完整"""
        required_fields = {
            "MCH_ID": self.MCH_ID,
            "APPID": self.APPID,
            "SECRET": self.SECRET,
            "API_KEY": self.API_KEY
        }
        
        missing_fields = [field for field, value in required_fields.items() if not value]
        if missing_fields:
            raise ValueError(f"缺少必要的配置项: {', '.join(missing_fields)}")
        
        # 检查证书文件
        if not Path(self.cert_path).exists():
            raise FileNotFoundError(f"证书文件不存在: {self.cert_path}")
        if not Path(self.key_path).exists():
            raise FileNotFoundError(f"私钥文件不存在: {self.key_path}")
        
        return True
    
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
