/* (c) Grzegorz Blinowski 2000-2023 [TIN / PSI] */
#include <arpa/inet.h>
#include <netdb.h>
#include <netinet/in.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h>

#define TRUE 1
#define BSIZE 1024

#define bailout(s) {perror(s); exit(1); }
#define notDone() TRUE


int  main(int argc, char **argv)
{
    int sock, length, ListenQueueSize=5;
    struct sockaddr_in6 server;
    int msgsock;
    char buf[BSIZE];
    int rval;

    sock = socket(AF_INET6, SOCK_STREAM, 0);
    if (sock<0)  bailout("opening stream socket");

/* dowiaz adres IPv6 do gniazda */
    server.sin6_family = AF_INET6;
    server.sin6_addr = in6addr_any;
    server.sin6_port = 0;
    if (bind(sock, (struct sockaddr *) &server, sizeof server) == -1) 
        bailout("binding stream socket");

    /* wydrukuj na konsoli przydzielony port */
    length = sizeof(server);
    if (getsockname(sock,(struct sockaddr *) &server,&length) == -1) 
        bailout("getting socket name");
    printf("Socket port #%d\n", ntohs(server.sin6_port));

    /* zacznij przyjmowaæ polaczenia... */
    listen(sock, ListenQueueSize);
    
    do {
        msgsock = accept(sock,(struct sockaddr *) 0,(int *) 0);
        if (msgsock == -1 ) {
             bailout("accept failed");
	  }
        else do {
             memset(buf, 0, sizeof buf);
             if ((rval = read(msgsock,buf, BSIZE)) == -1)
                 perror("reading stream message");
             if (rval == 0)
                 printf("%s: Ending connection\n", argv[0]);
             else
                 printf("%s: -->%s\n", argv[0], buf);
        } while (rval != 0);
        close(msgsock);
        fflush( stdout );
    } while(notDone());
    /*
     * gniazdo sock nie zostanie nigdy zamkniete jawnie,
     * jednak wszystkie deskryptory zostana zamkniete gdy proces 
     * zostanie zakonczony (np w wyniku wystapienia sygnalu) 
     */

     exit(0);
}
