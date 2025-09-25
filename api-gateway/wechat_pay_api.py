# 微信支付API路由
from flask import Flask, request, jsonify
from wechat_pay_utils import WeChatPayAPI, WeChatPayUtils
from order_manager import OrderManager
from wechat_pay_config import WeChatPayConfig
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 创建Flask应用
app = Flask(__name__)

# 初始化支付API和订单管理器
pay_api = WeChatPayAPI()
order_manager = OrderManager()

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
