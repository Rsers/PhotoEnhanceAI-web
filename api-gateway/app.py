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

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # 允许跨域请求

# 后端API服务器配置
BACKEND_API_BASE = "http://43.143.246.112:8000"
BACKEND_TIMEOUT = 300  # 5分钟超时

# 支持的API端点
SUPPORTED_ENDPOINTS = {
    'enhance': '/api/v1/enhance',
    'status': '/api/v1/status',
    'download': '/api/v1/download'
}

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
        backend_url = urljoin(BACKEND_API_BASE, '/api/v1/status/test')
        response = requests.get(backend_url, timeout=5)
        
        return jsonify({
            'status': 'healthy',
            'backend_status': 'connected',
            'backend_response': response.status_code,
            'timestamp': time.time()
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'backend_status': 'disconnected',
            'error': str(e),
            'timestamp': time.time()
        }), 503

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
            'info': '/api/v1/info'
        },
        'backend': BACKEND_API_BASE
    })

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
    app.run(host='0.0.0.0', port=5000, debug=False)
