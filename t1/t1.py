from threading import Thread, Semaphore
import itertools
import time
import csv



class Barrera:
    # Para esto me basé en este código, agregandole algunas otras cosas
    # https://stackoverflow.com/questions/26622745/implementing-barrier-in-python2-7

    def __init__(self, n):
        self.n = n
        self.count = 0
        self.mutex = Semaphore(1)
        self.barrier = Semaphore(0) #barrera parte bloqueada

    def wait(self):
        juego = ""
        self.mutex.acquire()
        self.count += 1
        self.mutex.release()

        if self.count == self.n: # si llegan los n procesos libero la primera vez
            self.barrier.release()

        self.barrier.acquire() #el thread que estaba acá pegado esperando, toma release() del if
        self.barrier.release() #se despierta al thread siguiente

        self.mutex.acquire()
        self.count -= 1 #resto al contador
        if self.count == 0: #si llegó a 0 bloqueo la barrera denuevo
            self.barrier.acquire()
        self.mutex.release()


def vecinos(tablero, row, col):
    # para revisar alrededor del ser actual
    permutaciones = list(set(itertools.permutations([-1, -1, 1, 1, 0], 2)))
    # para saber si esta en el tablero o se sale
    en_tablero = lambda ro, co: (ro in range(len(tablero)) and co in range(len(tablero[0])))

    vecinos = 0
    ameba = False
    amebas = 0
    planctons = 0

    for r, c in permutaciones:
        if tablero[row][col] != "X": # si estoy revisando una celda viva
            if en_tablero(r + row, c + col):
                if tablero[r + row][c + col] != "X":
                    if tablero[r + row][c + col] == tablero[row][col]:  # si es de mi ttipo
                        vecinos += 1 #tengo vecino
                    else: #si es contrario
                        ameba = True
        else:
            if en_tablero(r + row, c + col):
                if tablero[r + row][c + col] != "X":
                    if tablero[r + row][c + col] == "A":  # si es una ameba
                        amebas += 1
                        ameba = True
                    else:
                        planctons += 1

    if tablero[row][col] != "X":
        return vecinos, ameba
    else:
        #retorno el maximo ya que puede nacer como ameba o plancton y si ameba=true, nace como ameba,
        return max(amebas, planctons), ameba


def run(iteraciones, row, col, tablero, b1, b2):
    i = 0
    next = ""
    while (i< iteraciones):
        vecin, ameba = vecinos(tablero, row, col)

        # si el ser está vivo
        if tablero[row][col] != "X":
            # tiene que morir
            if vecin <= 1 or vecin >= 4:
                if (tablero[row][col] == "P" )& ameba:
                    next = "ameba" #si tiene una ameba cerca
                else:
                    next = "muerte"

            else:
                # si es un plancton y se tiene que transformar
                if ameba & (tablero[row][col] == "P"):
                    next = "ameba"
                else:
                    next = ""
        else:
            if vecin == 3:
                # si tiene que nacer
                if ameba:
                    next = "nacea"
                else:
                    next = "nacep"


        b1.wait() # espero a que todos revisen sus vecinos y definan su proximo estado

        #cambiar estado
        if next == "muerte":
            tablero[row][col] = "X"
        elif next == "ameba":
            tablero[row][col] = "A"
        elif next == "nacea":
            tablero[row][col] = "A"
        elif next == "nacep":
            tablero[row][col] = "P"
        else:
            tablero[row][col] = tablero[row][col]

        b2.wait() #espero a que todos cambien a su nuevo estado para revisar denuevo el tablero
        i += 1


if __name__ == "__main__":

    archivo = input("ingrese nombre del archivo: ")
    rows = 0
    cols = 0
    iteraciones = 0
    i = 0
    tablero = []

    with open(archivo) as file:
        read = csv.reader(file, delimiter=",")
        for line in read:
            if i == 0:
                rows = int(line[1])
                cols = int(line[0])
                iteraciones = int(line[2])
                for row in range(rows):
                    tablero.append([ "X" for j in range(cols)])
            else:
                tipo = line[0]
                tablero[int(line[1])][int(line[2])] = line[0]
            i += 1

    b1 = Barrera(rows*cols)
    b2 = Barrera(rows*cols)


    threads = [Thread(target=run, args=(iteraciones, i, j, tablero, b1, b2)) for i in range(rows) for j in range(cols)]
    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    for i in range(rows):
        for j in range(cols):
            if tablero[i][j] == "A":
                print(f"A {i} {j} ")
            if tablero[i][j] == "P":
                print(f"P {i} {j} ")
