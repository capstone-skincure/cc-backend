FROM python:3.9-slim

WORKDIR /app

# Salin requirements.txt ke dalam image
COPY requirements.txt ./

# Install dependensi
RUN pip install -r requirements.txt

# Salin semua file dari folder lokal ke dalam image
COPY . .

# Expose port untuk aplikasi Flask
EXPOSE 8000

# Jalankan aplikasi Flask
CMD ["python", "app.py"]