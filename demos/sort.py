"""Demo oblivious sorting in MPyC, with full secrecy.

Randomly generated secret-shared lists of numbers (integers or fixed-point numbers)
are sorted using MPyC's built-in functions mcp.sorted() and seclist.sort(),
which are the secure counterparts of Python's built-in function sorted() and
list.sort(), respectively.
"""

import sys
from mpyc.runtime import mpc
from mpyc.seclists import seclist


async def main():
    if sys.argv[1:]:
        n = int(sys.argv[1])
    else:
        n = 5
        print('Setting input to default =', n)

    s = [(-1)**i * (i + n//2)**2 for i in range(n)]
    print("s = ",s)
    secnum = mpc.SecInt()
    print("bitlenght", secnum.field.order)
    print('Using secure integers:', secnum)
    x = list(map(secnum, s))
    print("x：",x[0].share)
    async with mpc:
        mpc.random.shuffle(secnum, x)  # secret in-place random shuffle
        print('Randomly shuffled input:', await mpc.output(x))
        x = mpc.sorted(x, key=lambda a: a**2)  # sort on absolute value
        print('Sorted by absolute value:', await mpc.output(x))

    secnum = mpc.SecFxp()
    print("secnum prime: ", secnum.field.order, secnum.bit_length)
    print('Using secure fixed-point numbers:', secnum)
    print("bit lof secfix:", secnum.bit_length)
    x = list(map(secnum, s))
    async with mpc:
        mpc.random.shuffle(secnum, x)  # secret in-place random shuffle
        print('Randomly shuffled input:', await mpc.output(x))
        x = seclist(x)
        x.sort(reverse=True)  # in-place sort in descending order
        print('Sorted by descending value:', await mpc.output(list(x)))

if __name__ == '__main__':
    mpc.run(main())
