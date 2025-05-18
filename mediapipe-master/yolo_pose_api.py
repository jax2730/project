from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np
import base64
import tempfile
import os
from ultralytics import YOLO # 导入 YOLO

app = Flask(__name__)
CORS(app) # 启用CORS

# 加载 YOLOv11 姿态检测模型
# 请确保 'yolov11-pose.pt' 文件位于正确的位置，例如项目根目录或指定路径
# 如果模型文件有不同的名称或路径，请修改此处
try:
    YOLO_POSE_MODEL = YOLO('yolov11-pose.pt')
    print("YOLOv11 pose model loaded successfully.")
except Exception as e:
    print(f"Error loading YOLOv11 pose model: {e}")
    YOLO_POSE_MODEL = None # 如果加载失败，将模型设为 None

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
MAX_FILE_SIZE = 16 * 1024 * 1024 # 16MB max-limit
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# YOLO姿态检测路由
@app.route('/yolo/process-image', methods=['POST'])
def yolo_process_image():
    if YOLO_POSE_MODEL is None:
        return jsonify({
            'status': 'error',
            'message': 'YOLOv11 pose model failed to load.'
        }), 500

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

    # 可选：检查文件大小（尽管Flask配置了MAX_CONTENT_LENGTH，但提前检查更友好）
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0) # 移回文件开头
    if file_size > MAX_FILE_SIZE:
         return jsonify({
            'status': 'error',
            'message': f'File is too large. Maximum size is {MAX_FILE_SIZE / 1024 / 1024}MB'
        }), 413


    # 创建临时文件保存上传的图像
    temp_dir = tempfile.gettempdir() # 使用系统临时目录
    temp_filepath = os.path.join(temp_dir, file.filename)

    try:
        # 保存上传的文件到临时文件
        file.save(temp_filepath)

        # 使用OpenCV读取图像 (YOLO通常处理BGR格式)
        image_bgr = cv2.imread(temp_filepath)
        if image_bgr is None:
             return jsonify({
                'status': 'error',
                'message': 'Could not read image file.'
            }), 400

        # 执行YOLO姿态检测推理
        results = YOLO_POSE_MODEL(image_bgr, verbose=False) # results is a list of Results objects

        annotated_image_bgr = image_bgr.copy() # 复制原图用于绘制
        pose_result = "NO PERSON" # 默认姿态

        # 提取关键点和姿态信息
        extracted_keypoints_list = [] # 存储所有检测到的人体的关键点
        if results and len(results) > 0:
            for result in results:
                 if result.keypoints is not None and result.keypoints.xy.numel() > 0:
                    # 绘制关键点和骨骼线
                    annotated_image_bgr = result.plot(img=annotated_image_bgr, boxes=False, labels=False, conf=False) # 在复制的图像上绘制

                    # 提取关键点数据 (像素坐标)
                    person_keypoints = result.keypoints.xy[0].cpu().numpy() # 假设处理第一个检测到的人体
                    extracted_keypoints_list.append(person_keypoints)

                    # TODO: 根据 YOLO 关键点实现更复杂的姿态判断
                    # 注意：YOLO 姿态模型的关键点索引可能与 MediaPipe 不同
                    # 你需要查阅 YOLO 姿态模型的文档来确定关键点索引，
                    # 然后根据提取的 person_keypoints 数据实现姿态判断逻辑
                    # 例如，判断 RUN 姿态可能需要计算 YOLO 关键点中髋部和膝盖的夹角

                    # For now, a simple placeholder: if any person detected, mark as "POSE_DETECTED"
                    # You will replace this with actual pose classification based on YOLO keypoints
                    pose_result = "POSE_DETECTED (YOLO)" # 简单标记为已检测到姿态

        # 将处理后的图像转换为base64
        # annotated_image_bgr 是BGR格式，需要转为RGB才能正确编码为JPEG
        annotated_image_rgb = cv2.cvtColor(annotated_image_bgr, cv2.COLOR_BGR2RGB)
        _, buffer = cv2.imencode('.jpg', annotated_image_rgb)
        image_base64 = base64.b64encode(buffer).decode('utf-8')

        return jsonify({
            'status': 'success',
            'message': 'Image processed successfully by YOLOv11.',
            'data': f'data:image/jpeg;base64,{image_base64}',
            'pose': pose_result # 返回简化的姿态结果
        }), 200

    except Exception as e:
        print(f"YOLO processing error: {e}")
        return jsonify({
            'status': 'error',
            'message': f'YOLO processing error: {str(e)}'
        }), 500
    finally:
        # 删除临时文件
        if os.path.exists(temp_filepath):
            os.unlink(temp_filepath)


if __name__ == '__main__':
    # 运行在不同于原来Flask应用的端口，例如 5001
    app.run(debug=True, host='0.0.0.0', port=5001) 