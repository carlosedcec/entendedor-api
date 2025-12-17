FROM python:3.12-slim

WORKDIR /app

COPY ./src /app

RUN pip install --no-cache-dir -r /app/requirements.txt

RUN mkdir -p /app/data

VOLUME /app/data

EXPOSE 5000

CMD ["python", "/app/app.py"]