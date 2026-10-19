FROM python:3.12-slim

# Ishchi katalog
WORKDIR /app

# Tizim kutubxonalari
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Talablarni o'rnatish
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Loyiha kodlarini nusxalash
COPY . .

# Botni ishga tushirish
CMD ["python", "main.py"]
