# 订单管理模块
import json
import os
import time
from datetime import datetime
from wechat_pay_config import WeChatPayConfig

class OrderManager:
    """订单管理类"""
    
    def __init__(self):
        self.orders_file = os.path.join(os.path.dirname(__file__), "data", "orders.json")
        self._ensure_data_dir()
        self._load_orders()
    
    def _ensure_data_dir(self):
        """确保数据目录存在"""
        data_dir = os.path.dirname(self.orders_file)
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
    
    def _load_orders(self):
        """加载订单数据"""
        if os.path.exists(self.orders_file):
            try:
                with open(self.orders_file, 'r', encoding='utf-8') as f:
                    self.orders = json.load(f)
            except:
                self.orders = {}
        else:
            self.orders = {}
    
    def _save_orders(self):
        """保存订单数据"""
        with open(self.orders_file, 'w', encoding='utf-8') as f:
            json.dump(self.orders, f, ensure_ascii=False, indent=2)
    
    def create_order(self, openid, total_fee, body, attach=""):
        """创建订单"""
        from wechat_pay_utils import WeChatPayUtils
        
        out_trade_no = WeChatPayUtils.generate_out_trade_no()
        
        order = {
            'out_trade_no': out_trade_no,
            'openid': openid,
            'total_fee': total_fee,
            'body': body,
            'attach': attach,
            'status': WeChatPayConfig.ORDER_STATUS_PENDING,
            'create_time': datetime.now().isoformat(),
            'update_time': datetime.now().isoformat(),
            'transaction_id': '',
            'time_end': ''
        }
        
        self.orders[out_trade_no] = order
        self._save_orders()
        
        return order
    
    def update_order(self, out_trade_no, **kwargs):
        """更新订单"""
        if out_trade_no in self.orders:
            self.orders[out_trade_no].update(kwargs)
            self.orders[out_trade_no]['update_time'] = datetime.now().isoformat()
            self._save_orders()
            return True
        return False
    
    def get_order(self, out_trade_no):
        """获取订单"""
        return self.orders.get(out_trade_no)
    
    def get_orders_by_openid(self, openid):
        """根据openid获取订单列表"""
        user_orders = []
        for order in self.orders.values():
            if order['openid'] == openid:
                user_orders.append(order)
        
        # 按创建时间倒序排列
        user_orders.sort(key=lambda x: x['create_time'], reverse=True)
        return user_orders
    
    def mark_order_paid(self, out_trade_no, transaction_id, time_end):
        """标记订单为已支付"""
        return self.update_order(
            out_trade_no,
            status=WeChatPayConfig.ORDER_STATUS_PAID,
            transaction_id=transaction_id,
            time_end=time_end
        )
    
    def mark_order_cancelled(self, out_trade_no):
        """标记订单为已取消"""
        return self.update_order(
            out_trade_no,
            status=WeChatPayConfig.ORDER_STATUS_CANCELLED
        )
    
    def mark_order_failed(self, out_trade_no):
        """标记订单为支付失败"""
        return self.update_order(
            out_trade_no,
            status=WeChatPayConfig.ORDER_STATUS_FAILED
        )
    
    def get_order_stats(self):
        """获取订单统计信息"""
        stats = {
            'total': len(self.orders),
            'pending': 0,
            'paid': 0,
            'cancelled': 0,
            'failed': 0,
            'refunded': 0
        }
        
        for order in self.orders.values():
            status = order['status']
            if status in stats:
                stats[status] += 1
        
        return stats
