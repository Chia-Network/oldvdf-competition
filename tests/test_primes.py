import heapq
import unittest

from inkfish import primes


def prime_iter(max_value=None):
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


class test_Primes(unittest.TestCase):

    def test_odd_primes_below_n(self):
        p1 = primes.odd_primes_below_n(15000)
        self.assertEqual(p1, list(prime_iter(15000))[1:])

    def test_miller_rabin_test(self):
        p1 = primes.odd_primes_below_n(25000)
        for p in p1:
            mr = primes.miller_rabin_test(p)
            self.assertTrue(mr)
        for p in range(3, 25000):
            mr = primes.miller_rabin_test(p)
            self.assertEqual(mr, p in p1)
