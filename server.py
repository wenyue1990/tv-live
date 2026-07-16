#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
飞牛电视直播后端服务
提供API代理和流媒体转发功能
"""

from flask import Flask, request, Response, send_from_directory, jsonify
from flask_cors import CORS
import requests
import os
import json
from urllib.parse import urlparse

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

# 配置
CONFIG_FILE = 'config.json'
DEFAULT_CONFIG = {
    'port': 8080,
    'default_playlist': 'https://raw.githubusercontent.com/fanmingming/live/main/tv/m3u/global.m3u',
    'proxy_timeout': 10,
    'stream_buffer_size': 8192
}

def load_config():
    """加载配置文件"""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return {**DEFAULT_CONFIG, **json.load(f)}
    return DEFAULT_CONFIG

def save_config(config):
    """保存配置文件"""
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

config = load_config()

# 静态文件服务
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/css/<path:filename>')
def css_files(filename):
    return send_from_directory('css', filename)

@app.route('/js/<path:filename>')
def js_files(filename):
    return send_from_directory('js', filename)

# API代理 - 用于获取远程播放列表
@app.route('/api/proxy')
def proxy():
    """代理请求远程URL"""
    url = request.args.get('url')
    
    if not url:
        return jsonify({'error': 'URL参数缺失'}), 400
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': '*/*'
        }
        
        response = requests.get(url, headers=headers, timeout=config['proxy_timeout'])
        response.raise_for_status()
        
        # 返回内容
        return Response(
            response.content,
            status=response.status_code,
            content_type=response.headers.get('Content-Type', 'text/plain')
        )
        
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'请求失败: {str(e)}'}), 500

# 流媒体代理 - 用于转发视频流
@app.route('/api/stream')
def stream():
    """代理视频流"""
    url = request.args.get('url')
    
    if not url:
        return jsonify({'error': 'URL参数缺失'}), 400
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Referer': url,
            'Origin': urlparse(url).scheme + '://' + urlparse(url).netloc
        }
        
        # 流式响应
        def generate():
            with requests.get(url, headers=headers, stream=True, timeout=30) as response:
                response.raise_for_status()
                for chunk in response.iter_content(chunk_size=config['stream_buffer_size']):
                    if chunk:
                        yield chunk
        
        return Response(
            generate(),
            content_type='video/mp2t'
        )
        
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'流媒体请求失败: {str(e)}'}), 500

# 获取配置
@app.route('/api/config')
def get_config():
    """获取应用配置"""
    return jsonify(config)

# 更新配置
@app.route('/api/config', methods=['POST'])
def update_config():
    """更新应用配置"""
    global config
    
    try:
        new_config = request.get_json()
        config = {**config, **new_config}
        save_config(config)
        return jsonify({'message': '配置已更新'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 健康检查
@app.route('/api/health')
def health_check():
    """健康检查接口"""
    return jsonify({'status': 'ok', 'message': '飞牛直播服务运行中'})

# 错误处理
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': '资源未找到'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': '服务器内部错误'}), 500

if __name__ == '__main__':
    print('=' * 50)
    print('飞牛电视直播服务')
    print('=' * 50)
    print(f'服务地址: http://0.0.0.0:{config["port"]}')
    print(f'默认播放列表: {config["default_playlist"]}')
    print('=' * 50)
    
    app.run(
        host='0.0.0.0',
        port=config['port'],
        debug=False,
        threaded=True
    )