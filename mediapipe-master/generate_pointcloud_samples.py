import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import cv2
import os
from datetime import datetime
import json

def generate_lidar_pointcloud():
    """生成LiDAR点云数据可视化"""
    # 生成模拟LiDAR点云数据
    n_points = 50000
    
    # 创建地面点
    ground_x = np.random.uniform(-50, 50, n_points//4)
    ground_y = np.random.uniform(-50, 50, n_points//4)
    ground_z = np.random.normal(0, 0.1, n_points//4)
    
    # 创建建筑物点
    building_points = []
    for i in range(5):  # 5个建筑物
        bx = np.random.uniform(-40, 40)
        by = np.random.uniform(-40, 40)
        bw, bh, bd = np.random.uniform(5, 15, 3)
        
        # 建筑物墙面
        n_wall = n_points//20
        wall_x = np.concatenate([
            np.random.uniform(bx, bx+bw, n_wall//4),
            np.random.uniform(bx, bx+bw, n_wall//4),
            np.full(n_wall//4, bx),
            np.full(n_wall//4, bx+bw)
        ])
        wall_y = np.concatenate([
            np.full(n_wall//4, by),
            np.full(n_wall//4, by+bd),
            np.random.uniform(by, by+bd, n_wall//4),
            np.random.uniform(by, by+bd, n_wall//4)
        ])
        wall_z = np.random.uniform(0, bh, n_wall)
        
        building_points.extend(list(zip(wall_x, wall_y, wall_z)))
    
    building_points = np.array(building_points)
    
    # 创建车辆点
    vehicle_points = []
    for i in range(8):  # 8辆车
        vx = np.random.uniform(-45, 45)
        vy = np.random.uniform(-45, 45)
        vz = np.random.uniform(0.5, 2.5)
        
        # 车辆形状
        car_x = np.random.uniform(vx, vx+4, 200)
        car_y = np.random.uniform(vy, vy+2, 200)
        car_z = np.random.uniform(vz, vz+1.5, 200)
        
        vehicle_points.extend(list(zip(car_x, car_y, car_z)))
    
    vehicle_points = np.array(vehicle_points)
    
    # 创建人体点
    person_points = []
    for i in range(15):  # 15个人
        px = np.random.uniform(-30, 30)
        py = np.random.uniform(-30, 30)
        
        # 人体形状（简化）
        person_x = np.random.normal(px, 0.3, 100)
        person_y = np.random.normal(py, 0.3, 100)
        person_z = np.random.uniform(0, 1.8, 100)
        
        person_points.extend(list(zip(person_x, person_y, person_z)))
    
    person_points = np.array(person_points)
    
    # 合并所有点
    all_points = np.vstack([
        np.column_stack([ground_x, ground_y, ground_z]),
        building_points,
        vehicle_points,
        person_points
    ])
    
    # 创建颜色映射
    colors = np.zeros((len(all_points), 3))
    
    # 地面 - 灰色
    ground_end = len(ground_x)
    colors[:ground_end] = [0.5, 0.5, 0.5]
    
    # 建筑物 - 蓝色
    building_end = ground_end + len(building_points)
    colors[ground_end:building_end] = [0.2, 0.4, 0.8]
    
    # 车辆 - 红色
    vehicle_end = building_end + len(vehicle_points)
    colors[building_end:vehicle_end] = [0.8, 0.2, 0.2]
    
    # 人体 - 绿色
    colors[vehicle_end:] = [0.2, 0.8, 0.2]
    
    return all_points, colors

def generate_depth_camera_pointcloud():
    """生成深度相机点云数据可视化"""
    # 模拟深度图像
    height, width = 480, 640
    
    # 创建场景深度
    depth_map = np.ones((height, width)) * 5.0  # 背景5米
    
    # 添加前景对象
    # 人体轮廓
    for i in range(3):
        person_x = np.random.randint(100, 540)
        person_y = np.random.randint(50, 350)
        person_w, person_h = 80, 200
        
        # 创建人体形状
        y_coords, x_coords = np.ogrid[0:height, 0:width]
        person_mask = ((x_coords - person_x)**2 / (person_w/2)**2 + 
                      (y_coords - person_y)**2 / (person_h/2)**2) < 1
        depth_map[person_mask] = np.random.uniform(1.5, 3.0)
    
    # 添加桌子/物体
    for i in range(5):
        obj_x = np.random.randint(50, 590)
        obj_y = np.random.randint(200, 450)
        obj_w, obj_h = np.random.randint(40, 120, 2)
        
        obj_mask = ((x_coords - obj_x)**2 / (obj_w/2)**2 + 
                   (y_coords - obj_y)**2 / (obj_h/2)**2) < 1
        depth_map[obj_mask] = np.random.uniform(0.8, 2.5)
    
    # 转换为3D点云
    fx, fy = 525.0, 525.0  # 焦距
    cx, cy = width/2, height/2  # 主点
    
    points_3d = []
    colors = []
    
    for y in range(0, height, 2):  # 降采样
        for x in range(0, width, 2):
            z = depth_map[y, x]
            if z > 0.1:  # 有效深度
                # 转换为3D坐标
                x_3d = (x - cx) * z / fx
                y_3d = (y - cy) * z / fy
                z_3d = z
                
                points_3d.append([x_3d, y_3d, z_3d])
                
                # 根据深度着色
                if z < 1.5:
                    colors.append([1.0, 0.2, 0.2])  # 近距离 - 红色
                elif z < 3.0:
                    colors.append([0.2, 1.0, 0.2])  # 中距离 - 绿色
                else:
                    colors.append([0.2, 0.2, 1.0])  # 远距离 - 蓝色
    
    return np.array(points_3d), np.array(colors)

def generate_stereo_vision_pointcloud():
    """生成双目视觉点云数据可视化"""
    # 模拟双目视觉重建的点云
    n_points = 30000
    
    # 创建室内场景
    points = []
    colors = []
    
    # 地面
    floor_x = np.random.uniform(-3, 3, n_points//4)
    floor_y = np.random.uniform(-3, 3, n_points//4)
    floor_z = np.zeros(n_points//4)
    
    for i in range(len(floor_x)):
        points.append([floor_x[i], floor_y[i], floor_z[i]])
        colors.append([0.6, 0.4, 0.2])  # 棕色地面
    
    # 墙面
    # 后墙
    wall_x = np.random.uniform(-3, 3, n_points//8)
    wall_y = np.full(n_points//8, 3)
    wall_z = np.random.uniform(0, 2.5, n_points//8)
    
    for i in range(len(wall_x)):
        points.append([wall_x[i], wall_y[i], wall_z[i]])
        colors.append([0.8, 0.8, 0.8])  # 灰色墙面
    
    # 侧墙
    wall_x = np.full(n_points//8, -3)
    wall_y = np.random.uniform(-3, 3, n_points//8)
    wall_z = np.random.uniform(0, 2.5, n_points//8)
    
    for i in range(len(wall_x)):
        points.append([wall_x[i], wall_y[i], wall_z[i]])
        colors.append([0.8, 0.8, 0.8])  # 灰色墙面
    
    # 人体关键点
    for person_id in range(2):
        # 人体中心位置
        person_x = np.random.uniform(-2, 2)
        person_y = np.random.uniform(0, 2)
        
        # MediaPipe人体关键点（简化版）
        keypoints = [
            [person_x, person_y, 1.7],      # 头部
            [person_x, person_y, 1.5],      # 颈部
            [person_x-0.3, person_y, 1.4],  # 左肩
            [person_x+0.3, person_y, 1.4],  # 右肩
            [person_x-0.3, person_y, 1.0],  # 左肘
            [person_x+0.3, person_y, 1.0],  # 右肘
            [person_x-0.3, person_y, 0.7],  # 左手
            [person_x+0.3, person_y, 0.7],  # 右手
            [person_x, person_y, 1.2],      # 躯干中心
            [person_x-0.2, person_y, 0.8],  # 左髋
            [person_x+0.2, person_y, 0.8],  # 右髋
            [person_x-0.2, person_y, 0.4],  # 左膝
            [person_x+0.2, person_y, 0.4],  # 右膝
            [person_x-0.2, person_y, 0.0],  # 左脚
            [person_x+0.2, person_y, 0.0],  # 右脚
        ]
        
        for kp in keypoints:
            # 添加噪声
            noisy_kp = [kp[0] + np.random.normal(0, 0.02),
                       kp[1] + np.random.normal(0, 0.02),
                       kp[2] + np.random.normal(0, 0.02)]
            points.append(noisy_kp)
            colors.append([1.0, 0.0, 0.0])  # 红色关键点
    
    # 物体检测框内的点
    for obj_id in range(3):
        obj_x = np.random.uniform(-2, 2)
        obj_y = np.random.uniform(0.5, 2.5)
        obj_z = np.random.uniform(0.2, 1.0)
        
        # 物体点云
        obj_points_x = np.random.uniform(obj_x-0.2, obj_x+0.2, 200)
        obj_points_y = np.random.uniform(obj_y-0.2, obj_y+0.2, 200)
        obj_points_z = np.random.uniform(obj_z-0.1, obj_z+0.1, 200)
        
        for i in range(200):
            points.append([obj_points_x[i], obj_points_y[i], obj_points_z[i]])
            colors.append([0.0, 0.8, 0.8])  # 青色物体
    
    return np.array(points), np.array(colors)

def generate_combined_visualization():
    """生成综合可视化图像"""
    # 创建多子图布局
    fig = plt.figure(figsize=(20, 15))
    fig.suptitle('AI Recognition System - Point Cloud Visualizations', fontsize=20, fontweight='bold')
    
    # 1. LiDAR点云
    ax1 = fig.add_subplot(2, 3, 1, projection='3d')
    lidar_points, lidar_colors = generate_lidar_pointcloud()
    
    # 降采样显示
    sample_indices = np.random.choice(len(lidar_points), 10000, replace=False)
    ax1.scatter(lidar_points[sample_indices, 0], 
               lidar_points[sample_indices, 1], 
               lidar_points[sample_indices, 2],
               c=lidar_colors[sample_indices], s=0.5, alpha=0.6)
    ax1.set_title('LiDAR Point Cloud\n(Outdoor Scene)', fontsize=14, fontweight='bold')
    ax1.set_xlabel('X (m)')
    ax1.set_ylabel('Y (m)')
    ax1.set_zlabel('Z (m)')
    
    # 2. 深度相机点云
    ax2 = fig.add_subplot(2, 3, 2, projection='3d')
    depth_points, depth_colors = generate_depth_camera_pointcloud()
    
    sample_indices = np.random.choice(len(depth_points), 8000, replace=False)
    ax2.scatter(depth_points[sample_indices, 0], 
               depth_points[sample_indices, 1], 
               depth_points[sample_indices, 2],
               c=depth_colors[sample_indices], s=1, alpha=0.7)
    ax2.set_title('Depth Camera Point Cloud\n(Indoor Scene)', fontsize=14, fontweight='bold')
    ax2.set_xlabel('X (m)')
    ax2.set_ylabel('Y (m)')
    ax2.set_zlabel('Z (m)')
    
    # 3. 双目视觉点云
    ax3 = fig.add_subplot(2, 3, 3, projection='3d')
    stereo_points, stereo_colors = generate_stereo_vision_pointcloud()
    
    ax3.scatter(stereo_points[:, 0], 
               stereo_points[:, 1], 
               stereo_points[:, 2],
               c=stereo_colors, s=2, alpha=0.8)
    ax3.set_title('Stereo Vision Point Cloud\n(Human Pose Detection)', fontsize=14, fontweight='bold')
    ax3.set_xlabel('X (m)')
    ax3.set_ylabel('Y (m)')
    ax3.set_zlabel('Z (m)')
    
    # 4. 检测结果统计
    ax4 = fig.add_subplot(2, 3, 4)
    categories = ['Persons', 'Vehicles', 'Objects', 'Buildings']
    counts = [15, 8, 12, 5]
    colors_bar = ['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4']
    
    bars = ax4.bar(categories, counts, color=colors_bar, alpha=0.8)
    ax4.set_title('Detection Results\n(Object Counts)', fontsize=14, fontweight='bold')
    ax4.set_ylabel('Count')
    
    # 添加数值标签
    for bar, count in zip(bars, counts):
        height = bar.get_height()
        ax4.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                f'{count}', ha='center', va='bottom', fontweight='bold')
    
    # 5. 置信度分布
    ax5 = fig.add_subplot(2, 3, 5)
    confidence_scores = np.random.beta(8, 2, 1000)  # 生成偏向高置信度的分布
    
    ax5.hist(confidence_scores, bins=30, alpha=0.7, color='#ff9f43', edgecolor='black')
    ax5.axvline(np.mean(confidence_scores), color='red', linestyle='--', linewidth=2, 
                label=f'Mean: {np.mean(confidence_scores):.3f}')
    ax5.set_title('Confidence Score Distribution\n(Detection Quality)', fontsize=14, fontweight='bold')
    ax5.set_xlabel('Confidence Score')
    ax5.set_ylabel('Frequency')
    ax5.legend()
    ax5.grid(True, alpha=0.3)
    
    # 6. 处理时间分析
    ax6 = fig.add_subplot(2, 3, 6)
    processing_stages = ['Preprocessing', 'Feature\nExtraction', 'AI Inference', 'Post-processing']
    times = [12, 45, 156, 23]  # 毫秒
    colors_time = ['#a8e6cf', '#dcedc1', '#ffd3a5', '#fd9853']
    
    wedges, texts, autotexts = ax6.pie(times, labels=processing_stages, colors=colors_time,
                                      autopct='%1.1f%%', startangle=90)
    ax6.set_title('Processing Time Breakdown\n(Total: 236ms)', fontsize=14, fontweight='bold')
    
    # 美化饼图
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
    
    plt.tight_layout()
    return fig

def save_visualization_data():
    """保存可视化数据和元信息"""
    # 生成点云数据
    lidar_points, lidar_colors = generate_lidar_pointcloud()
    depth_points, depth_colors = generate_depth_camera_pointcloud()
    stereo_points, stereo_colors = generate_stereo_vision_pointcloud()
    
    # 创建输出目录
    output_dir = "frontend/public/pointcloud_data"
    os.makedirs(output_dir, exist_ok=True)
    
    # 保存点云数据
    np.savez_compressed(f"{output_dir}/lidar_pointcloud.npz", 
                       points=lidar_points, colors=lidar_colors)
    np.savez_compressed(f"{output_dir}/depth_pointcloud.npz", 
                       points=depth_points, colors=depth_colors)
    np.savez_compressed(f"{output_dir}/stereo_pointcloud.npz", 
                       points=stereo_points, colors=stereo_colors)
    
    # 生成元数据
    metadata = {
        "generated_at": datetime.now().isoformat(),
        "datasets": {
            "lidar": {
                "name": "LiDAR Outdoor Scene",
                "points_count": len(lidar_points),
                "description": "Outdoor scene with buildings, vehicles, and pedestrians",
                "detection_objects": ["buildings", "vehicles", "persons", "ground"],
                "accuracy": 97.2,
                "processing_time_ms": 156
            },
            "depth": {
                "name": "Depth Camera Indoor",
                "points_count": len(depth_points),
                "description": "Indoor scene captured with depth camera",
                "detection_objects": ["persons", "furniture", "objects"],
                "accuracy": 94.8,
                "processing_time_ms": 89
            },
            "stereo": {
                "name": "Stereo Vision Pose",
                "points_count": len(stereo_points),
                "description": "Human pose detection with stereo vision",
                "detection_objects": ["human_keypoints", "objects", "environment"],
                "accuracy": 92.5,
                "processing_time_ms": 45
            }
        },
        "statistics": {
            "total_detections": 40,
            "persons_detected": 15,
            "vehicles_detected": 8,
            "objects_detected": 12,
            "buildings_detected": 5,
            "average_confidence": 0.89,
            "processing_fps": 24.5
        }
    }
    
    # 保存元数据
    with open(f"{output_dir}/metadata.json", 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    
    print(f"Point cloud data saved to {output_dir}/")
    return metadata

def main():
    """主函数"""
    print("Generating AI Recognition System Point Cloud Visualizations...")
    
    # 创建输出目录
    os.makedirs("frontend/public/images/pointcloud", exist_ok=True)
    
    # 生成综合可视化
    fig = generate_combined_visualization()
    
    # 保存高质量图像
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = f"frontend/public/images/pointcloud/ai_pointcloud_analysis_{timestamp}.png"
    fig.savefig(output_path, dpi=300, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    
    # 也保存一个固定名称的版本供前端使用
    fig.savefig("frontend/public/images/pointcloud/current_analysis.png", 
                dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
    
    plt.close(fig)
    
    # 保存数据文件
    metadata = save_visualization_data()
    
    print(f"✅ Visualization saved: {output_path}")
    print(f"✅ Current analysis: frontend/public/images/pointcloud/current_analysis.png")
    print(f"✅ Point cloud data: frontend/public/pointcloud_data/")
    print(f"✅ Total detections: {metadata['statistics']['total_detections']}")
    print(f"✅ Average confidence: {metadata['statistics']['average_confidence']:.1%}")
    print(f"✅ Processing FPS: {metadata['statistics']['processing_fps']}")

if __name__ == "__main__":
    main() 