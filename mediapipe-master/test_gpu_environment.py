#!/usr/bin/env python3
"""
GPU训练环境测试脚本
验证PyTorch CUDA支持和Ultralytics YOLO GPU训练
"""

import torch
import sys
import os
from ultralytics import YOLO
import time

def check_gpu_environment():
    """检查GPU环境配置"""
    print("=" * 60)
    print("GPU训练环境检查")
    print("=" * 60)
    
    # PyTorch基础信息
    print(f"Python版本: {sys.version}")
    print(f"PyTorch版本: {torch.__version__}")
    print(f"CUDA版本: {torch.version.cuda}")
    print(f"cuDNN版本: {torch.backends.cudnn.version()}")
    
    # GPU信息
    print(f"\nCUDA可用: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"GPU数量: {torch.cuda.device_count()}")
        for i in range(torch.cuda.device_count()):
            props = torch.cuda.get_device_properties(i)
            memory_gb = props.total_memory / 1024**3
            print(f"GPU {i}: {props.name} ({memory_gb:.1f}GB)")
        print(f"当前设备: cuda:{torch.cuda.current_device()}")
    else:
        print("❌ CUDA不可用，将使用CPU训练")
        return False
    
    # 内存测试
    print(f"\n内存测试:")
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        memory_allocated = torch.cuda.memory_allocated() / 1024**2
        memory_cached = torch.cuda.memory_reserved() / 1024**2
        print(f"已分配GPU内存: {memory_allocated:.1f}MB")
        print(f"缓存GPU内存: {memory_cached:.1f}MB")
    
    return True

def test_simple_tensor_operations():
    """测试基础GPU张量运算"""
    print("\n" + "=" * 60)
    print("GPU张量运算测试")
    print("=" * 60)
    
    if not torch.cuda.is_available():
        print("❌ CUDA不可用，跳过GPU测试")
        return False
    
    try:
        # 创建测试张量
        device = torch.device('cuda:0')
        print(f"使用设备: {device}")
        
        # 基础运算测试
        x = torch.randn(1000, 1000, device=device)
        y = torch.randn(1000, 1000, device=device)
        
        start_time = time.time()
        z = torch.matmul(x, y)
        gpu_time = time.time() - start_time
        
        print(f"✅ GPU矩阵乘法测试通过")
        print(f"GPU运算时间: {gpu_time:.4f}秒")
        print(f"结果张量形状: {z.shape}")
        print(f"结果张量设备: {z.device}")
        
        # CPU对比测试
        x_cpu = x.cpu()
        y_cpu = y.cpu()
        start_time = time.time()
        z_cpu = torch.matmul(x_cpu, y_cpu)
        cpu_time = time.time() - start_time
        
        print(f"CPU运算时间: {cpu_time:.4f}秒")
        print(f"GPU加速比: {cpu_time/gpu_time:.1f}x")
        
        return True
        
    except Exception as e:
        print(f"❌ GPU张量运算失败: {e}")
        return False

def test_yolo_gpu_training():
    """测试YOLO模型GPU训练"""
    print("\n" + "=" * 60)
    print("YOLO GPU训练测试")
    print("=" * 60)
    
    try:
        # 加载预训练模型
        model = YOLO('yolo11n.pt')  # 使用最新的YOLOv11 nano模型
        print("✅ YOLO模型加载成功")
        
        # 检查设备
        device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
        print(f"使用设备: {device}")
        
        # 简单的训练测试（仅1个epoch，使用内置数据集）
        print("开始训练测试（1个epoch，coco8数据集）...")
        
        # 清理GPU缓存
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        
        results = model.train(
            data='coco8.yaml',  # 使用小型测试数据集
            epochs=1,           # 只训练1个epoch用于测试
            batch=4,            # 小批次大小
            imgsz=320,          # 较小的图像尺寸
            device=device,
            verbose=True,
            save=False,         # 不保存模型
            plots=False         # 不生成图表
        )
        
        print("✅ YOLO GPU训练测试通过")
        print(f"训练结果: {results}")
        return True
        
    except Exception as e:
        print(f"❌ YOLO训练测试失败: {e}")
        print("可能的解决方案:")
        print("1. 检查GPU内存是否充足")
        print("2. 尝试减小batch_size")
        print("3. 检查CUDA驱动版本")
        return False

def test_memory_management():
    """测试GPU内存管理"""
    print("\n" + "=" * 60)
    print("GPU内存管理测试")
    print("=" * 60)
    
    if not torch.cuda.is_available():
        print("❌ CUDA不可用，跳过内存测试")
        return False
    
    try:
        # 获取GPU属性
        props = torch.cuda.get_device_properties(0)
        total_memory = props.total_memory / 1024**3
        
        print(f"GPU总内存: {total_memory:.1f}GB")
        
        # 清理缓存
        torch.cuda.empty_cache()
        
        # 分配大张量测试
        tensor_size = min(1000, int(total_memory * 200))  # 根据内存调整大小
        x = torch.randn(tensor_size, tensor_size, device='cuda:0')
        
        allocated = torch.cuda.memory_allocated() / 1024**3
        reserved = torch.cuda.memory_reserved() / 1024**3
        
        print(f"已分配内存: {allocated:.2f}GB")
        print(f"保留内存: {reserved:.2f}GB")
        print(f"内存使用率: {allocated/total_memory*100:.1f}%")
        
        # 释放内存
        del x
        torch.cuda.empty_cache()
        
        print("✅ GPU内存管理测试通过")
        return True
        
    except Exception as e:
        print(f"❌ GPU内存测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("开始GPU训练环境验证...")
    
    # 基础环境检查
    gpu_available = check_gpu_environment()
    
    if not gpu_available:
        print("\n❌ GPU环境检查失败，请检查:")
        print("1. NVIDIA驱动程序是否正确安装")
        print("2. CUDA版本是否兼容")
        print("3. PyTorch CUDA版本是否正确")
        return False
    
    # 张量运算测试
    tensor_test = test_simple_tensor_operations()
    
    # 内存管理测试
    memory_test = test_memory_management()
    
    # YOLO训练测试
    yolo_test = test_yolo_gpu_training()
    
    # 汇总结果
    print("\n" + "=" * 60)
    print("测试结果汇总")
    print("=" * 60)
    print(f"GPU环境检查: {'✅ 通过' if gpu_available else '❌ 失败'}")
    print(f"张量运算测试: {'✅ 通过' if tensor_test else '❌ 失败'}")
    print(f"内存管理测试: {'✅ 通过' if memory_test else '❌ 失败'}")
    print(f"YOLO训练测试: {'✅ 通过' if yolo_test else '❌ 失败'}")
    
    all_passed = all([gpu_available, tensor_test, memory_test, yolo_test])
    
    if all_passed:
        print("\n🎉 所有测试通过！GPU训练环境配置成功！")
        print("\n现在您可以:")
        print("1. 使用GPU进行YOLO模型训练")
        print("2. 享受GPU加速的推理速度")
        print("3. 处理更大的数据集和模型")
    else:
        print("\n❌ 部分测试失败，请检查相关配置")
    
    return all_passed

if __name__ == "__main__":
    main()
