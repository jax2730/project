import matplotlib.pyplot as plt
import numpy as np
import os
from datetime import datetime

def plot_training_metrics(history, output_dir="training_plots"):
    """
    绘制并保存训练过程中的各项指标图表
    参数:
        history: 包含训练历史的字典
        output_dir: 输出目录路径
    """
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    # 获取当前时间戳用于文件名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # 1. 绘制训练和验证的损失曲线
    plt.figure(figsize=(10, 6))
    plt.plot(history['loss'], label='Training Loss')
    plt.plot(history['val_loss'], label='Validation Loss')
    plt.title('Training and Validation Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(output_dir, f'loss_{timestamp}.png'))
    plt.close()
    
    # 2. 绘制训练和验证的准确率曲线
    if 'accuracy' in history:
        plt.figure(figsize=(10, 6))
        plt.plot(history['accuracy'], label='Training Accuracy')
        plt.plot(history['val_accuracy'], label='Validation Accuracy')
        plt.title('Training and Validation Accuracy')
        plt.xlabel('Epoch')
        plt.ylabel('Accuracy')
        plt.legend()
        plt.grid(True)
        plt.savefig(os.path.join(output_dir, f'accuracy_{timestamp}.png'))
        plt.close()
    
    # 3. 绘制学习率变化曲线
    if 'lr' in history:
        plt.figure(figsize=(10, 6))
        plt.plot(history['lr'], label='Learning Rate')
        plt.title('Learning Rate Schedule')
        plt.xlabel('Epoch')
        plt.ylabel('Learning Rate')
        plt.legend()
        plt.grid(True)
        plt.savefig(os.path.join(output_dir, f'learning_rate_{timestamp}.png'))
        plt.close()
    
    # 4. 绘制混淆矩阵（如果有预测结果）
    if 'y_true' in history and 'y_pred' in history:
        from sklearn.metrics import confusion_matrix
        import seaborn as sns
        
        cm = confusion_matrix(history['y_true'], history['y_pred'])
        plt.figure(figsize=(10, 8))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
        plt.title('Confusion Matrix')
        plt.xlabel('Predicted Label')
        plt.ylabel('True Label')
        plt.savefig(os.path.join(output_dir, f'confusion_matrix_{timestamp}.png'))
        plt.close()
    
    # 5. 绘制预测样本示例（如果有图像数据）
    if 'sample_images' in history and 'sample_preds' in history:
        plt.figure(figsize=(15, 10))
        for i, (img, pred, true) in enumerate(zip(history['sample_images'], 
                                               history['sample_preds'], 
                                               history['sample_true'])):
            plt.subplot(3, 3, i+1)
            plt.imshow(img)
            plt.title(f"Pred: {pred}\nTrue: {true}")
            plt.axis('off')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, f'predictions_{timestamp}.png'))
        plt.close()
    
    # 6. 绘制预测置信度分布
    if 'pred_probs' in history:
        plt.figure(figsize=(10, 6))
        plt.hist(history['pred_probs'], bins=20, alpha=0.7)
        plt.title('Prediction Confidence Distribution')
        plt.xlabel('Confidence')
        plt.ylabel('Count')
        plt.savefig(os.path.join(output_dir, f'confidence_dist_{timestamp}.png'))
        plt.close()

    # 7. 绘制ROC曲线（分类任务）
    if 'y_true' in history and 'y_probs' in history:
        from sklearn.metrics import roc_curve, auc
        fpr, tpr, _ = roc_curve(history['y_true'], history['y_probs'])
        roc_auc = auc(fpr, tpr)
        
        plt.figure(figsize=(10, 6))
        plt.plot(fpr, tpr, label=f'ROC curve (area = {roc_auc:.2f})')
        plt.plot([0, 1], [0, 1], 'k--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('Receiver Operating Characteristic')
        plt.legend(loc="lower right")
        plt.savefig(os.path.join(output_dir, f'roc_curve_{timestamp}.png'))
        plt.close()

if __name__ == "__main__":
    # 扩展示例数据
    history = {
        'loss': np.random.rand(10).tolist(),
        'val_loss': np.random.rand(10).tolist(),
        'accuracy': np.random.rand(10).tolist(),
        'val_accuracy': np.random.rand(10).tolist(),
        'lr': np.linspace(0.001, 0.0001, 10).tolist(),
        'sample_images': [np.random.rand(32,32,3) for _ in range(9)],
        'sample_preds': ['sit', 'hand up', 'sit', 'hand up', 'sit', 'hand up', 'sit', 'hand up', 'sit'],
        'sample_true': ['sit', 'sit', 'hand up', 'hand up', 'sit', 'hand up', 'sit', 'hand up', 'sit'],
        'pred_probs': np.random.rand(100),
        'y_true': np.random.randint(0, 2, 100),
        'y_probs': np.random.rand(100)
    }
    plot_training_metrics(history)