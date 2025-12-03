#define _POSIX_C_SOURCE 200112L

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <unistd.h>
#include <sys/select.h>
#include <netdb.h>
#include <netinet/in.h>

#define CHUNK_SIZE 100

int main(int argc, char *argv[]) {
    if(argc != 4) {
        printf("Usage: %s filename server_name server_port\n", argv[0]);
        return 1;
    }

    char *filename = argv[1];
    char *server_name = argv[2];
    char *port_str = argv[3];
    int port = atoi(port_str);

    int sock = socket(AF_INET, SOCK_DGRAM, 0);
    if(sock < 0) { perror("socket"); return 1; }

    struct addrinfo hints, *res;
    memset(&hints, 0, sizeof(hints));
    hints.ai_family = AF_INET;
    hints.ai_socktype = SOCK_DGRAM;

    int err = getaddrinfo(server_name, port_str, &hints, &res);
    if(err) { fprintf(stderr, "getaddrinfo: %s\n", gai_strerror(err)); return 1; }

    struct sockaddr_in servaddr = *((struct sockaddr_in*)res->ai_addr);
    socklen_t servlen = sizeof(servaddr);

    FILE *f = fopen(filename, "rb");
    if(!f) { perror("fopen"); return 1; }

    unsigned int seq = 0;
    char buffer[CHUNK_SIZE];
    size_t n;

    while((n = fread(buffer, 1, CHUNK_SIZE, f)) > 0) {
        char packet[6 + CHUNK_SIZE];
        *((unsigned int*)packet) = htonl(seq);
        *((unsigned short*)(packet+4)) = htons(n);
        memcpy(packet+6, buffer, n);

        int attempts = 0;
        while(attempts < 10) {
            ssize_t sent = sendto(sock, packet, 6 + n, 0,
                                  (struct sockaddr*)&servaddr, servlen);
            if(sent != 6 + n) {
                perror("sendto");
                attempts++;
                continue;
            }

            fd_set fds;
            struct timeval tv = {3,0};
            FD_ZERO(&fds);
            FD_SET(sock, &fds);

            int r = select(sock+1, &fds, NULL, NULL, &tv);
            if(r > 0) {
                unsigned int ack_seq;
                struct sockaddr_in from;
                socklen_t fromlen = sizeof(from);
                ssize_t rbytes = recvfrom(sock, &ack_seq, sizeof(ack_seq), 0,
                                          (struct sockaddr*)&from, &fromlen);
                if(rbytes == sizeof(ack_seq)) {
                    ack_seq = ntohl(ack_seq);
                    if(ack_seq == seq) break;
                }
            }

            attempts++;
            if(attempts == 10) {
                printf("Failed to send seq %u\n", seq);
                fclose(f);
                close(sock);
                return 1;
            }
        }

        seq++;
    }

    fclose(f);
    close(sock);
    freeaddrinfo(res);

    printf("File sent successfully!\n");
    return 0;
}
