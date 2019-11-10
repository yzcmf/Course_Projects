#include "Enclave_t.h"
#include <stdio.h>
#include <string.h>
#include <math.h>

double X[30][4];
double Y[30];
double weights[4];
int count = 0;

int generate_random_number() {
    ocall_print("Processing random number generation...");
    return 42;
}

void enclaveOut(double *buf, size_t len) {
    for(int i = 0; i< 4; i++)
      weights[i] = 0;

    for(int i = 0; i < 50; i++) {
      //dot product
      double result[30];
      double grad[4];
      for(int tmp = 0; tmp < 30; tmp++) {
        result[tmp] = 0;
        if (tmp < 4)
          grad[tmp] = 0;
      }

      for (int j = 0; j < 30; j++) {
        for(int k = 0; k< 4; k++) {
          result[j] += X[j][k]*weights[k];
        }
         result[j] = 1.0 / (1 + exp(-result[j]));
      }

      for(int j = 0; j < 4; j++){
        for(int k = 0 ; k < 30; k++) {
          grad[j] += X[k][j]*(result[k]-Y[k]);
        }
        grad[j] /= 90*0.01;
        weights[j] -= grad[j];
      }
    }

    memcpy(buf,weights,len);
}

void enclaveInX(double *buf, size_t len) {
    memcpy(X[count],buf,len);
    count ++;
}

void enclaveInY(double *buf, size_t len) {
    memcpy(Y,buf,len);
}
