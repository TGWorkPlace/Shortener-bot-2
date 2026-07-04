FROM python:3.11-slim

# Avoid .pyc files and enable unbuffered stdout (useful for Koyeb logs)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Koyeb expects the app to listen on this port (matches config.PORT default)
ENV PORT=8080
EXPOSE 8080

CMD ["python", "main.py"]
