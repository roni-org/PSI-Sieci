FROM python:3.11-slim
WORKDIR /app
COPY crypto_utils.py .
COPY client/client.py .
ENTRYPOINT ["python", "client.py"]
