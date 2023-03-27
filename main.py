import random
import math
import sys


def exponential(lmbda):
    z = random.random()
    return (-lmbda) * math.log(z)

class Event:
    def __init__(self, id, type, loc, time):
        self.type = type
        self.loc = loc
        self.time = time
        self.id = id

    def __repr__(self):
        return self.type + " of " + str(self.id) + " on " + self.loc


class CPU:
    def __init__(self, service_time):
        self.avail = True
        self.service_time = service_time
        self.queue = []

    def arr_handler(self, eq, event, time):
        if self.avail:
            self.avail = False
            eq.append(Event(event.id, 'DEP', 'CPU', time+exponential(self.service_time)))
        else:
            self.queue.append(event)


class DISK:
    def __init__(self, service_time):
        self.avail = True
        self.service_time = service_time
        self.queue = []

    def arr_handler(self, eq, event, time):
        if self.avail:
            self.avail = False
            eq.append(Event(event.id, 'DEP', 'DISK', time+exponential(self.service_time)))
        else:
            self.queue.append(event)


def main():
    if len(sys.argv) != 4:
        print("please use 3 arguments:\n"
              "1: average arrival rate\n"
              "2: average CPU service time\n"
              "3: average Disk service time\n")
        return 1
    arr_rate = float(sys.argv[1])
    cpu_serv = float(sys.argv[2])
    dsk_serv = float(sys.argv[3])
    processes = 0
    time = 0
    eq = [Event(0, 'ARR', 'CPU', exponential(1/arr_rate))]
    eq = sorted(eq, key=lambda event: event.time)
    print(eq)
    print(eq[0].time)


main()
