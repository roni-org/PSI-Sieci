# client in C
# FROM gcc:4.9
# COPY . /Sockets
# WORKDIR /Sockets/
# RUN gcc -o sock_client1 sock_client1.c
# ENTRYPOINT  ["./sock_client1"]


# client in Python
FROM python:3
ADD tcp_client.py /
ENTRYPOINT [ "python", "./tcp_client.py" ]
