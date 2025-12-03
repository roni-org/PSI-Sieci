FROM gcc:latest

WORKDIR /app
COPY client.c /app

RUN gcc client.c -o client -std=c99 -Wall -Wextra

CMD ["./client"]
