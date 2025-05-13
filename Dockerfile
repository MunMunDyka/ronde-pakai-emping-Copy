# Gunakan base image Python resmi yang ringan
FROM python:3.10-slim

# Set environment variable untuk menghindari masalah locale dan TTS
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    TZ=Asia/Jakarta

# Install dependencies sistem yang dibutuhkan
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Salin semua file ke container
COPY . .

# Install pip dependencies
RUN python -m pip install --upgrade pip && \
    python -m pip install --no-cache-dir -r requirements.txt

# Buat folder static (untuk simpan hasil TTS)
RUN mkdir -p /app/static

# Ekspose port FastAPI
EXPOSE 5000

# Jalankan aplikasi dengan uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000"]
