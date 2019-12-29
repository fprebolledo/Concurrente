from threading import Thread, Condition, Lock
import time
import random
import queue as q
import csv

contrario = [4, 3, 2, 1]
N_SECRETARIAS = 3
N_ENFERMERAS = 2
N_DOCTORES = 3

def mostrar(personal, persona):
    # esta función es para printear la acción y los estados de las colas
    # pido los locks mas que nada para poder printear todo junto

    personal.general.acquire()
    personal.espera.acquire()
    personal.prioridad.acquire()

    print("**********************************************************************")
    if personal.tipo == "Doctor":
        print(f"{personal.tipo} {personal.name}: Ha atendido a {persona[1]}, esta lista para ir a casa")
    elif personal.tipo == "Secretaria":
        print(f"{personal.tipo} {personal.name}: Ha registrado a {persona[0]}, debe esperar para ser evaluada")
    else:
        print(f"{personal.tipo} {personal.name}: Ha evaluado {persona[1]} con {persona[2]}")
    print(list(personal.cola_general.queue))
    print(list(personal.cola_espera.queue))
    # el orden printeado en la cola de prioridad no es el orden de la cola! ya que se convierte en una lista
    # y esta no conserva el mismo orden
    print(list(personal.cola_prioridad.queue))
    print("**********************************************************************\n")

    personal.prioridad.release()
    personal.espera.release()
    personal.general.release()


class Secretaria(Thread):
    def __init__(self, tipo, name, general, espera, cola_general, cola_espera, cola_prioridad, prioridad):
        Thread.__init__(self)
        self.name = name
        self.tipo = tipo
        self.general = general
        self.espera = espera
        self.cola_general = cola_general
        self.cola_espera = cola_espera
        self.cola_prioridad = cola_prioridad
        self.prioridad = prioridad

    def atentender(self):
        self.general.acquire()
        # pido lock para no tener conflictos al revisar y sacar persona de la cola
        persona_registrada = self.cola_general.get()
        # suelto lock porque ya saqué a persona de la cola
        print_lock.acquire()

        self.general.release()

        self.espera.acquire()
        # pongo a la persona
        self.cola_espera.put(persona_registrada)
        self.espera.notify() # le aviso a la enfermera qe hay un nuevo paciente
        self.espera.release()

        mostrar(self, persona_registrada)
        print_lock.release()

    def run(self):
        # mietras queden pacientes esperando a ser registrados sigo atendiendo

        while not self.cola_general.empty():
            self.atentender()
            time.sleep(random.randint(1, 2))


class Enfermera(Thread):
    def __init__(self, tipo, name, espera, prioridad, cola_espera, cola_prioridad, cola_general, general):
        Thread.__init__(self)
        self.name = name
        self.tipo = tipo
        self.espera = espera
        self.prioridad = prioridad
        self.cola_prioridad = cola_prioridad
        self.cola_espera = cola_espera
        self.cola_general = cola_general
        self.general = general

    def evaluar(self):
        self.espera.acquire()
        # si no hay nada en la cola, espero
        if self.cola_espera.empty(): 
            self.espera.wait()
            if self.cola_espera.empty():
                # si me desperté y no habia nada, porque otra enfermera lo sacó o porque ya no hay más pacientes
                self.espera.notify()
                self.espera.release()
                return

        persona = self.cola_espera.get()
        self.espera.release()
        # le asigno una prioridad (es la inversa ya que las priority queue el más prioritario es el número más bajo)
        con_prioridad = (contrario[persona[1] - 1], persona[0], "gravedad:" + str(persona[1]))


        self.prioridad.acquire()

        # se inserta en la cola de prioridad
        self.cola_prioridad.put(con_prioridad)
        # aviso a un doctor si esque había
        self.prioridad.notify()
        self.prioridad.release()

        mostrar(self, con_prioridad)

    def run(self):
        # mientras queden pacientes en la cola general o en la de espera sigo evaluando

        while not (self.cola_general.empty() and self.cola_espera.empty()):
            self.evaluar()
            time.sleep(random.randint(1, 2))

        self.espera.acquire()
        # si yo terminé pero hay enfermeras que estaban esperando, las notifico para que terminen
        self.espera.notifyAll()
        self.espera.release()


class Doctor(Thread):
    def __init__(self, tipo, name, prioridad, cola_prioridad, cola_general, cola_espera, general, espera):
        Thread.__init__(self)
        self.tipo = tipo
        self.name = name
        self.prioridad = prioridad
        self.cola_prioridad = cola_prioridad
        self.cola_general = cola_general
        self.cola_espera = cola_espera
        self.general = general
        self.espera = espera

    def atender_paciente(self):
        self.prioridad.acquire()
        # si la cola de prioridad está vacía, espero
        if self.cola_prioridad.empty():
            self.prioridad.wait()
            # si desperté y me "quitaron" el paciente ó ya no queda nadie más en el hospital, solo retorno para poder termiar o volver a esperar
            if self.cola_prioridad.empty():
                self.prioridad.notify()
                self.prioridad.release()
                return

        persona_atendida = self.cola_prioridad.get()
        # saco a la persona y la mando a su casa :3
        self.prioridad.release()
        mostrar(self, persona_atendida)

    def run(self):
        # mientras queden pacientes en algún lado sigo atendiendo
        while not (self.cola_general.empty() and self.cola_espera.empty() and self.cola_prioridad.empty()):
            self.atender_paciente()
            time.sleep(random.randint(1, 2))

        self.prioridad.acquire()
        #si terminé, ya no quedan mas pacientes, porlo que si había algún doctor esperando, le aviso.
        self.prioridad.notifyAll()
        self.prioridad.release()


if __name__ == "__main__":
    print_lock = Lock()
    cola_general = q.Queue()
    cola_espera = q.Queue()
    cola_prioridad = q.PriorityQueue()
    general = Condition()
    espera = Condition()
    prioridad = Condition()

    archivo = input("ingrese nombre del archivo: ")
    cont = 0
    with open(archivo) as file:
        read = csv.reader(file, delimiter=" ")
        for line in read:
            if cont == 0:
                cont += 1
                continue
            cola_general.put((line[0], int(line[1])))

    print("Inicio: \n")
    print(list(cola_general.queue))
    print(list(cola_espera.queue))
    print(list(cola_prioridad.queue))

    entidades = []

    for i in range(N_SECRETARIAS):
        sec = Secretaria("Secretaria", i, general, espera, cola_general, cola_espera, cola_prioridad, prioridad)
        entidades.append(sec)

    for i in range(N_ENFERMERAS):
        enf = Enfermera("Enfermera", i, espera, prioridad, cola_espera, cola_prioridad, cola_general, general)
        entidades.append(enf)

    for i in range(N_DOCTORES):
        doc = Doctor("Doctor", i, prioridad, cola_prioridad, cola_general, cola_espera, general, espera)
        entidades.append(doc)

    for thread in entidades:
        # inicio los threads
        thread.start()

    for thread in entidades:
        # espero que todos terminen
        thread.join()

    print("Hemos atendido a todas las personas del hospital!")