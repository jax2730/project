import cv2
import os

def annotate_images(input_dir, output_dir):
    """
    为指定目录中的所有图片添加"stand"标注
    参数:
        input_dir: 输入图片目录路径
        output_dir: 输出图片目录路径
    """
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    # 遍历输入目录中的所有图片文件
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            # 读取图片
            img_path = os.path.join(input_dir, filename)
            image = cv2.imread(img_path)
            
            if image is not None:
                # 添加"stand"标注
                text = "stand"
                text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
                text_x = (image.shape[1] - text_size[0]) // 2  # 水平居中
                text_y = image.shape[0] - 10  # 图片底部上方
                
                # 绘制文字
                cv2.putText(image, text, (text_x, text_y), 
                          cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
                
                # 保存处理后的图片
                output_path = os.path.join(output_dir, filename)
                cv2.imwrite(output_path, image)

if __name__ == '__main__':
    # 使用示例
    input_folder = "c:/Users/jax/Desktop/mediapipe-master/picture"  # 输入图片目录
    output_folder = "c:/Users/jax/Desktop/mediapipe-master/annotated_images"  # 输出目录
    
    annotate_images(input_folder, output_folder)
    print(f"图片标注完成，结果已保存到 {output_folder}")