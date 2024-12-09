# Menggunakan image dasar dari Node.js
FROM node:16

# Menentukan direktori kerja dalam container
WORKDIR /app

# Menyalin file package.json dan package-lock.json terlebih dahulu untuk menginstall dependensi
COPY package*.json ./

# Menginstall dependensi aplikasi
RUN npm install

# Menyalin semua file sumber dari aplikasi ke dalam container
COPY . .

# Mengekspos port aplikasi (sesuaikan dengan port yang digunakan oleh aplikasi Anda)
EXPOSE 8001

# Perintah untuk menjalankan aplikasi Node.js
CMD ["node", "server.js"]
