# 微信登录认证模块
import requests
import json
from wechat_pay_config import WeChatPayConfig

class WeChatAuth:
    """微信登录认证类"""
    
    def __init__(self):
        self.config = WeChatPayConfig()
        self.appid = self.config.APPID
        self.secret = self.config.SECRET
    
    def get_openid(self, code):
        """通过code获取openid"""
        url = "https://api.weixin.qq.com/sns/jscode2session"
        
        params = {
            'appid': self.appid,
            'secret': self.secret,
            'js_code': code,
            'grant_type': 'authorization_code'
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            result = response.json()
            
            if 'openid' in result:
                return {
                    'success': True,
                    'data': {
                        'openid': result['openid'],
                        'session_key': result.get('session_key', ''),
                        'unionid': result.get('unionid', '')
                    }
                }
            else:
                return {
                    'success': False,
                    'error': result.get('errmsg', '获取openid失败'),
                    'errcode': result.get('errcode', -1)
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f'请求失败: {str(e)}'
            }
