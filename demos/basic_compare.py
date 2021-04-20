
import sys, getopt
from mpyc.runtime import mpc


secnum = mpc.SecInt()
if __name__ == '__main__':
    mpc.run(mpc.start())
    x = mpc.input(secnum(1), 0)
    y = mpc.input(secnum(2), 1)
    tmp = mpc.sgn(x-y)
    a = mpc.run(mpc.output(tmp, 1))
    if a:
        print(f'You have received message {a}.')
    mpc.run(mpc.shutdown())