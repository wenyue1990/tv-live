# 飞牛电视直播 Dockerfile
# 适用于fnOS (飞牛NAS)

FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 复制应用文件
COPY . .

# 创建配置目录
RUN mkdir -p /config

# 暴露端口
EXPOSE 8080

# 设置环境变量
ENV PYTHONUNBUFFERED=1
ENV TZ=Asia/Shanghai

# 启动命令
CMD ["python", "server.py"]
