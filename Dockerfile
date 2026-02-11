# Menggunakan base image Python yang ringan
FROM python:3.9-slim

# Mencegah Python menulis file pyc dan buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory di dalam container
WORKDIR /app

# Copy file requirements dan install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy seluruh source code ke dalam container
COPY . .

# Cloud Run akan menginject variable PORT, default 8080
ENV PORT 8080

# Command untuk menjalankan aplikasi menggunakan Gunicorn (Production Server)
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app