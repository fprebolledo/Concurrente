#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "mpi.h"
#include <time.h>

int main(int argc, char *argv[])
{
  int cantidad = 0;
  float x, y, z;
  double segundos;
  int i, nodenum, id, count = 0;
  float rial_pi = 3.1416;
  float f = 0;
  clock_t tiempo_final, tiempo_inicio = clock();
  MPI_Init(&argc, &argv);                       //Se inicia MPI
  MPI_Comm_rank(MPI_COMM_WORLD, &id);           //tomo una id para el proceso
  MPI_Comm_size(MPI_COMM_WORLD, &nodenum);
  int cont_reciv[nodenum];
  int cant_reciv[nodenum];

  if (id != 0) // mientras sea cualquier proceso menos el primero..
  {
    while (fabs(f - 3.1416) > 0.00009)
    { // calculo los numeros randoms
      x = (float)random() / RAND_MAX;
      y = (float)random() / RAND_MAX;
      z = x*x + y*y;
      if (z<=1)
      {
        count++;
      }
      cantidad++;
      // calculo

      //envío al nodo 0
      
      MPI_Send(&count, 1, MPI_INT, 0, 1, MPI_COMM_WORLD);
      MPI_Send(&cantidad, 1, MPI_LONG, 0, 2, MPI_COMM_WORLD);

      // recibo del nodo 0 el f que calculo
      MPI_Recv(&f, nodenum, MPI_INT, 0, 1, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
    }
  } else if( id == 0){
    while (fabs(f - 3.1416) > 0.00009)
    {

      for (int i = 0; i < nodenum-1; i++)
      {
        // recibo de los otros nodos 
        MPI_Recv(&cont_reciv[i], nodenum, MPI_INT,
        MPI_ANY_SOURCE, 1, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        MPI_Recv(&cant_reciv[i], nodenum, MPI_LONG,
        MPI_ANY_SOURCE, 2, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
      }
      int cont_final = 0;
      int cant_final = 0;
      for (int i = 0; i < nodenum-1; i++)
      {
        // hago el conteo final
        cont_final += cont_reciv[i];
        cant_final += cant_reciv[i];
      }

      float estimated_pi = ((float)cont_final / (float)cant_final) * 4.0;
      f = floor(10000 * estimated_pi) / 10000;
      // calculo pi estimado
      for (int i = 0; i < nodenum-1; i++)
      {
        // lo envio a los demás procesos para que sepan si deben terminar o no el loop
        MPI_Send(&f, 1, MPI_INT, i+1, 1, MPI_COMM_WORLD);

      }
    }
  }
  printf("PI ES : %.4f id %d\n", f, id);
  MPI_Finalize();
  tiempo_final = clock();

  segundos = (double)(tiempo_final - tiempo_inicio) / CLOCKS_PER_SEC;

  printf("%f\n",segundos); 
  return 0;
}