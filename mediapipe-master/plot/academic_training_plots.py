import matplotlib.pyplot as plt
import numpy as np
import os
import seaborn as sns
from datetime import datetime
from sklearn.metrics import confusion_matrix, roc_curve, auc

def plot_academic_training_curves(history, output_dir="academic_plots"):
    """
    生成学术标准的训练可视化图表
    参数:
        history: 包含训练历史的字典
        output_dir: 输出目录路径
    """
    # 设置学术图表样式
    sns.set_style("whitegrid")
    plt.rcParams.update({
        'font.size': 12,
        'font.family': 'Times New Roman',
        'figure.autolayout': True
    })
    
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # 1. 训练指标曲线
    plt.figure(figsize=(10, 4))
    plt.subplot(1, 2, 1)
    plt.plot(history['epoch'], history['loss'], 'b-', label='Training', linewidth=2)
    plt.plot(history['epoch'], history['val_loss'], 'r-', label='Validation', linewidth=2)
    plt.title('Loss Curve', pad=15)
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()
    
    plt.subplot(1, 2, 2)
    plt.plot(history['epoch'], history['accuracy'], 'b-', label='Training', linewidth=2)
    plt.plot(history['epoch'], history['val_accuracy'], 'r-', label='Validation', linewidth=2)
    plt.title('Accuracy Curve', pad=15)
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy')
    plt.ylim(0, 1)
    plt.legend()
    
    plt.savefig(f"{output_dir}/training_curves_{timestamp}.png", dpi=300, bbox_inches='tight')
    plt.close()

    # 2. 混淆矩阵热力图
    if 'y_true' in history and 'y_pred' in history:
        plt.figure(figsize=(8, 6))
        cm = confusion_matrix(history['y_true'], history['y_pred'])
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                   cbar_kws={'label': 'Count'})
        plt.title('Confusion Matrix', pad=15)
        plt.xlabel('Predicted Labels')
        plt.ylabel('True Labels')
        plt.savefig(f"{output_dir}/confusion_matrix_{timestamp}.png", dpi=300)
        plt.close()

if __name__ == "__main__":
    # 生成更真实的训练曲线数据
    epochs = np.arange(1, 21)
    
    # 训练Loss - 添加随机波动和更真实的下降曲线
    train_loss = 1.0 * np.exp(-0.15 * epochs) 
    train_loss += np.random.normal(0, 0.02, len(epochs))
    
    # 验证Loss - 比训练Loss稍高且有波动
    val_loss = 1.1 * np.exp(-0.12 * epochs)
    val_loss += np.random.normal(0, 0.03, len(epochs))
    
    # 训练Accuracy - S形增长曲线
    train_acc = 0.5 + 0.5 * (1 / (1 + np.exp(-0.3*(epochs-10))))
    train_acc += np.random.normal(0, 0.01, len(epochs))
    
    # 验证Accuracy - 比训练稍低
    val_acc = 0.45 + 0.45 * (1 / (1 + np.exp(-0.25*(epochs-10))))
    val_acc += np.random.normal(0, 0.015, len(epochs))
    
    history = {
        'epoch': epochs,
        'loss': train_loss,
        'val_loss': val_loss,
        'accuracy': train_acc,
        'val_accuracy': val_acc,
        'y_true': np.random.randint(0, 6, 100),
        'y_pred': np.random.randint(0, 6, 100)
    }
    
    plot_academic_training_curves(history)