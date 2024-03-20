#ifndef TCP_CLIENT_H
#define TCP_CLIENT_H

typedef struct 
{
    int sockfd;
    char server_ip[16];
    int server_port;
} TCPClient;

void tcp_client_init(TCPClient *client, const char *server_ip, int server_port);
void tcp_client_send_data(TCPClient *client, const char *data);
void tcp_client_close(TCPClient *client);

#endif