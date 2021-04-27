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

    mpc.run(mpc.start())

    secnum = mpc.SecInt()
    for i in range(0, 1):
        #x = mpc.input([secnum(message[i - 1][0]), secnum(18)], i)
        x = mpc.input(secnum(1800000000000000000000000000000000000000000000000000000000000000000000000000000000000), 0)
        b = mpc.input(secnum(6), 1)
        #a = mpc.run(mpc.output(mpc.if_else(b, x[1], x[0]), t + i))
        tmp = mpc.mul(x, b)
        a = mpc.run(mpc.output(tmp, i+1))
        if a:
            print(f'You have received message {a}.')

    mpc.run(mpc.shutdown())
