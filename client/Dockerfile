# client in C
# FROM gcc:4.9
# COPY . /Sockets
# WORKDIR /Sockets/
# RUN gcc -o sock_client1 sock_client1.c
# ENTRYPOINT  ["./sock_client1"]


# client in Python
FROM python:3
COPY zad1_1_client.py /
RUN pip install --no-cache-dir matplotlib
ENTRYPOINT [ "python", "./zad1_1_client.py" ]
