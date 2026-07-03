FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends mpg123 && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

ENV HOST=0.0.0.0 PORT=5000
EXPOSE 5000
CMD ["python", "main.py"]
