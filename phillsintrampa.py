from multiprocessing import Process
from multiprocessing import Condition, Lock
from multiprocessing import Array, Manager
from multiprocessing import Value
import time
import random



NPHIL = 5
K = 100

def delay(n):
    time.sleep(random.random()/n)

class Table():

    def __init__(self, NPHIL, manager):
        self.mutex = Lock()
        self.phil = None
        self.NPHIL = Value('i',0)
        #self.manager = Manager()
        self.listphil = manager.list([False for i in range(NPHIL)])
        self.ffork = Condition(self.mutex)


    def free_fork(self):
        return not self.listphil[(self.set_current_phil-1) % (len(self.listphil))] and not self.listphil[(self.set_current_phil+1) % (len(self.listphil))]


    def set_current_phil(self, num): #asigna un valor a cada uno de los procesos (filosofos)
        self.set_current_phil= num


    def wants_eat(self):
        self.mutex.acquire()
        self.ffork.wait_for(self.free_fork)
        self.listphil[self.set_current_phil] = True
        self.mutex.release()


    def wants_think(self):
        self.mutex.acquire()
        self.listphil[self.set_current_phil] = False
        self.ffork.notify_all()
        self.mutex.release()



def philosopher_task(num:int, table: Table):
    table.set_current_phil(num)
    while True:
        print (f"Philosofer {num} thinking")
        print (f"Philosofer {num} wants to eat")
        table.wants_eat()
        print (f"Philosofer {num} eating")
        table.wants_think()
        print (f"Philosofer {num} stops eating")
def main():
    manager = Manager()
    print("Hola mu wenas")
    table = Table(NPHIL, manager)
    philosofers = [Process(target=philosopher_task, args=(i,table)) \
                   for i in range(NPHIL)]
    print("Hola soy el principio")
    for i in range(NPHIL):
        philosofers[i].start()
    print("Hola soy la mitad")
    for i in range(NPHIL):
        philosofers[i].join()
    print("Hola soy el final")


if __name__ == '__main__':
    main()