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


    def __repr__(self):
        return self.type + " of " + str(self.process.id) + " on " + self.loc + " @ " + str(self.time)


class Process:
    def __init__(self, id, arr_time):
        self.id = id
        self.arr_time = arr_time

    def find_turnaround(self, time):
        return time - self.arr_time

    def __repr__(self):
        return str(self.id) + " arrived at " + str(self.arr_time)


class CPU:
    def __init__(self, service_time):
        self.avail = True
        self.service_time = service_time
        self.queue = []
        self.time_since_on = 0
        self.total_time = 0

    def arr_handler(self, eq, event, time):
        if self.avail:
            self.avail = False
            self.time_since_on = time
            eq.append(Event(event.process, 'DEP', 'CPU', time+exponential(self.service_time)))
        else:
            self.queue.append(event.process)

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
            self.total_time += (time - self.time_since_on)
        return exit

    def handle_util(self, time):
        if not self.avail:
            self.total_time += (time - self.time_since_on)



class DISK:
    def __init__(self, service_time):
        self.avail = True
        self.service_time = service_time
        self.queue = []
        self.time_since_on = 0
        self.total_time = 0

    def arr_handler(self, eq, event, time):
        if self.avail:
            self.avail = False
            self.time_since_on = time
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
            self.total_time += (time - self.time_since_on)

    def handle_util(self, time):
        if not self.avail:
            self.total_time += (time - self.time_since_on)


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
    iteration = 0
    cpu_queue_cap = 0
    disk_queue_cap = 0
    turnaround = 0
    eq = []
    eq.append(new_process(id, time, arr_rate))
    while len(eq) != 0 and processes < 10000:
        iteration += 1
        eq = sorted(eq, key=lambda event: event.time)
        time = eq[0].time
        curr = eq[0]
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
                    turnaround += curr.process.find_turnaround(time)
        elif curr.loc == 'DISK':
            if curr.type == 'ARR':
                disk.arr_handler(eq, curr, time)
            elif curr.type == 'DEP':
                disk.dep_handler(eq, curr, time)
        cpu_queue_cap += len(cpu.queue)
        disk_queue_cap += len(disk.queue)
    cpu.handle_util(time)
    disk.handle_util(time)
    print("FINAL STATS:")
    print("Average Turnaround: \n" + str(turnaround/10000))
    print("Average Throughput: \n" + str(time/10000))
    print("CPU Util: \n" + str(cpu.total_time/time))
    print("Disk Util: \n" + str(disk.total_time/time))
    print("Average # of items in CPU queue: \n" + str(cpu_queue_cap / iteration))
    print("Average # of items in Disk queue: \n" + str(disk_queue_cap / iteration))







main()
