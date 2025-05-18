import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix

def plot_label_heatmap(y_true, y_pred, output_path="label_heatmap.png"):
    """
    生成预测标签热力图
    参数:
        y_true: 真实标签列表
        y_pred: 预测标签列表
        output_path: 输出图片路径
    """
    labels = ['sit', 'stand', 'run', 'walk', 'jump', 'wave']
    
    # 计算混淆矩阵
    cm = confusion_matrix(y_true, y_pred, labels=labels)
    
    # 创建热力图
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=labels, 
                yticklabels=labels,
                cbar_kws={'label': 'Count'})
    
    # 设置图表属性
    plt.title('Predicted vs Ground Truth Labels')
    plt.xlabel('Predicted Labels')
    plt.ylabel('Ground Truth Labels')
    plt.xticks(rotation=45)
    plt.yticks(rotation=0)
    plt.tight_layout()
    
    # 保存图表
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"标签热力图已保存到: {output_path}")

if __name__ == "__main__":
    # 示例数据
    y_true = ['sit', 'stand', 'run', 'walk', 'jump', 'wave',
              'sit', 'stand', 'sit', 'walk', 'jump', 'stand']
    y_pred = ['sit', 'stand', 'run', 'walk', 'jump', 'wave',
              'stand', 'stand', 'sit', 'walk', 'jump', 'stand']
    
    # 生成热力图
    plot_label_heatmap(y_true, y_pred)