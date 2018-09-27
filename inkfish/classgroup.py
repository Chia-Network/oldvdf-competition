from . import mod


class ClassGroup(tuple):
    @classmethod
    def identity_for_discriminant(class_, d):
        return class_.from_ab_discriminant(1, 1, d)

    @classmethod
    def from_ab_discriminant(class_, a, b, discriminant):
        assert discriminant < 0
        assert discriminant % 4 == 1
        c = (b * b - discriminant) // (4 * a)
        p = class_(a, b, c).reduced()
        assert p.discriminant() == discriminant
        return p

    @classmethod
    def from_bytes(class_, bytearray, discriminant):
        int_size = (discriminant.bit_length() + 16) >> 4
        a = int.from_bytes(bytearray[0:int_size], "big", signed=True)
        b = int.from_bytes(bytearray[int_size:], "big", signed=True)
        return ClassGroup(a, b, (b**2 - discriminant)//(4*a))

    def __new__(self, a, b, c):
        return tuple.__new__(self, (a, b, c))

    def __init__(self, a, b, c):
        super(ClassGroup, self).__init__()
        self._discriminant = None

    def __mul__(self, other):
        return self.multiply(other)

    def __hash__(self):
        a, b, c = self.reduced()
        return hash((a, b, c))

    def identity(self):
        return self.identity_for_discriminant(self.discriminant())

    def discriminant(self):
        if self._discriminant is None:
            a, b, c = self
            self._discriminant = b * b - 4 * a * c
        return self._discriminant

    def reduced(self):
        a, b, c = self.normalized()
        while a > c or (a == c and b < 0):
            s = (c + b) // (c + c)
            a, b, c = c, -b + 2 * s * c, c * s * s - b * s + a
        return self.__class__(a, b, c).normalized()

    def normalized(self):
        a, b, c = self
        if -a < b <= a:
            return self
        r = (a - b) // (2 * a)
        b, c = b + 2 * r * a, a * r * r + b * r + c
        return self.__class__(a, b, c)

    def serialize(self):
        r = self.reduced()
        int_size_bits = int(self.discriminant().bit_length())
        int_size = (int_size_bits + 16) >> 4
        return b''.join([x.to_bytes(int_size, "big", signed=True)
                         for x in [r[0], r[1]]])

    def __eq__(self, other):
        return tuple(self.reduced()) == tuple(ClassGroup(*other).reduced())

    def __ne__(self, other):
        return not self.__eq__(other)

    def __pow__(self, n):
        if n == 0:
            return self.identity()
        a = self
        items_prod = None
        bits = bin(n)[2:]
        for i in range(len(bits) - 1, 0, -1):
            if bits[i] == "1":
                if not items_prod:
                    items_prod = a
                else:
                    items_prod = items_prod * a
            a *= a
        if items_prod:
            a = a * items_prod
        return a.reduced()

    def inverse(self):
        a, b, c = self
        return self.__class__(a, -b, c)

    def multiply(self, other):
        """
        An implementation of form composition as documented by Wikipedia.

        https://en.wikipedia.org/wiki/Binary_quadratic_form#Composition
        """

        a1, b1, c1 = self.reduced()
        a2, b2, c2 = other.reduced()

        discriminant = self.discriminant()

        b_mu = (b1 + b2) // 2
        e = mod.gcd(a1, a2, b_mu)
        a3 = (a1 * a2) // (e * e)

        u3 = b_mu // e
        v3 = (discriminant + b1 * b2) // (2 * e)
        w3 = 2 * a3
        gcd = mod.gcd(u3, v3, w3)
        u3, v3, w3 = u3 // gcd, v3 // gcd, w3 // gcd
        i3 = mod.inverse(u3, w3)
        v3 *= i3

        a_list = [b1, b2, v3]
        m_list = [2 * a1 // e, 2 * a2 // e, w3]

        b3 = mod.crt(a_list, m_list)
        c3 = (b3 * b3 - discriminant) // (4 * a3)
        return self.__class__(a3, b3, c3).reduced()

    def square(self):
        """
        A rewrite of multiply for squaring
        """

        a1, b1, c1 = self.reduced()

        discriminant = self.discriminant()

        e = mod.gcd(a1, b1)
        a3 = (a1 * a1) // (e * e)

        u3 = b1 // e
        v3 = (discriminant + b1 * b1) // (2 * e)
        w3 = 2 * a3
        gcd = mod.gcd(u3, v3, w3)
        u3, v3, w3 = u3 // gcd, v3 // gcd, w3 // gcd
        i3 = mod.inverse(u3, w3)
        v3 *= i3

        a_list = [b1, v3]
        m_list = [2 * a1 // e, w3]

        b3 = mod.crt(a_list, m_list)
        c3 = (b3 * b3 - discriminant) // (4 * a3)
        return self.__class__(a3, b3, c3).reduced()


"""
Copyright 2018 Chia Network Inc

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
