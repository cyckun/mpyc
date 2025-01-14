
import sys, getopt
from mpyc.runtime import mpc


secnum = mpc.SecInt()
if __name__ == '__main__':
    mpc.run(mpc.start())
    x = 0
    y = 0
    num_x = 0
    num_y = 1
    if mpc.pid == 0:
        print("enter your number:")
        num_x = input('input x:')
    x = mpc.input(secnum(int(num_x)), 0)
    if mpc.pid == 1:
        num_y = input('input y:')
    y = mpc.input(secnum(int(num_y)), 1)
    print("x, y = ", x, y)
    tmp = mpc.sub(x, y)
    tmp = mpc.add(x,y)
    print("add tmp：", tmp)
    print("sub result:", mpc.run(mpc.output(tmp)))
    tmp = mpc.sgn(tmp)
    a = mpc.run(mpc.output(tmp, 1))
    if a:
        print(f'You have received message {a}.')
    mpc.run(mpc.shutdown())