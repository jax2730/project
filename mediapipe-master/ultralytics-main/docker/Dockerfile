# Ultralytics 🚀 AGPL-3.0 License - https://ultralytics.com/license

# Builds ultralytics/ultralytics:latest image on DockerHub https://hub.docker.com/r/ultralytics/ultralytics
# Image is CUDA-optimized for YOLO11 single/multi-GPU training and inference

# Start FROM PyTorch image https://hub.docker.com/r/pytorch/pytorch or nvcr.io/nvidia/pytorch:25.02-py3
FROM ac2-registry.cn-hangzhou.cr.aliyuncs.com/ac2/cuda:12.6.0-runtime-cudnn9-ubuntu22.04

# Set up Alibaba Cloud mirrors for apt
RUN sed -i 's/archive.ubuntu.com/mirrors.aliyun.com/g' /etc/apt/sources.list && \
    sed -i 's/security.ubuntu.com/mirrors.aliyun.com/g' /etc/apt/sources.list

# Set environment variables
# Avoid DDP error "MKL_THREADING_LAYER=INTEL is incompatible with libgomp.so.1 library" https://github.com/pytorch/pytorch/issues/37377
# Suppress TensorFlow cuDNN, cuBLAS, and cuFFT Registration Warnings
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_BREAK_SYSTEM_PACKAGES=1 \
    MKL_THREADING_LAYER=GNU \
    OMP_NUM_THREADS=1 \
    TF_CPP_MIN_LOG_LEVEL=3

# Copy fonts from local assets directory
COPY assets/Arial.ttf /root/.config/Ultralytics/
COPY assets/Arial.Unicode.ttf /root/.config/Ultralytics/

# Install linux packages
# gnupg required for Edge TPU install
# libsm6 required by libqxcb to create QT-based windows for visualization; set 'QT_DEBUG_PLUGINS=1' to test in docker
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc git zip unzip wget curl htop libgl1 libglib2.0-0 libpython3-dev gnupg libsm6 \
    && rm -rf /var/lib/apt/lists/*

# Security updates
# https://security.snyk.io/vuln/SNYK-UBUNTU1804-OPENSSL-3314796
RUN apt upgrade --no-install-recommends -y openssl tar

# Create working directory
WORKDIR /ultralytics

# Copy contents and configure git
COPY . .
RUN [ -f .git/config ] && sed -i '/^\[http "https:\/\/github\.com\/"\]/,+1d' .git/config || echo ".git/config not found, skipping modification"
COPY yolo11n.pt .

# Install pip packages
RUN pip install uv --index-url https://mirrors.aliyun.com/pypi/simple/
RUN uv pip install --system --index-url https://mirrors.aliyun.com/pypi/simple/ --extra-index-url https://pypi.nvidia.com/ -e ".[export]" albumentations pycocotools "onnxruntime-gpu" tensorrt wandb

# Run exports to AutoInstall packages
RUN yolo export model=tmp/yolo11n.pt format=edgetpu imgsz=32 || echo "EdgeTPU export failed, continuing..."
RUN yolo export model=tmp/yolo11n.pt format=ncnn imgsz=32 || echo "NCNN export failed, continuing..."
RUN uv pip install --system --index-url https://mirrors.aliyun.com/pypi/simple/ paddlepaddle x2paddle

# Remove extra build files
RUN rm -rf tmp /root/.config/Ultralytics/persistent_cache.json

# Usage Examples -------------------------------------------------------------------------------------------------------

# Build and Push
# t=ultralytics/ultralytics:latest && sudo docker build -f docker/Dockerfile -t $t . && sudo docker push $t

# Pull and Run with access to all GPUs
# t=ultralytics/ultralytics:latest && sudo docker pull $t && sudo docker run -it --ipc=host --gpus all $t

# Pull and Run with access to GPUs 2 and 3 (inside container CUDA devices will appear as 0 and 1)
# t=ultralytics/ultralytics:latest && sudo docker pull $t && sudo docker run -it --ipc=host --gpus '"device=2,3"' $t

# Pull and Run with local directory access
# t=ultralytics/ultralytics:latest && sudo docker pull $t && sudo docker run -it --ipc=host --gpus all -v "$(pwd)"/shared/datasets:/datasets $t

# Kill all
# sudo docker kill $(sudo docker ps -q)

# Kill all image-based
# sudo docker kill $(sudo docker ps -qa --filter ancestor=ultralytics/ultralytics:latest)

# DockerHub tag update
# t=ultralytics/ultralytics:latest tnew=ultralytics/ultralytics:v6.2 && sudo docker pull $t && sudo docker tag $t $tnew && sudo docker push $tnew

# Clean up
# sudo docker system prune -a --volumes

# Update Ubuntu drivers
# https://www.maketecheasier.com/install-nvidia-drivers-ubuntu/

# DDP test
# python -m torch.distributed.run --nproc_per_node 2 --master_port 1 train.py --epochs 3

# GCP VM from Image
# docker.io/ultralytics/ultralytics:latest
