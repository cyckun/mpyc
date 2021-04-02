#cao add 20210401; Compute x*x (x = (x1, x2))

import random
import sys
from mpyc.runtime import mpc

if __name__ == '__main__':

    m = len(mpc.parties)
    # m = 3
    print("m = ", m)
    if m % 2 == 0:
        print('OT runs with even number of parties only.')
        sys.exit()

    t = m // 2
    message = [(None, None)] * t
    choice = [None] * t
    if mpc.pid == 0:
        print('You are the trusted third party.')
    elif 1 <= mpc.pid <= t:
        message[mpc.pid - 1] = (random.randint(0, 99), random.randint(0, 99))
        print(f'You are sender {mpc.pid} holding messages '
              f'{message[mpc.pid - 1][0]} and {message[mpc.pid - 1][1]}.')
    else:
        choice[mpc.pid - t - 1] = random.randint(0, 1)
        print(f'You are receiver {mpc.pid - t} with random choice bit {choice[mpc.pid - t - 1]}.')

    mpc.run(mpc.start())

    secnum = mpc.SecInt()
    for i in range(1, t + 1):
        #x = mpc.input([secnum(message[i - 1][0]), secnum(18)], i)
        x = mpc.input(secnum(18), i)
        b = mpc.input(secnum(choice[i - 1]), t + i)
        #a = mpc.run(mpc.output(mpc.if_else(b, x[1], x[0]), t + i))
        a = mpc.run(mpc.output(mpc.mul(x, x), t + i))
        if a:
            print(f'You have received message {a}.')

    mpc.run(mpc.shutdown())
