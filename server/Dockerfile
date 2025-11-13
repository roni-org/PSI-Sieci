# server in C
FROM gcc:4.9
COPY . /Server
WORKDIR /Server/
RUN gcc -o zad1_1_server zad1_1_server.c
ENTRYPOINT ["./zad1_1_server"]

# server in Python
# FROM python:3
# ADD tcp_server_to.py /
# ENTRYPOINT [ "python", "./tcp_server_to.py" ]