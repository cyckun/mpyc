#cao add 20210401; Compute x*x (x = (x1, x2))

import random
import sys, getopt
from mpyc.runtime import mpc

if __name__ == '__main__':

    opts, args = getopt.getopt(sys.argv[1:], "M")
    for op, value in opts:
        if op == '-M':
            m = value
            print("m11 = ", m)
        else:
            print("opt error.")

    m = len(mpc.parties)
    # m = 3
    print("m = ", m)
    if m % 2 == 1:
        print('OT runs with even number of parties only.')
        sys.exit()

    t = m // 2
    message = [(None, None)] * t
    choice = [None] * t
    message[0] = (random.randint(0, 99), random.randint(0, 99))
    print("mpc.pid = ", mpc.pid)
    print(f'You are sender {mpc.pid} holding messages '
        f'{message[mpc.pid - 1][0]} and {message[mpc.pid - 1][1]}.')
    choice[0] = random.randint(0, 1)
    print(f'You are receiver {mpc.pid - t} with random choice bit {choice[0]}.')

    mpc.run(mpc.start())

    secnum = mpc.SecInt()
    for i in range(0, 1):
        #x = mpc.input([secnum(message[i - 1][0]), secnum(18)], i)
        x = mpc.input(secnum(18), 0)
        b = mpc.input(secnum(choice[0]), 1)
        #a = mpc.run(mpc.output(mpc.if_else(b, x[1], x[0]), t + i))
        a = mpc.run(mpc.output(mpc.mul(x, x), t + i))
        if a:
            print(f'You have received message {a}.')

    mpc.run(mpc.shutdown())
