FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p instance

# Railway 会使用 PORT 环境变量，默认 5000
# Gunicorn 会监听 $PORT 端口
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:$PORT --timeout 30 --workers 2 run:app"]
