/* (c) Grzegorz Blinowski 2000-2022 [TIN / PSI] */
#include <arpa/inet.h>
#include <netdb.h>
#include <netinet/in.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h>

#define DATA "Half a league, half a league . . ."
#define USE_RESOLVER
#define _USE_ARGS
#define DEFAULT_PORT 8001
// #define DEFAULT_SRV_IP "::1"
#define DEFAULT_SRV_IP "fc00::2"

#define BSIZE 1024

#define bailout(s) {perror(s); exit(1); }
int main(int argc, char *argv[])
{
    int sock = 0;
    struct sockaddr_in6 server;
    char buf[BSIZE];
    struct hostent *hp;

    printf("Starting...\n");

    /* Create socket. */
    sock = socket( AF_INET6, SOCK_STREAM, 0 );
    if (sock == -1) bailout("creating socket"); 
    
    server.sin6_family = AF_INET6;

#ifdef USE_RESOLVER
    hp = gethostbyname2(argv[1], AF_INET6 );
/* hostbyname() returns a struct with resolved host address  */
    if (hp == (struct hostent *) 0) {
        fprintf(stderr, "%s: unknown host\n", argv[1]);
        exit(2);
    }
    memcpy((char *) &server.sin6_addr, (char *) hp->h_addr, hp->h_length);
    server.sin6_port = htons(atoi( argv[2]));
#elif defined(USE_ARGS)
    inet_pton(AF_INET6, argv[1], &server.sin6_addr );
    server.sin6_port = htons(atoi( argv[2]));
#else
    inet_pton( AF_INET6, DEFAULT_SRV_IP, &server.sin6_addr );
    server.sin6_port = htons(DEFAULT_PORT);
#endif

    printf("Connecting...\n");
    if (connect(sock, (struct sockaddr *) &server, sizeof server) == -1)
      bailout("connecting stream socket");
    printf("Connected.\n");

    if (write( sock, DATA, sizeof DATA ) == -1) 
        bailout( "writing on stream socket");

    close(sock);
    exit(0);
}

