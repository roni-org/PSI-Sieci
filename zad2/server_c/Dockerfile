FROM gcc:latest

WORKDIR /app
COPY server.c /app

RUN gcc server.c -o server

CMD ["./server"]
