Manual de uso:

* Forma de uso: al correr el prorgrama, este te pedirá el nombre
de un archivo, el cual debe ser un txt, con los elementos del input
se la forma mostrada en el enunciado.
Vienen ejemplos de input.
Luego el programa lo lee, y forma una cola FIFO con el orden dispuesto
en el archivo txt.
Se crean los threads correspodientes, se printea el estado inicial
y se hace correr cada uno, con sus respectivos prints.

Para la funcionalidad de sincronización por monitor, realicé 3 clases(threads):
Secretaria, Enfermera, Doctor, donde todas recibian las variables de condición
para cada una de las colas, junto con las colas (general, espera, prioridad).

Abajo de los imports, hay  3 números que indican, el número de secretarias, 
enfermeras, y doctores.

Luego la función run de cada uno dependía de lo que debía hacer, en caso
de las secretarias, mientras hubiesen personas en la cola general, trataban 
de sacarlas de la cola e insertarlas en la de espera(todo esto bajo exclusión 
mutua entre colas), para los otros 2 casos es lo mismo, pero con las colas 
correspondientes.

* Supuestos:

Añadí los casos en que si por algún motivo, se leía la condición del while 
de run verdadera, y al instante de entrar en un wait:
por ejemplo, queda una persona en la cola de espera, la enfermera 0 lee que queda gente, 
y la enfermera 1 también, enf 1 toma el loc primero, por lo que saca a la persona, 
mientras que enfermera 0 queda esperando, por lo que cuando enfermera uno salga de la acción,
su thread terminará y antes de terminar, hago que envie una señal a sus pares diciendo que 
ya no queda más trabajo, es decir, deben terminar.
Esto fue hecho para enfermeras y doctores.