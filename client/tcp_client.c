#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include "tcp_client.h"

void tcp_client_init(TCPClient *client, const char *server_ip, int server_port) 
{
    strcpy(client->server_ip, server_ip);
    client->server_port = server_port;
    
    client->sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if (client->sockfd == -1) 
    {
        perror("socket");
        exit(1);
    }

    struct sockaddr_in server_addr;
    memset(&server_addr, 0, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(client->server_port);
    if (inet_pton(AF_INET, client->server_ip, &server_addr.sin_addr) <= 0) 
    {
        perror("inet_pton");
        exit(1);
    }

    if (connect(client->sockfd, (struct sockaddr *)&server_addr, sizeof(server_addr)) == -1) 
    {
        perror("connect");
        exit(1);
    }
}

void tcp_client_send_data(TCPClient *client, const char *data) 
{
    if (send(client->sockfd, data, strlen(data), 0) == -1) 
    {
        perror("send");
    }
}

void tcp_client_close(TCPClient *client) 
{
    close(client->sockfd);
}
