
import random
import sys, getopt
from mpyc.runtime import mpc

secnum = mpc.SecInt()

if __name__ == '__main__':
    mpc.run(mpc.start())
    x = secnum(2)
    y = secnum(3)
    x = mpc.input(x)
    y = mpc.input(y)
    y = mpc.output(mpc.mul(x[0], y[0]))
    #y = mpc.run(mpc.output(mpc.mul(x, y)))
    print("y = ", y )

    mpc.run(mpc.shutdown())