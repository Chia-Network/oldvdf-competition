import heapq
import math
import unittest

from inkfish import mod


def primes(max_value=None):
    yield 2
    heap = [(4, 2)]
    c = 2
    while max_value is None or c < max_value:
        c += 1
        n, p = heap[0]
        if n > c:
            yield c
            heapq.heappush(heap, (c+c, c))
        while n <= c:
            heapq.heapreplace(heap, (n+p, p))
            n, p = heap[0]


def primes_3_mod_4(max_value=None):
    for p in primes(max_value):
        if p & 3 == 3:
            yield p


class test_ModArithmetic(unittest.TestCase):

    def test_extended_gcd(self):
        for a in range(1, 1000, 3):
            for b in range(1, 1000, 5):
                r, s, t = mod.extended_gcd(a, b)
                self.assertEqual(r, math.gcd(a, b))
                self.assertEqual(r, a * s + b * t)

    def test_inverse(self):
        for p in primes(1000):
            for a in range(1, p-1):
                v = mod.inverse(a, p)
                self.assertEqual(a * v % p, 1)

    def test_reduce_equivalencies_rp(self):
        for a0, m0, a1, m1 in ((2, 5, 1, 2), (1, 6, 7, 10), (1, 6, 2, 10)):
            a, m, works = mod.reduce_equivalencies(a0, m0, a1, m1)
            self.assertEqual(m, m0 * m1 // math.gcd(m0, m1))
            if works:
                self.assertEqual(a % m0, a0)
                self.assertEqual(a % m1, a1)

    def test_crt(self):
        for a_list, m_list in [([2, 6], [14, 18]), ([1, 3, 5, 7],
                                                    [3, 7, 11, 109])]:
            v = mod.crt(a_list, m_list)
            for a, m in zip(a_list, m_list):
                self.assertEqual(v % m, a)

    def test_square_root_mod_p(self):
        for p in primes_3_mod_4(1000):
            for a in range(1, p):
                for t in mod.square_root_mod_p(a, p):
                    self.assertEqual(t * t % p, a)

    def test_square_root_mod_p_list(self):
        for p0 in primes_3_mod_4(10):
            for p1 in primes_3_mod_4(100):
                if p1 <= p0:
                    continue
                for p2 in primes_3_mod_4(100):
                    if p2 <= p1:
                        continue
                    prod = p0 * p1 * p2
                    for a in range(1, prod):
                        for t in mod.square_root_mod_p_list(a, [p0, p1, p2]):
                            print(a, prod, t, t*t % prod)
                            self.assertEqual(t * t % prod, a)

    def test_solve_mod(self):

        def check(a, b, c):
            r, s = mod.solve_mod(a, b, c)
            b %= c
            for k in range(50):
                a_coefficient = r + s * k
                self.assertEqual((a_coefficient * a) % c, b)

        check(3, 4, 5)
        check(6, 8, 10)
        check(12, 30, 7)
        check(6, 15, 411)
        check(192, 193, 863)
        check(-565721958, 740, 4486780496)
        check(565721958, 740, 4486780496)
        check(-565721958, -740, 4486780496)
        check(565721958, -740, 4486780496)

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
