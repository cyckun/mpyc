# basic test of mpyc. 20210329
# including add / mul

import sys

from mpyc.random import getrandbits

from mpyc.runtime import mpc
from mpyc import gfpx
from mpyc import sectypes

if __name__ == '__main__':
    # 1 party mul;
    secfield = mpc.SecFld(11)
    f11 = secfield.field
    a = getrandbits(secfield, 8)
    b = getrandbits(secfield, 8)
    print("a = ", mpc.output(a))
    print("b = ", mpc.output(b))
    print("a*b=", a*b)
    tst = mpc.output(a*b)
    print(tst)
    # 2 party mul;
    test_runtime =

"""
    secfield = mpc.SecFld(11)
    f11 = secfield.field
    a = getrandbits(secfield, 8)
    b = getrandbits(secfield, 8)
    print("a = ", mpc.output(a))
    print("b = ", mpc.output(b))
    print("a*b=", a*b)
    tst = mpc.run(mpc.output(a*b))
    print(tst)
"""