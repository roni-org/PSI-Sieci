FROM python:3.11-slim
WORKDIR /app
COPY crypto_utils.py .
COPY server/server.py .
ENTRYPOINT ["python", "server.py"]
CMD ["4444", "10"]  # port i max_clients
