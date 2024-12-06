const { Storage } = require('@google-cloud/storage');
const path = require('path');

const storage = new Storage({
    projectId: process.env.GCP_PROJECT_ID,
    keyFilename: path.join(__dirname, '../../keyfile.json'), 
});

const bucketName = process.env.CLOUD_STORAGE_BUCKET;

async function uploadImageToCloudStorage(file) {
    const bucket = storage.bucket(bucketName);
    const blob = bucket.file(file.originalname);
    const blobStream = blob.createWriteStream();

    return new Promise((resolve, reject) => {
        blobStream.on('error', (err) => reject(err));
        blobStream.on('finish', () => {
            const publicUrl = `https://storage.googleapis.com/${bucket.name}/${blob.name}`;
            resolve(publicUrl);
        });
        blobStream.end(file.buffer);
    });
}

module.exports = { uploadImageToCloudStorage };
