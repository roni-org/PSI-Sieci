#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <arpa/inet.h>
#include <unistd.h>

#define PORT 8000
#define BUFFER_SIZE 65535
#define bailout(s) {perror(s); exit(1); }

int main(int argc, char **argv) {
    int sock;
    struct sockaddr_in server_addr, client_addr;
    socklen_t client_len = sizeof(client_addr);
    char buffer[BUFFER_SIZE];
    int n;

    int port = PORT;
    if (argc > 1) {
        port = atoi(argv[1]);
    }

    sock = socket(AF_INET, SOCK_DGRAM, 0);
    if (sock < 0) {
        bailout("socket creation failed");
    }

    memset(&server_addr, 0, sizeof(server_addr));

    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = INADDR_ANY;
    server_addr.sin_port = htons(port);

    if (bind(sock, (const struct sockaddr *)&server_addr, sizeof(server_addr)) < 0) {
        bailout("bind failed");
    }

    printf("UDP server listening on port %d\n", port);

    while (1) {
        client_len = sizeof(client_addr);
        n = recvfrom(sock, buffer, BUFFER_SIZE, 0, (struct sockaddr *)&client_addr, &client_len);
        if (n < 0) {
            perror("recvfrom failed");
            continue;
        }

        printf("Received %d bytes\n", n);

        // Client answer
        const char *ack = "ACK";
        if (sendto(sock, ack, strlen(ack), 0, (struct sockaddr*)&client_addr, client_len) < 0) {
            bailout("sendto failed");
        }
    }

    close(sock);
    return 0;
}
