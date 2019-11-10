/*
 * Magic8:
 * An incrediably simple server.
 * It listens to port 10001.  For each client connection, it reads data,
 * and randomly returns one of three reponses, like a very simplistic
 * magic eightball.  Then it goes back to listening for replies.
 */
#include <stdlib.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <sys/select.h>
#include <netinet/in.h>
#include <stdio.h>
#include <errno.h>
#include <string.h>
#include <time.h>
#include <unistd.h>

void DoServerStuff(int sock);
void DoChildStuff(int sock);

int Resp_count;
char **Responses;

void ReadResponses() {
	FILE *resp_file = fopen("response.txt", "r");
	if (!resp_file) {
		fprintf(stderr, "Failed to open response.txt\n");
		exit(1);
	}
	Resp_count = 0;
	char *buffer = NULL;
	int count= 0;
	while (getline(&buffer, &count, resp_file) > 0) {
		Resp_count++;
	}
	if (Resp_count == 0) {
		fprintf(stderr, "No responses found\n");
		exit(1);
	}

	fclose(resp_file);
	fopen("response.txt", "r");
	Responses = malloc(sizeof(char *)*Resp_count);
	memset(Responses, 0, sizeof(char*)*Resp_count);
	int i = 0;
	while (getline(&Responses[i++], &count, resp_file) >  0) {
	}
	fclose(resp_file);	
}

int main(int argc, char *argv[])
{
	struct sockaddr_in address;
	int listen_sock;

	ReadResponses();

	listen_sock = socket(PF_INET, SOCK_STREAM, 0);
	if (listen_sock < 0)
	{
		fprintf(stderr, "Failed to open listen socket %d\n", errno);
		exit(1);
	}
	int val = 1;
	setsockopt(listen_sock, SOL_SOCKET, SO_REUSEADDR, &val, sizeof(val));

	address.sin_family = AF_INET;
	address.sin_port = htons(10001);
	address.sin_addr.s_addr = INADDR_ANY;

	if (bind(listen_sock, (struct sockaddr *)&address, sizeof(address)) < 0)
	{
		// error
		fprintf(stderr, "Failed to bind listen socket %d\n", errno);
		exit(1);
	}	

	DoServerStuff(listen_sock);
}

void DoServerStuff(int listen_sock)
{
	fd_set read_set, write_set;
	int select_retval;
	struct sockaddr_in address;
	struct sockaddr_in peer_address;
	socklen_t addr_len = sizeof(address);
	int comm_sock;

	while (1)	// Loop forever
	{
		if (listen(listen_sock, 5) != 0)
		{
			// error
			fprintf(stderr, "Failed to listen on listen socket %d\n", errno);
			exit(1);
		}

		FD_ZERO(&read_set);
		FD_SET(listen_sock, &read_set);
		FD_ZERO(&write_set);

		select_retval = select(listen_sock+1, &read_set, NULL, NULL, NULL);
		if (select_retval <= 0)
		{
			// error
			fprintf(stderr, "Listen select failed %d\n", errno);
			exit(1);
		}
	
		// Got a response, go ahead and accept it
		comm_sock = accept(listen_sock, (struct sockaddr *)&peer_address, &addr_len);
		if (comm_sock < 0)
		{
			// error
			fprintf(stderr, "Accept failed %d\n", errno);
			exit(1);
		}
	
		//printf("Communicating with %s\n", inet_ntoa(peer_address.sin_addr));
	
		// Fork off logic to continue communicating with this client
		//int pid = fork();

		//if (pid == 0)
		{
			DoChildStuff(comm_sock);
		}	
	}
}

char retstr[100];	

unsigned long get_sp(void)
{
	__asm__("mov %esp, %eax");
}

unsigned long get_fp(void)
{
	__asm__("mov %ebp, %eax");
}

// Source of the buffer overflow
void LogBuffer(char *data)
{
	char log[512];
	
	memset(retstr, 0, 100);
	sprintf(retstr, "buffer addr %p\n", log);

	strcpy(log, data);
	FILE *log_file = fopen("./magic8.log", "a");
	if (log_file) {
		fprintf(log_file, "%s\n", log);
	}
	fclose(log_file);
}

void DoChildStuff(int comm_sock)
{
	char read_buffer[1024];
	fd_set read_set, write_set;
	int select_retval;

	srand(time(NULL));

	FD_ZERO(&read_set);
	FD_SET(comm_sock, &read_set);

	// See if there is data to read
	select_retval = select(comm_sock+1, &read_set, NULL, NULL, NULL);
	if (select_retval <= 0)
	{
		// error
		fprintf(stderr, "Read select failed %d\n", errno);
		exit(1);
	}

	// Read the data
	int readct = read(comm_sock, read_buffer, 1024);
	read_buffer[readct] = 0;

	LogBuffer(read_buffer);

	int rand_val = rand();

	// Return a message
	write(comm_sock, retstr, strlen(retstr)+1);
	shutdown(comm_sock, SHUT_RDWR);	
}
