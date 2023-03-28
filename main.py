import random
import math
import sys


def exponential(lmbda):
    z = random.random()
    return (-lmbda) * math.log(z)

class Event:
    def __init__(self, process, type, loc, time):
        self.type = type
        self.loc = loc
        self.process = process
        self.time = time

    def handle_event(self):
        return
    def __repr__(self):
        return self.type + " of " + str(self.process.id) + " on " + self.loc + " @ " + str(self.time)


class Process:
    def __init__(self, id, arr_time):
        self.id = id
        self.arr_time = arr_time

    def __repr__(self):
        return str(self.id) + " arrived at " + str(self.arr_time)


class CPU:
    def __init__(self, service_time):
        self.avail = True
        self.service_time = service_time
        self.queue = []

    def arr_handler(self, eq, event, time):
        if self.avail:
            self.avail = False
            eq.append(Event(event.process, 'DEP', 'CPU', time+exponential(self.service_time)))
        else:
            self.queue.append(event)

    def dep_handler(self, eq, event, time):
        prob = random.random()
        exit = False
        if prob <= 0.6:
            exit = True
        else:
            eq.append(Event(event.process, 'ARR', 'DISK', time))
        if len(self.queue) > 0:
            eq.append(Event(self.queue[0], 'DEP', 'CPU', time+exponential(self.service_time)))
            self.queue.pop(0)
        else:
            self.avail = True
        return exit



class DISK:
    def __init__(self, service_time):
        self.avail = True
        self.service_time = service_time
        self.queue = []

    def arr_handler(self, eq, event, time):
        if self.avail:
            self.avail = False
            eq.append(Event(event.process, 'DEP', 'DISK', time+exponential(self.service_time)))
        else:
            self.queue.append(event.process)

    def dep_handler(self, eq, event, time):
        eq.append(Event(event.process, 'ARR', 'CPU', time))
        if len(self.queue) > 0:
            eq.append(Event(self.queue[0], 'DEP', 'DISK', time+exponential(self.service_time)))
            self.queue.pop(0)
        else:
            self.avail = True


def new_process(id, time, arr_rate):
    arr_time = time + exponential(1/arr_rate)
    return Event(Process(id, arr_time), 'ARR', 'CPU', arr_time)


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
    disk = DISK(dsk_serv)
    cpu = CPU(cpu_serv)
    processes = 0
    id = 0
    time = 0
    eq = []
    eq.append(new_process(id, time, arr_rate))

    while len(eq) != 0 and processes <= 2:
        print("\n")
        eq = sorted(eq, key=lambda event: event.time)
        time = eq[0].time
        print(time)
        print(eq)
        curr = eq[0]
        print(curr)
        eq.pop(0)
        if curr.loc == 'CPU':
            if curr.type == 'ARR':
                cpu.arr_handler(eq, curr, time)
                if curr.process.id == id:
                    id += 1
                    eq.append(new_process(id, time, arr_rate))
            elif curr.type == 'DEP':
                if cpu.dep_handler(eq, curr, time):
                    processes+=1
        elif curr.loc == 'DISK':
            if curr.type == 'ARR':
                disk.arr_handler(eq, curr, time)
            elif curr.type == 'DEP':
                disk.dep_handler(eq, curr, time)
        print(eq)
        print("PROCESSES COMPLETE: " + str(processes))




main()
