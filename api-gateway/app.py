#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API网关服务
为微信小程序提供HTTPS API接口，代理到基于IP的后端服务
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import requests
import os
import json
import time
from urllib.parse import urljoin
import logging
from config import config

# 导入微信支付相关模块
from wechat_pay_utils import WeChatPayAPI, WeChatPayUtils
from order_manager import OrderManager
from wechat_pay_config import WeChatPayConfig
from wechat_auth import WeChatAuth

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # 允许跨域请求

# 从配置文件获取后端API服务器配置
BACKEND_API_BASE = config.get_backend_url()
BACKEND_TIMEOUT = config.get_timeout()

# 支持的API端点
SUPPORTED_ENDPOINTS = config.get_endpoints()

# 初始化微信支付相关组件
pay_api = WeChatPayAPI()
order_manager = OrderManager()
wechat_auth = WeChatAuth()

@app.route('/api/v1/enhance', methods=['POST'])
def enhance_image():
    """
    图片增强API - 代理到后端服务
    """
    try:
        logger.info("收到图片增强请求")
        
        # 检查是否有文件上传
        if 'file' not in request.files:
            return jsonify({'error': '没有上传文件'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': '文件名为空'}), 400
        
        # 准备转发到后端的请求
        files = {'file': (file.filename, file.stream, file.content_type)}
        
        # 获取其他参数
        data = {}
        if 'tile_size' in request.form:
            data['tile_size'] = request.form['tile_size']
        if 'quality_level' in request.form:
            data['quality_level'] = request.form['quality_level']
        
        # 转发请求到后端
        backend_url = urljoin(BACKEND_API_BASE, '/api/v1/enhance')
        logger.info(f"转发请求到: {backend_url}")
        
        response = requests.post(
            backend_url,
            files=files,
            data=data,
            timeout=BACKEND_TIMEOUT
        )
        
        # 返回后端响应
        return jsonify(response.json()), response.status_code
        
    except requests.exceptions.Timeout:
        logger.error("请求超时")
        return jsonify({'error': '请求超时，请稍后重试'}), 408
    except requests.exceptions.ConnectionError:
        logger.error("连接后端服务失败")
        return jsonify({'error': '服务暂时不可用'}), 503
    except Exception as e:
        logger.error(f"处理请求时出错: {str(e)}")
        return jsonify({'error': '服务器内部错误'}), 500

@app.route('/api/v1/status/<task_id>', methods=['GET'])
def get_task_status(task_id):
    """
    查询任务状态API - 代理到后端服务
    """
    try:
        logger.info(f"查询任务状态: {task_id}")
        
        # 转发请求到后端
        backend_url = urljoin(BACKEND_API_BASE, f'/api/v1/status/{task_id}')
        logger.info(f"转发请求到: {backend_url}")
        
        response = requests.get(backend_url, timeout=30)
        
        # 返回后端响应
        return jsonify(response.json()), response.status_code
        
    except requests.exceptions.Timeout:
        logger.error("请求超时")
        return jsonify({'error': '请求超时'}), 408
    except requests.exceptions.ConnectionError:
        logger.error("连接后端服务失败")
        return jsonify({'error': '服务暂时不可用'}), 503
    except Exception as e:
        logger.error(f"查询状态时出错: {str(e)}")
        return jsonify({'error': '服务器内部错误'}), 500

@app.route('/api/v1/download/<task_id>', methods=['GET'])
def download_result(task_id):
    """
    下载处理结果API - 代理到后端服务
    """
    try:
        logger.info(f"下载任务结果: {task_id}")
        
        # 转发请求到后端
        backend_url = urljoin(BACKEND_API_BASE, f'/api/v1/download/{task_id}')
        logger.info(f"转发请求到: {backend_url}")
        
        response = requests.get(backend_url, timeout=60, stream=True)
        
        if response.status_code == 200:
            # 直接返回文件流
            return send_file(
                response.raw,
                mimetype=response.headers.get('content-type', 'application/octet-stream'),
                as_attachment=True,
                download_name=f'enhanced_{task_id}.jpg'
            )
        else:
            return jsonify(response.json()), response.status_code
        
    except requests.exceptions.Timeout:
        logger.error("下载超时")
        return jsonify({'error': '下载超时'}), 408
    except requests.exceptions.ConnectionError:
        logger.error("连接后端服务失败")
        return jsonify({'error': '服务暂时不可用'}), 503
    except Exception as e:
        logger.error(f"下载时出错: {str(e)}")
        return jsonify({'error': '服务器内部错误'}), 500

@app.route('/api/v1/health', methods=['GET'])
def health_check():
    """
    健康检查接口
    """
    try:
        # 检查后端服务是否可用
        backend_url = urljoin(BACKEND_API_BASE, '/health')
        response = requests.get(backend_url, timeout=5)
        
        return jsonify({
            'status': 'healthy',
            'backend_status': 'connected',
            'backend_response': response.status_code,
            'timestamp': time.time()
        }), 200
        
    except Exception as e:
        # 即使后端不可用，网关本身仍然健康
        return jsonify({
            'status': 'healthy',
            'backend_status': 'disconnected',
            'backend_error': str(e),
            'gateway_status': 'running',
            'timestamp': time.time()
        }), 200

@app.route('/api/v1/info', methods=['GET'])
def api_info():
    """
    API信息接口
    """
    return jsonify({
        'name': 'PhotoEnhance API Gateway',
        'version': '1.0.0',
        'description': '为微信小程序提供HTTPS API接口',
        'endpoints': {
            'enhance': '/api/v1/enhance',
            'status': '/api/v1/status/{task_id}',
            'download': '/api/v1/download/{task_id}',
            'health': '/api/v1/health',
            'info': '/api/v1/info',
            'config': '/api/v1/config',
            'wechat_auth': {
                'openid': '/api/wechat/auth/openid'
            },
            'wechat_pay': {
                'create': '/api/wechat/pay/create',
                'notify': '/api/wechat/pay/notify',
                'query': '/api/wechat/pay/query/{out_trade_no}',
                'orders': '/api/wechat/pay/orders/{openid}',
                'stats': '/api/wechat/pay/stats'
            }
        },
        'backend': config.get_backend_url(),
        'config_info': config.get_config_info()
    })

@app.route('/api/v1/config', methods=['GET'])
def get_config():
    """
    获取配置信息接口
    """
    return jsonify(config.get_config_info())

@app.route('/api/v1/config/backend', methods=['POST'])
def update_backend_config():
    """
    更新后端服务地址接口
    """
    try:
        data = request.get_json()
        if not data or 'backend_url' not in data:
            return jsonify({'error': '缺少backend_url参数'}), 400
        
        new_url = data['backend_url']
        success = config.update_backend_url(new_url)
        
        if success:
            # 重新加载配置
            global BACKEND_API_BASE
            BACKEND_API_BASE = config.get_backend_url()
            
            return jsonify({
                'message': '后端服务地址更新成功',
                'new_backend_url': new_url,
                'timestamp': time.time()
            }), 200
        else:
            return jsonify({'error': '更新失败'}), 500
            
    except Exception as e:
        logger.error(f"更新后端配置时出错: {str(e)}")
        return jsonify({'error': '服务器内部错误'}), 500

# ==================== 微信认证相关API ====================

@app.route('/api/wechat/auth/openid', methods=['POST'])
def get_openid():
    """通过code获取openid"""
    try:
        data = request.get_json()
        
        if not data or 'code' not in data:
            return jsonify({
                'success': False,
                'error': '缺少code参数'
            }), 400
        
        code = data['code']
        result = wechat_auth.get_openid(code)
        
        if result['success']:
            return jsonify({
                'success': True,
                'data': {
                    'openid': result['data']['openid'],
                    'session_key': result['data']['session_key']
                }
            })
        else:
            return jsonify({
                'success': False,
                'error': result['error']
            }), 400
            
    except Exception as e:
        logger.error(f"获取openid失败: {str(e)}")
        return jsonify({
            'success': False,
            'error': '服务器内部错误'
        }), 500

# ==================== 微信支付相关API ====================

@app.route('/api/wechat/pay/create', methods=['POST'])
def create_payment():
    """创建支付订单"""
    try:
        data = request.get_json()
        
        # 验证必要参数
        required_fields = ['openid', 'total_fee', 'body']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'缺少必要参数: {field}'
                }), 400
        
        openid = data['openid']
        total_fee = int(data['total_fee'])  # 单位：分
        body = data['body']
        attach = data.get('attach', '')
        
        # 验证金额
        if total_fee <= 0 or total_fee > 1000000:  # 最大10000元
            return jsonify({
                'success': False,
                'error': '金额无效'
            }), 400
        
        # 创建本地订单
        order = order_manager.create_order(openid, total_fee, body, attach)
        
        # 调用微信支付API创建订单
        result = pay_api.create_order(openid, total_fee, body, attach)
        
        if result['success']:
            # 更新本地订单的prepay_id
            order_manager.update_order(
                order['out_trade_no'],
                prepay_id=result['data']['prepay_id']
            )
            
            return jsonify({
                'success': True,
                'data': {
                    'out_trade_no': order['out_trade_no'],
                    'pay_params': result['data']['pay_params']
                }
            })
        else:
            # 创建失败，删除本地订单
            order_manager.mark_order_failed(order['out_trade_no'])
            return jsonify({
                'success': False,
                'error': result['error']
            }), 500
            
    except Exception as e:
        logger.error(f"创建支付订单失败: {str(e)}")
        return jsonify({
            'success': False,
            'error': '服务器内部错误'
        }), 500

@app.route('/api/wechat/pay/notify', methods=['POST'])
def payment_notify():
    """支付回调通知"""
    try:
        # 获取回调数据
        xml_data = request.get_data(as_text=True)
        logger.info(f"收到支付回调: {xml_data}")
        
        # 解析XML数据
        callback_data = WeChatPayUtils.xml_to_dict(xml_data)
        
        # 验证签名
        sign = callback_data.pop('sign', '')
        if not WeChatPayUtils.verify_sign(callback_data, sign, WeChatPayConfig.API_KEY):
            logger.error("支付回调签名验证失败")
            return WeChatPayUtils.dict_to_xml({
                'return_code': 'FAIL',
                'return_msg': '签名验证失败'
            })
        
        # 检查支付结果
        if callback_data.get('return_code') == 'SUCCESS' and callback_data.get('result_code') == 'SUCCESS':
            out_trade_no = callback_data.get('out_trade_no')
            transaction_id = callback_data.get('transaction_id')
            time_end = callback_data.get('time_end')
            
            # 更新订单状态
            if order_manager.mark_order_paid(out_trade_no, transaction_id, time_end):
                logger.info(f"订单支付成功: {out_trade_no}")
                
                # 这里可以添加业务逻辑，比如：
                # - 发送支付成功通知
                # - 更新用户权益
                # - 记录支付日志
                
                return WeChatPayUtils.dict_to_xml({
                    'return_code': 'SUCCESS',
                    'return_msg': 'OK'
                })
            else:
                logger.error(f"更新订单状态失败: {out_trade_no}")
                return WeChatPayUtils.dict_to_xml({
                    'return_code': 'FAIL',
                    'return_msg': '订单不存在'
                })
        else:
            logger.error(f"支付失败: {callback_data}")
            return WeChatPayUtils.dict_to_xml({
                'return_code': 'FAIL',
                'return_msg': '支付失败'
            })
            
    except Exception as e:
        logger.error(f"处理支付回调失败: {str(e)}")
        return WeChatPayUtils.dict_to_xml({
            'return_code': 'FAIL',
            'return_msg': '处理失败'
        })

@app.route('/api/wechat/pay/query/<out_trade_no>', methods=['GET'])
def query_payment(out_trade_no):
    """查询支付状态"""
    try:
        # 先查询本地订单
        local_order = order_manager.get_order(out_trade_no)
        if not local_order:
            return jsonify({
                'success': False,
                'error': '订单不存在'
            }), 404
        
        # 如果本地订单已支付，直接返回
        if local_order['status'] == WeChatPayConfig.ORDER_STATUS_PAID:
            return jsonify({
                'success': True,
                'data': {
                    'out_trade_no': out_trade_no,
                    'status': local_order['status'],
                    'transaction_id': local_order['transaction_id'],
                    'time_end': local_order['time_end']
                }
            })
        
        # 查询微信支付状态
        result = pay_api.query_order(out_trade_no)
        
        if result['success']:
            trade_state = result['data']['trade_state']
            
            # 根据微信支付状态更新本地订单
            if trade_state == 'SUCCESS':
                order_manager.mark_order_paid(
                    out_trade_no,
                    result['data']['transaction_id'],
                    result['data']['time_end']
                )
            elif trade_state in ['CLOSED', 'REVOKED', 'PAYERROR']:
                order_manager.mark_order_failed(out_trade_no)
            
            return jsonify({
                'success': True,
                'data': result['data']
            })
        else:
            return jsonify({
                'success': False,
                'error': result['error']
            }), 500
            
    except Exception as e:
        logger.error(f"查询支付状态失败: {str(e)}")
        return jsonify({
            'success': False,
            'error': '服务器内部错误'
        }), 500

@app.route('/api/wechat/pay/orders/<openid>', methods=['GET'])
def get_user_orders(openid):
    """获取用户订单列表"""
    try:
        orders = order_manager.get_orders_by_openid(openid)
        
        # 只返回必要信息，不包含敏感数据
        safe_orders = []
        for order in orders:
            safe_orders.append({
                'out_trade_no': order['out_trade_no'],
                'total_fee': order['total_fee'],
                'body': order['body'],
                'status': order['status'],
                'create_time': order['create_time'],
                'time_end': order['time_end']
            })
        
        return jsonify({
            'success': True,
            'data': safe_orders
        })
        
    except Exception as e:
        logger.error(f"获取用户订单失败: {str(e)}")
        return jsonify({
            'success': False,
            'error': '服务器内部错误'
        }), 500

@app.route('/api/wechat/pay/stats', methods=['GET'])
def get_payment_stats():
    """获取支付统计信息"""
    try:
        stats = order_manager.get_order_stats()
        return jsonify({
            'success': True,
            'data': stats
        })
        
    except Exception as e:
        logger.error(f"获取支付统计失败: {str(e)}")
        return jsonify({
            'success': False,
            'error': '服务器内部错误'
        }), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'API接口不存在'}), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({'error': 'HTTP方法不允许'}), 405

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': '服务器内部错误'}), 500

if __name__ == '__main__':
    logger.info("启动API网关服务...")
    logger.info(f"后端API地址: {BACKEND_API_BASE}")
    logger.info("使用HTTPS协议，端口443")
    
    # 配置SSL证书路径
    ssl_cert = '/etc/letsencrypt/live/www.gongjuxiang.work/fullchain.pem'
    ssl_key = '/etc/letsencrypt/live/www.gongjuxiang.work/privkey.pem'
    
    # 检查SSL证书是否存在
    import os
    if os.path.exists(ssl_cert) and os.path.exists(ssl_key):
        logger.info("使用SSL证书启动HTTPS服务")
        app.run(host='0.0.0.0', port=443, ssl_context=(ssl_cert, ssl_key), debug=False)
    else:
        logger.warning("SSL证书不存在，使用HTTP服务（仅用于开发）")
        logger.warning("生产环境请配置SSL证书")
        app.run(host='0.0.0.0', port=5000, debug=False)
