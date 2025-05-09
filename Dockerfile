# Gunakan image dasar Python versi 3.11.9
FROM python:3.11.9-slim
# Instal dependensi sistem yang diperlukan
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    libpq-dev \
    gcc \
    wget \
    unzip \
    && rm -rf /var/lib/apt/lists/*
# Atur direktori kerja di dalam container
WORKDIR /app
# Salin file requirements.txt ke dalam direktori kerja di dalam container
RUN pip install --upgrade pip setuptools wheel
COPY requirements.txt .
# Instal semua dependensi yang tercantum di requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
# Salin semua file kode Anda ke dalam container
COPY . .
# Buat shell script untuk menjalankan kedua file Python
RUN echo '#!/bin/bash\npython health_check.py & python chat_id.py' > start.sh
RUN chmod +x start.sh
EXPOSE 8000
# Gunakan shell script sebagai entrypoint
CMD ["./start.sh"]