FROM python:3.8-slim
WORKDIR /app
COPY . /app
RUN pip install flask tensorflow
CMD ["python", "app.py"]