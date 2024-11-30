FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY . /app

COPY ./model /app/model

EXPOSE 8080

CMD ["python", "app.py"]