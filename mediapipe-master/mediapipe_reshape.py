import random

import cv2
import matplotlib.pyplot as plt
import mediapipe as mp
import time
from tqdm import tqdm
import numpy as np
from PIL import Image, ImageFont, ImageDraw
# ------------------------------------------------
#   mediapipe的初始化
# ------------------------------------------------
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose(static_image_mode=True)

def get_angle(v1, v2):
    angle = np.dot(v1, v2) / (np.sqrt(np.sum(v1 * v1)) * np.sqrt(np.sum(v2 * v2)))
    angle = np.arccos(angle) / 3.14 * 180

    cross = v2[0] * v1[1] - v2[1] * v1[0]
    if cross < 0:
        angle = - angle
    return angle

# ------------------------------------------------
#   计算姿态
# ------------------------------------------------
def get_pos(keypoints):
    str_pose = ""
    # 计算左臂与水平方向的夹角
    keypoints = np.array(keypoints)
    v1 = keypoints[12] - keypoints[11]
    v2 = keypoints[13] - keypoints[11]
    angle_left_arm = get_angle(v1, v2)
    #计算右臂与水平方向的夹角
    v1 = keypoints[11] - keypoints[12]
    v2 = keypoints[14] - keypoints[12]
    angle_right_arm = get_angle(v1, v2)
    #计算左肘的夹角
    v1 = keypoints[11] - keypoints[13]
    v2 = keypoints[15] - keypoints[13]
    angle_left_elow = get_angle(v1, v2)
    # 计算右肘的夹角
    v1 = keypoints[12] - keypoints[14]
    v2 = keypoints[16] - keypoints[14]
    angle_right_elow = get_angle(v1, v2)
    
    # 计算腿部夹角（用于检测跑步姿势）
    try:
        # MediaPipe Pose 关键点：
        # 23: 左髋 (LEFT_HIP)
        # 24: 右髋 (RIGHT_HIP)
        # 25: 左膝 (LEFT_KNEE)
        # 26: 右膝 (RIGHT_KNEE)
        
        # 确保所有需要的关键点都存在且有效
        if '' in [keypoints[23], keypoints[24], keypoints[25], keypoints[26]]:
            print("部分腿部关键点缺失")
            pass
        else:
            # 左腿向量: 左髋到左膝
            left_leg_upper = np.array(keypoints[25]) - np.array(keypoints[23])  # 左膝 - 左髋
            # 右腿向量: 右髋到右膝
            right_leg_upper = np.array(keypoints[26]) - np.array(keypoints[24])  # 右膝 - 右髋
            
            # 确保向量长度不为零
            if np.linalg.norm(left_leg_upper) > 0 and np.linalg.norm(right_leg_upper) > 0:
                # 计算两腿之间的夹角
                legs_angle = abs(get_angle(left_leg_upper, right_leg_upper))
                
                print(f"检测到腿部夹角: {legs_angle}度")
                
                # 如果夹角大于30度，则识别为跑步姿势
                if legs_angle > 30:
                    return "RUN"
    except Exception as e:
        # 如果关键点不存在，忽略这部分检测
        print(f"腿部检测错误: {str(e)}")

    if angle_left_arm<0 and angle_right_arm<0:
        str_pose = "LEFT_UP"
    elif angle_left_arm>0 and angle_right_arm>0:
        str_pose = "RIGHT_UP"
    elif angle_left_arm<0 and angle_right_arm>0:
        str_pose = "ALL_HANDS_UP"
        if abs(angle_left_elow)<120 and abs(angle_right_elow)<120:
            str_pose = "TRIANGLE"
    elif angle_left_arm>0 and angle_right_arm<0:
        str_pose = "NORMAL"
        if abs(angle_left_elow)<120 and abs(angle_right_elow)<120:
            str_pose = "AKIMBO"
    return str_pose

def drawImage(im,chinese,pos,color):
    img_PIL = Image.fromarray(cv2.cvtColor(im,cv2.COLOR_BGR2RGB))
    font = ImageFont.truetype('simsun.ttc',100,encoding="utf-8")
    fillColor = color #(255,0,0)
    position = pos #(100,100)

    draw = ImageDraw.Draw(img_PIL)
    draw.text(position,chinese,fillColor,font)

    img = cv2.cvtColor(np.asarray(img_PIL),cv2.COLOR_RGB2BGR)
    return img
def process_frame(img):
    start_time = time.time()
    h, w = img.shape[0], img.shape[1]               # 高和宽
    # 调整字体
    tl = round(0.005 * (img.shape[0] + img.shape[1]) / 2) + 1
    tf = max(tl-1, 1)
    # BRG-->RGB
    img_RGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # 将RGB图像输入模型，获取 关键点 预测结果
    results = pose.process(img_RGB)
    keypoints = ['' for i in range(33)]
    pose_result = "NO PERSON"
    
    if results.pose_landmarks:
        mp_drawing.draw_landmarks(img, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        for i in range(33):
            cx = int(results.pose_landmarks.landmark[i].x * w)
            cy = int(results.pose_landmarks.landmark[i].y * h)
            keypoints[i] = (cx, cy)                                 # 得到最终的33个关键点
        
        # 获取姿态
        pose_result = get_pos(keypoints)
    else:
        print("NO PERSON")
        struction = "NO PERSON"
        img = cv2.putText(img, struction, (25, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.25, (255, 255, 0),
                          6)
    
    end_time = time.time()
    process_time = end_time - start_time            # 图片关键点预测时间
    fps = 1 / process_time                          # 帧率
    colors = [[random.randint(0,255) for _ in range(3)] for _ in range(33)]
    radius = [random.randint(8,15) for _ in range(33)]
    for i in range(33):
        cx, cy = keypoints[i]
        #if i in range(33):
        img = cv2.circle(img, (cx, cy), radius[i], colors[i], -1)
    
    # 在图像上显示姿态信息
    cv2.putText(img, "POSE-{}".format(pose_result), (12, 50), cv2.FONT_HERSHEY_TRIPLEX,
                tl / 3, (255, 0, 0), thickness=tf)
    cv2.putText(img, "FPS-{}".format(str(int(fps))), (12, 100), cv2.FONT_HERSHEY_SIMPLEX,
                tl/3, (255, 255, 0), thickness=tf)
                
    return img, pose_result



# ------------------------------------------------
#   主函数
# ------------------------------------------------
def pre_image(image_path):
    print(image_path)
    # 读取图像文件
    image = cv2.imread(image_path)
    img = image.copy()
    frame, pose_result = process_frame(img)
    return frame, pose_result
    # 先不显示
def save_image(image, image_path):
    '''
        image是imread读取的图片，
        image_path是保存的路径
    '''
    cv2.imwrite(image_path, image)
if __name__ == '__main__':
    img0 = cv2.imread("./data/outImage--20.jpg")
    image, pose_result = pre_image("./data/outImage--20.jpg")
    '''cv2.namedWindow("frame", cv2.WINDOW_NORMAL)
    cv2.imshow("frame", image)
    cv2.waitKey(0)
    cv2.imwrite("demo/image/out.jpg", image)'''

    # plot显示图像
    fig, axes = plt.subplots(nrows=1, ncols=2)
    axes[0].imshow(img0[:,:,::-1])
    axes[0].set_title("原图")
    axes[1].imshow(image[:,:,::-1])
    axes[1].set_title("检测并可视化后的图片")
    plt.rcParams["font.sans-serif"] = ['SimHei']
    plt.rcParams["axes.unicode_minus"] = False

    plt.show()
    fig.savefig("./data/out.png")





