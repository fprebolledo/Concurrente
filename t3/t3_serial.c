#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>

int main(int argc, char const *argv[])
{
  clock_t tiempo_final, tiempo_inicio = clock();
  double segundos;
  int cantidad = 0;
  float x, y, z;
  int i, count = 0;
  float rial_pi = 3.1416;
  float f = 0;
  while (fabs(f - 3.1416) > 0.00009)
  {
    x = (float)random() / RAND_MAX;
    y = (float)random() / RAND_MAX;
    // función H(x,y)
    z = x*x + y*y;
    if (z<=1)
    {
      count++;
    }
    cantidad++;
    //calculo pi estimado y saco los 4 decimales
    float estimated_pi = ((float)count / (float)cantidad) * 4.0;
    f = floor(10000 * estimated_pi) / 10000;
  }

 tiempo_final = clock();

  segundos = (double)(tiempo_final - tiempo_inicio) / CLOCKS_PER_SEC;

  printf("%f\n",segundos); 
  printf("PI ES : %.4f\n", f);
  return 0;
}