# Gunakan image dasar untuk Node.js
FROM node:16

# Set direktori kerja dalam container
WORKDIR /usr/src/app

# Salin package.json dan package-lock.json ke dalam container
COPY package*.json ./

# Install dependencies yang dibutuhkan
RUN npm install

# Salin seluruh kode aplikasi ke dalam container
COPY . .

# Expose port yang digunakan oleh aplikasi
EXPOSE 8080

# Jalankan server menggunakan file server.js
CMD ["node", "server.js"]
