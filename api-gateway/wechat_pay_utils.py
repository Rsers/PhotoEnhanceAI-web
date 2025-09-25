# 微信支付工具类
import hashlib
import hmac
import json
import random
import string
import time
import xml.etree.ElementTree as ET
from urllib.parse import urlencode
import requests
from wechat_pay_config import WeChatPayConfig

class WeChatPayUtils:
    """微信支付工具类"""
    
    @staticmethod
    def generate_nonce_str(length=32):
        """生成随机字符串"""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    
    @staticmethod
    def generate_timestamp():
        """生成时间戳"""
        return str(int(time.time()))
    
    @staticmethod
    def generate_out_trade_no():
        """生成商户订单号"""
        timestamp = int(time.time())
        random_str = ''.join(random.choices(string.digits, k=6))
        return f"PAY{timestamp}{random_str}"
    
    @staticmethod
    def sign_md5(params, api_key):
        """MD5签名"""
        # 1. 参数排序
        sorted_params = sorted(params.items())
        
        # 2. 拼接字符串
        string_a = '&'.join([f"{k}={v}" for k, v in sorted_params if v])
        string_sign_temp = f"{string_a}&key={api_key}"
        
        # 3. MD5加密
        sign = hashlib.md5(string_sign_temp.encode('utf-8')).hexdigest().upper()
        return sign
    
    @staticmethod
    def sign_hmac_sha256(params, api_key):
        """HMAC-SHA256签名"""
        # 1. 参数排序
        sorted_params = sorted(params.items())
        
        # 2. 拼接字符串
        string_a = '&'.join([f"{k}={v}" for k, v in sorted_params if v])
        
        # 3. HMAC-SHA256加密
        sign = hmac.new(
            api_key.encode('utf-8'),
            string_a.encode('utf-8'),
            hashlib.sha256
        ).hexdigest().upper()
        return sign
    
    @staticmethod
    def dict_to_xml(data):
        """字典转XML"""
        xml = "<xml>"
        for key, value in data.items():
            xml += f"<{key}><![CDATA[{value}]]></{key}>"
        xml += "</xml>"
        return xml
    
    @staticmethod
    def xml_to_dict(xml_str):
        """XML转字典"""
        root = ET.fromstring(xml_str)
        result = {}
        for child in root:
            result[child.tag] = child.text
        return result
    
    @staticmethod
    def verify_sign(data, sign, api_key, sign_type="MD5"):
        """验证签名"""
        if sign_type == "MD5":
            calculated_sign = WeChatPayUtils.sign_md5(data, api_key)
        elif sign_type == "HMAC-SHA256":
            calculated_sign = WeChatPayUtils.sign_hmac_sha256(data, api_key)
        else:
            return False
        
        return calculated_sign == sign

class WeChatPayAPI:
    """微信支付API类"""
    
    def __init__(self):
        self.config = WeChatPayConfig()
    
    def create_order(self, openid, total_fee, body, attach=""):
        """创建支付订单"""
        # 构建请求参数
        params = {
            'appid': self.config.APPID,
            'mch_id': self.config.MCH_ID,
            'nonce_str': WeChatPayUtils.generate_nonce_str(),
            'body': body,
            'out_trade_no': WeChatPayUtils.generate_out_trade_no(),
            'total_fee': total_fee,  # 单位：分
            'spbill_create_ip': '127.0.0.1',
            'notify_url': self.config.NOTIFY_URL,
            'trade_type': self.config.TRADE_TYPE_JSAPI,
            'openid': openid,
            'attach': attach
        }
        
        # 添加签名
        params['sign'] = WeChatPayUtils.sign_md5(params, self.config.API_KEY)
        
        # 转换为XML
        xml_data = WeChatPayUtils.dict_to_xml(params)
        
        try:
            # 发送请求
            response = requests.post(
                self.config.UNIFIED_ORDER_URL,
                data=xml_data.encode('utf-8'),
                headers={'Content-Type': 'application/xml'},
                timeout=30
            )
            
            # 解析响应
            result = WeChatPayUtils.xml_to_dict(response.text)
            
            if result.get('return_code') == 'SUCCESS' and result.get('result_code') == 'SUCCESS':
                # 构建小程序支付参数
                pay_params = {
                    'appId': self.config.APPID,
                    'timeStamp': WeChatPayUtils.generate_timestamp(),
                    'nonceStr': WeChatPayUtils.generate_nonce_str(),
                    'package': f"prepay_id={result['prepay_id']}",
                    'signType': 'MD5'
                }
                
                # 添加签名
                pay_params['paySign'] = WeChatPayUtils.sign_md5(pay_params, self.config.API_KEY)
                
                return {
                    'success': True,
                    'data': {
                        'out_trade_no': params['out_trade_no'],
                        'prepay_id': result['prepay_id'],
                        'pay_params': pay_params
                    }
                }
            else:
                return {
                    'success': False,
                    'error': result.get('err_code_des', '创建订单失败')
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f'请求失败: {str(e)}'
            }
    
    def query_order(self, out_trade_no):
        """查询订单状态"""
        params = {
            'appid': self.config.APPID,
            'mch_id': self.config.MCH_ID,
            'out_trade_no': out_trade_no,
            'nonce_str': WeChatPayUtils.generate_nonce_str()
        }
        
        # 添加签名
        params['sign'] = WeChatPayUtils.sign_md5(params, self.config.API_KEY)
        
        # 转换为XML
        xml_data = WeChatPayUtils.dict_to_xml(params)
        
        try:
            response = requests.post(
                self.config.ORDER_QUERY_URL,
                data=xml_data.encode('utf-8'),
                headers={'Content-Type': 'application/xml'},
                timeout=30
            )
            
            result = WeChatPayUtils.xml_to_dict(response.text)
            
            if result.get('return_code') == 'SUCCESS' and result.get('result_code') == 'SUCCESS':
                return {
                    'success': True,
                    'data': {
                        'out_trade_no': result.get('out_trade_no'),
                        'transaction_id': result.get('transaction_id'),
                        'trade_state': result.get('trade_state'),
                        'total_fee': result.get('total_fee'),
                        'time_end': result.get('time_end')
                    }
                }
            else:
                return {
                    'success': False,
                    'error': result.get('err_code_des', '查询订单失败')
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f'查询失败: {str(e)}'
            }
