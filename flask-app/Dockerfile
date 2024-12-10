FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app
COPY . .

# Set environment variable for Cloud Run to listen on port 8080
ENV PORT 8080

# Expose port 8080
EXPOSE 8080

# Run the Flask app
CMD ["python", "app.py"]
