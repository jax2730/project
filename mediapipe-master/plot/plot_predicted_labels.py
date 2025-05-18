import matplotlib.pyplot as plt
import numpy as np
import os
from collections import Counter

def plot_label_distribution(labels, output_path="label_distribution.png"):
    """
    生成预测标签分布图
    参数:
        labels: 包含所有预测标签的列表
        output_path: 输出图片路径
    """
    # 统计各标签出现次数
    label_counts = Counter(labels)
    sorted_labels = ['sit', 'stand', 'run', 'walk', 'jump', 'wave']
    
    # 准备数据
    counts = [label_counts.get(label, 0) for label in sorted_labels]
    
    # 创建图表
    plt.figure(figsize=(10, 6))
    bars = plt.bar(sorted_labels, counts, color='skyblue')
    
    # 添加数值标签
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                 f'{int(height)}', ha='center', va='bottom')
    
    # 设置图表属性
    plt.title('Predicted Labels Distribution')
    plt.xlabel('Action Labels')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # 保存图表
    plt.savefig(output_path)
    plt.close()
    print(f"标签分布图已保存到: {output_path}")

if __name__ == "__main__":
    # 示例数据
    sample_labels = ['sit', 'stand', 'run', 'walk', 'jump', 'wave',
                    'sit', 'stand', 'sit', 'walk', 'jump', 'stand']
    
    # 生成图表
    plot_label_distribution(sample_labels)