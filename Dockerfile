FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p instance

EXPOSE 5000

# Railway 会自动设置 PORT 环境变量
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--timeout", "30", "--workers", "2", "run:app"]
