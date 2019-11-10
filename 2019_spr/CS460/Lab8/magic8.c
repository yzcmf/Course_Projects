/*
 * VulClient:
 * An incrediably simple client create for the
 * cyber security lab 6.
 * It creates a connection to a server listening on TCP/80 and sends
 * a message that is passed in on command line argument to.  It waits
 * for a reply from the server and prints the reply.
 */
#include <stdlib.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <sys/select.h>
#include <netinet/in.h>
#include <stdio.h>
#include <errno.h>
#include <string.h>

int main(int argc, char *argv[])
{
	if (argc != 3)
	{
		fprintf(stderr, "USAGE: %s <serverIP> \"fortune\"\n", argv[0]);
		exit(1);
	}

	int sock = socket(PF_INET, SOCK_STREAM, 0);
	if (sock < 0)
	{
		// error
		fprintf(stderr, "Socket creation failed %d\n", errno);
		exit(1);
	}

	// Connect to the server
	struct sockaddr_in server_address;
	server_address.sin_family = AF_INET;
	server_address.sin_port = ((0xFF & 10001) << 8) |
			   ((10001 >> 8) & 0xFF);
	if (inet_aton(argv[1], &server_address.sin_addr) < 0)
	{
		// Error
		fprintf(stderr, "Inet creation failed %d\n", errno);
		exit(1);
	}
	
	if (connect(sock, (struct sockaddr*)&server_address, sizeof(server_address)) < 0)
	{
		// error
		fprintf(stderr, "Connect failed %d\n", errno);
		exit(1);
	}

	if (write(sock, argv[2], strlen(argv[2])) < 0)
	{
		// error 
		fprintf(stderr, "Write failed %d\n", errno);
		exit(1);
	}

	// Wait for the reply
	fd_set read_set;
	FD_ZERO(&read_set);
	FD_SET(sock, &read_set);
	if (select(sock+1, &read_set, NULL, NULL, NULL) <= 0)
	{
		// error
		fprintf(stderr, "Read select failed %d\n", errno);
		exit(1);
	}

	char reply[512];
	if (read(sock, reply, 512) < 0)
	{
		// error
		fprintf(stderr, "Read failed %d\n", errno);
		exit(1);
	}
	printf("The answer is %s\n", reply);
}
