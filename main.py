import random
import math
import sys


def exponential(lmbda):
    z = random.random()
    z = z / 1
    return (-lmbda) * math.log(z)


def main():
    if len(sys.argv) != 4:
        print("please use 3 arguments:\n"
              "1: average arrival rate\n"
              "2: CPU service time\n"
              "3: Disk service time\n")
        return 1
    arr_rate = sys.argv[1]
    cpu_serv = sys.argv[2]
    dsk_serv = sys.argv[3]
    print("howdy ho!")
    processes = 0
    print(exponential(sys.argv[1]))


main()
