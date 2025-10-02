#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Webhook路由
用于B服务器注册和管理
"""

import logging
from flask import request, jsonify
from backend_manager import backend_manager

logger = logging.getLogger(__name__)

def register_webhook_routes(app):
    """注册webhook路由到Flask应用"""
    
    @app.route('/webhook/register', methods=['POST'])
    def webhook_register():
        """B服务器注册接口"""
        try:
            data = request.get_json()
            if not data:
                return jsonify({'success': False, 'error': '请求数据为空'}), 400
            
            # 验证必需字段
            required_fields = ['server_id', 'ip', 'port', 'secret']
            for field in required_fields:
                if field not in data:
                    return jsonify({'success': False, 'error': f'缺少必需字段: {field}'}), 400
            
            server_id = data['server_id']
            ip = data['ip']
            port = data['port']
            secret = data['secret']
            
            # 添加或更新服务器
            success = backend_manager.add_or_update_server(server_id, ip, port, secret)
            
            if success:
                logger.info(f"服务器 {server_id} 注册成功: {ip}:{port}")
                return jsonify({
                    'success': True,
                    'message': f'服务器 {server_id} 注册成功',
                    'server_id': server_id,
                    'ip': ip,
                    'port': port
                }), 200
            else:
                return jsonify({'success': False, 'error': '密码验证失败'}), 401
                
        except Exception as e:
            logger.error(f"处理注册请求失败: {e}")
            return jsonify({'success': False, 'error': '服务器内部错误'}), 500
    
    @app.route('/webhook/unregister', methods=['POST'])
    def webhook_unregister():
        """B服务器注销接口"""
        try:
            data = request.get_json()
            if not data:
                return jsonify({'success': False, 'error': '请求数据为空'}), 400
            
            # 验证必需字段
            required_fields = ['server_id', 'secret']
            for field in required_fields:
                if field not in data:
                    return jsonify({'success': False, 'error': f'缺少必需字段: {field}'}), 400
            
            server_id = data['server_id']
            secret = data['secret']
            
            # 验证密码
            if not backend_manager.verify_secret(secret):
                return jsonify({'success': False, 'error': '密码验证失败'}), 401
            
            # 删除服务器
            success = backend_manager.remove_server(server_id)
            
            if success:
                logger.info(f"服务器 {server_id} 已注销")
                return jsonify({
                    'success': True,
                    'message': f'服务器 {server_id} 已注销',
                    'server_id': server_id
                }), 200
            else:
                return jsonify({'success': False, 'error': '服务器不存在'}), 404
                
        except Exception as e:
            logger.error(f"处理注销请求失败: {e}")
            return jsonify({'success': False, 'error': '服务器内部错误'}), 500
    
    @app.route('/webhook/servers', methods=['GET'])
    def webhook_get_servers():
        """获取所有服务器信息"""
        try:
            # 可选密码验证
            secret = request.args.get('secret') or (request.get_json() or {}).get('secret')
            if secret and not backend_manager.verify_secret(secret):
                return jsonify({'success': False, 'error': '密码验证失败'}), 401
            
            stats = backend_manager.get_stats()
            return jsonify({
                'success': True,
                'data': stats
            }), 200
                
        except Exception as e:
            logger.error(f"获取服务器信息失败: {e}")
            return jsonify({'success': False, 'error': '服务器内部错误'}), 500
    
    logger.info("Webhook路由已注册")

