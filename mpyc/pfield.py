"""This module supports Galois (finite) fields of prime order.

Function GF creates types implementing prime fields.
Instantiate an object from a field and subsequently apply overloaded
operators such as + (addition), - (subtraction), * (multiplication),
and / (division), etc., to compute with field elements.
In-place versions of the field operators are also provided.
Modular square roots and quadratic residuosity tests supported as well.
"""

import mpyc.gmpy as gmpy2


def find_prime_root(l, blum=True, n=1):
    """Find smallest prime of bit length at least l satisfying given constraints.

    Default is to return Blum primes (primes p with p % 4 == 3).
    Also, a primitive root w is returned of prime order at least n.
    """
    if l == 2:
        if not blum:
            p = 2
            assert n == 1
            w = 1
        else:
            p = 3
            n, w = 2, -1
    elif n <= 2:
        n, w = 2, -1
        p = gmpy2.next_prime(1 << l - 1)
        if blum:
            while p % 4 != 3:
                p = gmpy2.next_prime(p)
        p = int(p)
    else:
        assert blum
        if not gmpy2.is_prime(n):
            n = int(gmpy2.next_prime(n))
        p = 1 + n * (1 + (n**2) % 4 + 4 * ((1 << l - 2) // n))
        while not gmpy2.is_prime(p):
            p += 4 * n

        a = 1
        w = 1
        while w == 1:
            a += 1
            w = gmpy2.powmod(a, (p - 1) // n, p)
        p, w = int(p), int(w)
    return p, n, w


# Calls to GF with identical modulus and frac_length return the same class.
_field_cache = {}


def GF(modulus, f=0):
    """Create a Galois (finite) field for given prime modulus."""
    if isinstance(modulus, tuple):
        p, n, w = modulus
    else:
        p = modulus
        if p == 2:
            n, w = 1, 1
        else:
            n, w = 2, -1

    if (p, f) in _field_cache:
        return _field_cache[(p, f)]

    if not gmpy2.is_prime(p):
        raise ValueError(f'{p} is not a prime')

    GFElement = type(f'GF({p})', (PrimeFieldElement,), {'__slots__': ()})
    GFElement.modulus = p
    GFElement.order = p
    GFElement.is_signed = True
    GFElement.nth = n
    GFElement.root = w % p
    GFElement.frac_length = f
    GFElement.rshift_factor = int(gmpy2.invert(1 << f, p))  # cache (1/2)^f mod p
    _field_cache[(p, f)] = GFElement
    return GFElement


class PrimeFieldElement():
    """Common base class for prime field elements.

    Invariant: attribute 'value' nonnegative and below prime modulus.
    """

    __slots__ = 'value'

    modulus = None
    order = None
    is_signed = None
    nth = None
    root = None
    frac_length = 0
    rshift_factor = 1

    def __init__(self, value):
        self.value = value % self.modulus

    def __int__(self):
        """Extract (signed) integer value from the field element."""
        if self.is_signed:
            v = self.signed()
        else:
            v = self.unsigned()
        return round(v)

    def __float__(self):
        """Extract (signed) float value from the field element."""
        if self.is_signed:
            v = self.signed()
        else:
            v = self.unsigned()
        return float(v)

    def __abs__(self):
        """Absolute value of (signed) value."""
        if self.is_signed:
            v = self.signed()
        else:
            v = self.unsigned()
        return abs(v)

    @classmethod
    def to_bytes(cls, x):
        """Return an array of bytes representing the given list of integers x."""
        byteorder = 'little'
        r = (cls.modulus.bit_length() + 7) >> 3
        data = bytearray(2 + len(x) * r)
        data[:2] = r.to_bytes(2, byteorder)
        i = 2
        for v in x:
            j = i + r
            data[i:j] = v.to_bytes(r, byteorder)
            i = j
        return data

    @staticmethod
    def from_bytes(data):
        """Return the list of integers represented by the given array of bytes."""
        byteorder = 'little'
        from_bytes = int.from_bytes  # cache
        r = from_bytes(data[:2], byteorder)
        n = (len(data) - 2) // r
        x = [None] * n
        i = 2
        for k in range(n):
            j = i + r
            x[k] = from_bytes(data[i:j], byteorder)
            i = j
        return x

    def __add__(self, other):
        """Addition."""
        if isinstance(other, type(self)):
            return type(self)(self.value + other.value)

        if isinstance(other, int):
            return type(self)(self.value + other)

        return NotImplemented

    __radd__ = __add__

    def __iadd__(self, other):
        """In-place addition."""
        if isinstance(other, type(self)):
            other = other.value
        elif not isinstance(other, int):
            return NotImplemented

        self.value += other
        self.value %= self.modulus
        return self

    def __sub__(self, other):
        """Subtraction."""
        if isinstance(other, type(self)):
            return type(self)(self.value - other.value)

        if isinstance(other, int):
            return type(self)(self.value - other)

        return NotImplemented

    def __rsub__(self, other):
        """Subtraction (with reflected arguments)."""
        if isinstance(other, int):
            return type(self)(other - self.value)

        return NotImplemented

    def __isub__(self, other):
        """In-place subtraction."""
        if isinstance(other, type(self)):
            other = other.value
        elif not isinstance(other, int):
            return NotImplemented

        self.value -= other
        self.value %= self.modulus
        return self

    def __mul__(self, other):
        """Multiplication."""
        if isinstance(other, type(self)):
            return type(self)(self.value * other.value)

        if isinstance(other, int):
            return type(self)(self.value * other)

        return NotImplemented

    __rmul__ = __mul__

    def __imul__(self, other):
        """In-place multiplication."""
        if isinstance(other, type(self)):
            other = other.value
        elif not isinstance(other, int):
            return NotImplemented

        self.value *= other
        self.value %= self.modulus
        return self

    def __pow__(self, exponent):
        """Exponentiation."""
        return type(self)(int(gmpy2.powmod(self.value, exponent, self.modulus)))

    def __neg__(self):
        """Negation."""
        return type(self)(-self.value)

    def __truediv__(self, other):
        """Division."""
        if isinstance(other, type(self)):
            return self * other.reciprocal()

        if isinstance(other, int):
            return self * type(self)(other).reciprocal()

        return NotImplemented

    def __rtruediv__(self, other):
        """Division (with reflected arguments)."""
        if isinstance(other, int):
            return type(self)(other) * self.reciprocal()

        return NotImplemented

    def __itruediv__(self, other):
        """In-place division."""
        if isinstance(other, int):
            other = type(self)(other)
        elif not isinstance(other, type(self)):
            return NotImplemented

        self.value *= other.reciprocal().value
        self.value %= self.modulus
        return self

    def reciprocal(self):
        """Multiplicative inverse."""
        return type(self)(int(gmpy2.invert(self.value, self.modulus)))

    def __lshift__(self, other):
        """Left shift."""
        if not isinstance(other, int):
            return NotImplemented

        return type(self)(self.value << other)

    def __rlshift__(self, other):
        """Left shift (with reflected arguments)."""
        return NotImplemented

    def __ilshift__(self, other):
        """In-place left shift."""
        if not isinstance(other, int):
            return NotImplemented

        self.value <<= other
        self.value %= self.modulus
        return self

    def __rshift__(self, other):
        """Right shift."""
        if not isinstance(other, int):
            return NotImplemented

        if other == self.frac_length:
            rsf = self.rshift_factor
        else:
            rsf = int(gmpy2.invert(1 << other, self.modulus))
        return type(self)(self.value * rsf)

    def __rrshift__(self, other):
        """Right shift (with reflected arguments)."""
        return NotImplemented

    def __irshift__(self, other):
        """In-place right shift."""
        if not isinstance(other, int):
            return NotImplemented

        if other == self.frac_length:
            rsf = self.rshift_factor
        else:
            rsf = int(gmpy2.invert(1 << other, self.modulus))
        self.value *= rsf
        self.value %= self.modulus
        return self

    def is_sqr(self):
        """Test for quadratic residuosity (0 is also square)."""
        p = self.modulus
        if p == 2:
            return True

        return gmpy2.legendre(self.value, p) != -1

    def sqrt(self, INV=False):
        """Modular (inverse) square roots."""
        a = self.value
        p = self.modulus
        if p == 2:
            return type(self)(a)

        if p & 3 == 3:
            if INV:
                q = (p * 3 - 5) >> 2  # a**q == a**(-1/2) == 1/sqrt(a) mod p
            else:
                q = (p + 1) >> 2
            return type(self)(int(gmpy2.powmod(a, q, p)))

        # 1 (mod 4) primes are covered using Cipolla-Lehmer's algorithm.
        # find b s.t. b^2 - 4*a is not a square (maybe cache this for p)
        b = 1
        while gmpy2.legendre(b * b - 4 * a, p) != -1:
            b += 1

        # compute u*X + v = X^{(p+1)/2} mod f, for f = X^2 - b*X + a
        u, v = 0, 1
        e = (p + 1) >> 1
        for i in range(e.bit_length() - 1, -1, -1):
            u2 = (u * u) % p
            u = ((u << 1) * v + b * u2) % p
            v = (v * v - a * u2) % p
            if (e >> i) & 1:
                u, v = (v + b * u) % p, (-a * u) % p
        if INV:
            return type(self)(v).reciprocal()

        return type(self)(v)

    def signed(self):
        """Return signed integer representation, symmetric around zero."""
        v = self.value
        if v > self.modulus >> 1:
            v -= self.modulus
        if self.frac_length:
            v = float(v * 2**-self.frac_length)
        return v

    def unsigned(self):
        """Return unsigned integer representation."""
        if self.frac_length:
            return float(self.value * 2**-self.frac_length)

        return self.value

    def __repr__(self):
        if self.frac_length:
            return f'{self.__float__()}'

        return f'{self.__int__()}'

    def __eq__(self, other):
        """Equality test."""
        if isinstance(other, type(self)):
            return self.value == other.value

        if isinstance(other, int):
            if self.frac_length:
                other <<= self.frac_length
            return self.value == type(self)(other).value

        if self.frac_length:
            if isinstance(other, float):
                other = round(other * (1 << self.frac_length))
                return self.value == type(self)(other).value

        return NotImplemented

    def __bool__(self):
        """Truth value testing.

        Return False if this field element is zero, True otherwise.
        Field elements can thus be used directly in Boolean formulas.
        """
        return self.value != 0
