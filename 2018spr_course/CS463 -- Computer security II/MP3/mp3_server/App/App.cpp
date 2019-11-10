#include <stdio.h>
#include <iostream>
#include "Enclave_u.h"
#include "sgx_urts.h"
#include "sgx_utils/sgx_utils.h"
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <unistd.h>
#include <string.h>


#define BUFFER_SIZE 4096
#define on_error(...) { fprintf(stderr, __VA_ARGS__); fflush(stderr); exit(1); }
/* Global EID shared by multiple threads */
sgx_enclave_id_t global_eid = 0;

// OCall implementations
void ocall_print(const char* str) {
    printf("%s\n", str);
}

int main(int argc, char const *argv[]) {
    if (initialize_enclave(&global_eid, "enclave.token", "enclave.signed.so") < 0) {
        std::cout << "Fail to initialize enclave." << std::endl;
        return 1;
    }
    int ptr;
    sgx_status_t status = generate_random_number(global_eid, &ptr);
    std::cout << status << std::endl;
    if (status != SGX_SUCCESS) {
        std::cout << "noob" << std::endl;
    }
    printf("Random number: %d\n", ptr);

    // Seal the random number
    size_t sealed_size = sizeof(sgx_sealed_data_t) + sizeof(ptr);
    uint8_t* sealed_data = (uint8_t*)malloc(sealed_size);

    sgx_status_t ecall_status;
    status = seal(global_eid, &ecall_status,
            (uint8_t*)&ptr, sizeof(ptr),
            (sgx_sealed_data_t*)sealed_data, sealed_size);

    if (!is_ecall_successful(status, "Sealing failed :(", ecall_status)) {
        return 1;
    }

    int unsealed;
    status = unseal(global_eid, &ecall_status,
            (sgx_sealed_data_t*)sealed_data, sealed_size,
            (uint8_t*)&unsealed, sizeof(unsealed));

    if (!is_ecall_successful(status, "Unsealing failed :(", ecall_status)) {
        return 1;
    }

    std::cout << "Seal round trip success! Receive back " << unsealed << std::endl;

    int port = 10055;
    int server_fd, client_fd, err;
    struct sockaddr_in server, client;
    char buf[BUFFER_SIZE];

    server_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (server_fd < 0) on_error("Could not create socket\n");

    server.sin_family = AF_INET;
    server.sin_port = htons(port);
    server.sin_addr.s_addr = htonl(INADDR_ANY);

    int opt_val = 1;
    setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR, &opt_val, sizeof opt_val);

    err = bind(server_fd, (struct sockaddr *) &server, sizeof(server));
    if (err < 0) on_error("Could not bind socket\n");

    err = listen(server_fd, 128);
    if (err < 0) on_error("Could not listen on socket\n");

    printf("Server is listening on %d\n", port);

    while (1) {
      socklen_t client_len = sizeof(client);
      client_fd = accept(server_fd, (struct sockaddr *) &client, &client_len);

      if (client_fd < 0) on_error("Could not establish new connection\n");

      //while (1) {
      int read = recv(client_fd, buf, BUFFER_SIZE, 0);

      //if (read == 0) break; // done reading
      if (read < 0) on_error("Client read failed\n");
      //}

      // printf("parsing below:\n");
      int numLines = 0;
      const char *con_ch;
      for(con_ch = buf; *con_ch; ++con_ch){
            numLines += *con_ch == '\n';
      }
      // printf("%d samples in dataset\n", numLines-1);

      int rows = numLines-1, cols = 5, numFeat = 4, cnt = 0, r=0, c=0;
      double *y = (double *)malloc(rows * sizeof(double));
      double *X[rows];
      for(r=0; r < rows; r++){
           X[r] = (double *)malloc(numFeat * sizeof(double));
      }

      char * line;
      line = strtok(buf,"\n"); //remove the header
      line = strtok(NULL, ",");
      while(line != NULL){
           if(cnt%cols == 4) {
                y[cnt/cols] = atof(line);
           }else {
                X[cnt/cols][cnt%cols] = atof(line);
           }
           cnt++;
           line = strtok(NULL,",\n");
      }

      // for(int i = 0; i < rows; i++) {
      //   printf("%lf\n",y[i]);
      // }
      //
      // for(int i = 0; i < rows; i++) {
      //   for(int j = 0; j < 4; j++)
      //     printf("%.2lf\n",X[i][j]);
      // }

      for(int i = 0; i < rows; i++) {
    	   enclaveInX(global_eid, X[i], numFeat*sizeof(double));
      }

      enclaveInY(global_eid,y,rows*sizeof(double));

      double *weights = (double *)malloc(numFeat*sizeof(double));

      enclaveOut(global_eid, weights, rows*sizeof(double));

      for(int j = 0; j < 4; j++)
        printf("%.2lf\n",weights[j]);

      err = send(client_fd, weights, numFeat*sizeof(double), 0);
      if (err < 0) on_error("Client write failed\n");

    }

    return 0;

}
