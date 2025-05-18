from flask import Flask, request, jsonify
from flask_cors import CORS  # 添加CORS支持
import cv2
import numpy as np
import mediapipe as mp
from mediapipe_reshape import pre_image
import base64
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import tempfile
import os

app = Flask(__name__)
CORS(app)  # 启用CORS
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max-limit

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 测试连接的根路由
@app.route('/')
def index():
    return jsonify({
        'status': 'success',
        'message': 'API is running'
    })

# 图像处理路由
@app.route('/api/process-image', methods=['POST'])
@limiter.limit("10 per minute")  # 限制每分钟最多10次请求
def process_image():
    if 'file' not in request.files:
        return jsonify({
            'status': 'error',
            'message': 'No file uploaded'
        }), 400
        
    file = request.files['file']
    if not allowed_file(file.filename):
        return jsonify({
            'status': 'error',
            'message': 'Invalid file type. Allowed types: ' + ', '.join(ALLOWED_EXTENSIONS)
        }), 400

    try:
        # 创建临时文件
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
        temp_filename = temp_file.name
        temp_file.close()
        
        # 保存上传的文件到临时文件
        file.save(temp_filename)
        
        # 处理图像
        processed_image, pose_result = pre_image(temp_filename)
        
        # 删除临时文件
        os.unlink(temp_filename)
        
        # 将处理后的图像转换为base64
        _, buffer = cv2.imencode('.jpg', processed_image)
        image_base64 = base64.b64encode(buffer).decode('utf-8')
        
        return jsonify({
            'status': 'success',
            'message': 'Image processed successfully',
            'data': f'data:image/jpeg;base64,{image_base64}',
            'pose': pose_result
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

# 获取系统状态的路由
@app.route('/api/status')
def get_status():
    return jsonify({
        'status': 'success',
        'system_status': 'operational',
        'api_version': '1.0'
    })

@app.errorhandler(413)
def too_large(e):
    return jsonify({
        'status': 'error',
        'message': 'File is too large. Maximum size is 16MB'
    }), 413

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)