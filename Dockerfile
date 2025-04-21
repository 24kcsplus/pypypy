FROM python:3.13.0a1-slim
LABEL authors="24k"

WORKDIR /app
COPY . .

# 安装系统依赖和 Python 库
RUN apt-get update && \
    apt-get install -y gcc python3-dev && \
    pip install --no-cache-dir -r requirements.txt

# 复制并授权 entrypoint 脚本
#COPY entrypoint.sh /app/entrypoint.sh
#RUN chmod +x /app/entrypoint.sh

EXPOSE 5000

# 容器启动时执行 entrypoint.sh
#ENTRYPOINT ["/app/entrypoint.sh"]