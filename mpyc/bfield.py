"""This module supports Galois (finite) fields of characteristic 2.

Function GF creates types implementing binary fields.
Instantiate an object from a field and subsequently apply overloaded
operators such as + (addition), - (subtraction), * (multiplication),
and / (division), etc., to compute with field elements.
In-place versions of the field operators are also provided.
"""

from mpyc import gf2x


def find_irreducible(d):
    """Find smallest irreducible polynomial of degree d satisfying given constraints.

    Constraints ... primitive, low weight w=3, 5
    """
    return gf2x.next_irreducible(2**d - 1)


# Calls to GF with identical modulus return the same class.
_field_cache = {}


def GF(modulus):
    """Create a Galois (finite) field for given irreducible polynomial."""
    poly = gf2x.Polynomial(modulus)

    if poly in _field_cache:
        return _field_cache[poly]

    if not gf2x.is_irreducible(poly):
        raise ValueError(f'{poly} is not irreducible')

    GFElement = type(f'GF(2^{poly.degree()})', (BinaryFieldElement,), {'__slots__': ()})
    GFElement.modulus = poly
    GFElement.ext_deg = poly.degree()
    GFElement.order = 2**poly.degree()
    _field_cache[poly] = GFElement
    return GFElement


class BinaryFieldElement():
    """Common base class for binary field elements.

    Invariant: attribute 'value' is reduced.
    """

    __slots__ = 'value'

    modulus = None
    ext_deg = None
    order = None
    frac_length = 0

    def __init__(self, value):
        if isinstance(value, int):
            assert 0 <= value < self.order
            value = gf2x.Polynomial(value)
        self.value = value % self.modulus

    def __int__(self):
        """Extract polynomial field element as an integer."""
        return self.value.value

    @classmethod
    def to_bytes(cls, x):
        """Return an array of bytes representing the given list of polynomials x."""
        byteorder = 'little'
        r = (cls.ext_deg + 7) >> 3
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

        if isinstance(other, (int, gf2x.Polynomial)):
            return type(self)(self.value + other)

        return NotImplemented

    __radd__ = __add__  # TODO: __radd__ may skip first test

    def __iadd__(self, other):
        """In-place addition."""
        if isinstance(other, type(self)):
            other = other.value
        elif not isinstance(other, (int, gf2x.Polynomial)):
            return NotImplemented

        self.value += other
        return self

    __sub__ = __add__
    __rsub__ = __add__
    __isub__ = __iadd__

    def __mul__(self, other):
        """Multiplication."""
        if isinstance(other, type(self)):
            return type(self)(self.value * other.value)

        if isinstance(other, (int, gf2x.Polynomial)):
            return type(self)(self.value * other)

        return NotImplemented

    __rmul__ = __mul__

    def __imul__(self, other):
        """In-place multiplication."""
        if isinstance(other, type(self)):
            other = other.value
        elif not isinstance(other, (int, gf2x.Polynomial)):
            return NotImplemented

        self.value *= other
        self.value %= self.modulus.value
        return self

    def __pow__(self, other):
        """Exponentiation."""
        if not isinstance(other, int):
            return NotImplemented

        return type(self)(gf2x.powmod(self.value, other, self.modulus.value))

    def __neg__(self):
        """Negation."""
        return type(self)(self.value)

    def __truediv__(self, other):
        """Division."""
        if isinstance(other, type(self)):
            return self * other.reciprocal()

        if isinstance(other, (int, gf2x.Polynomial)):
            return self * type(self)(other).reciprocal()

        return NotImplemented

    def __rtruediv__(self, other):
        """Division (with reflected arguments)."""
        if isinstance(other, (int, gf2x.Polynomial)):
            return type(self)(other) * self.reciprocal()

        return NotImplemented

    def __itruediv__(self, other):
        """In-place division."""
        if isinstance(other, (int, gf2x.Polynomial)):
            other = type(self)(other)
        elif not isinstance(other, type(self)):
            return NotImplemented

        self.value *= other.reciprocal().value
        self.value %= self.modulus.value
        return self

    def reciprocal(self):
        """Multiplicative inverse."""
        return type(self)(gf2x.invert(self.value, self.modulus))

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
        self.value %= self.modulus.value
        return self

    def __rshift__(self, other):
        """Right shift."""
        if not isinstance(other, int):
            return NotImplemented

        return self * type(self)(1 << other).reciprocal()

    def __rrshift__(self, other):
        """Right shift (with reflected arguments)."""
        return NotImplemented

    def __irshift__(self, other):
        """In-place right shift."""
        if not isinstance(other, int):
            return NotImplemented

        self.value *= type(self)(1 << other).reciprocal().value
        self.value %= self.modulus.value
        return self

    def __repr__(self):
        return f'{self.value}'

    def __eq__(self, other):
        """Equality test."""
        if isinstance(other, type(self)):
            return self.value == other.value

        if isinstance(other, (int, gf2x.Polynomial)):
            return self.value == other

        return NotImplemented

    def __bool__(self):
        """Truth value testing.

        Return False if this field element is zero, True otherwise.
        Field elements can thus be used directly in Boolean formulas.
        """
        return bool(self.value)
