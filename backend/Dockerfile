# 使用 Python 3.13 作为基础镜像
# 建议使用 slim 版本以减小镜像体积，bookworm 是 Debian 12 代号，包含较新系统库
FROM python:3.13-slim-bookworm

# 设置工作目录
WORKDIR /app

# 设置环境变量
# PYTHONDONTWRITEBYTECODE=1: 防止 Python 写入 .pyc 文件
# PYTHONUNBUFFERED=1: 确保日志直接输出到控制台，不被缓存
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    TZ=Asia/Shanghai

# 安装系统依赖
# ChromaDB 可能需要构建工具 (build-essential)
# curl 用于健康检查
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirement.txt .

# 安装 Python 依赖
# --no-cache-dir 减小镜像体积
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirement.txt

# 复制应用代码
COPY . .

# 设置 PYTHONPATH 以便正确导入模块
ENV PYTHONPATH=/app

# 暴露端口
EXPOSE 8000

# 启动命令
# 使用 uvicorn 启动 FastAPI 应用
# main:app 指向 main.py 中的 app 对象
# --host 0.0.0.0 允许外部访问
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
