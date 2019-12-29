##### MANUAL DE USO #####
#########################

Forma de uso: al correr el programa, te pedirá un input, este debe ser el nombre de un csv
con los elementos del input(de la forma mostrada en el enunciado, pero separado por comas).
Vienen ejemplos de inputs :D.
Luego el programa lo lee, arma el tablero con el juego y realiza las iteraciones.
Se printea el estado del programa en cada iteración (solo para ver) y al final se printea el output correspondiente.

Para la funcionalidad de la sincronización realicé una clase barrera, que recibe un número n, indicador de cuantos threads
se debe esperar, cada vez que alguien pide la barrera se suma uno a un contador interno, cuando se llega a n se liberan en cadena
los threads y cuando el contador vuelve a 0, la barrera se vuelve a bloquear.

Para cada celda en el juego, creé un thread que revisara el estado de la celda y definiera un next step, para revisar y definir next,
todos los threads pueden hacerlo al mismo tiempo, así que usé una barrera para que todos revisaran, luego de llegar a ella, todos cambian
de acuerdo a su next(tambien sincronizado con barrera para no empezar una iteración antes de que alguien haya cambiado).

Supuestos: 
1) Utilicé las reglas que salian en internet, ya que varias diferian con las del enunciado 
(como cuantos elementos eran sobrepoblación para que un ser muriera) y estás si daban los resultados de los ejemplos del enunciado.

2) Cuando un ser debe nacer y tiene suficientes planctos vecinos para nacer y hay al menos 1 ameba vecina, nace como ameba.

3) Cuando un plancton tiene una ameba vecina, ese instante de tiempo lo uso solo para transformarlo a ameba y en el siguiente se ve si sobrevive o no.
Ej: 3 amebas vecinas y estoy revisando un plancton en el instante t=1, en t=1 se transforma a ameba (si revisabamos primero si cumplía las reglas para seguir vivo debería morir), 
y en t=2 se revisa si cumple las condiciones para seguir viviendo como ameba.
