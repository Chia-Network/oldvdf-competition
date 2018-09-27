from hashlib import sha256

from .primes import is_probable_prime, odd_primes_below_n


odd_primes = odd_primes_below_n(1 << 16)
sieve_info = [(p, pow(8, p-2, p)) for p in odd_primes]


def entropy_from_seed(seed, byte_count):
    blob = bytearray()
    extra = 0
    while len(blob) < byte_count:
        extra_bits = extra.to_bytes(2, "big")
        more_entropy = sha256(seed + extra_bits).digest()
        blob.extend(more_entropy)
        extra += 1
    return bytes(blob[:byte_count])


def create_discriminant(seed, length=2048):
    """
    Return a discriminant of the given length using the given seed.
    Generate a probable prime p where p % 8 == 7.
    Return -p.
    """
    entropy = entropy_from_seed(seed, length >> 3)
    n = int.from_bytes(entropy, 'big') | (1 << (length - 1)) | 7

    # Find the smallest prime >= n
    while True:
        # we set up "sieve" so it's "True" for known composite numbers
        sieve = [False] * (1 << 16)  # Store 8*i as i
        for p, q in sieve_info:
            # q = 8^-1 (mod p)
            # i = -n / 8, so that 8*i is -n (mod p).
            i = ((-n % p) * q) % p
            while i < len(sieve):
                sieve[i] = True
                i += p

        for i, x in enumerate(sieve):
            if not x and is_probable_prime(n + 8*i):
                return -(n + 8*i)
        n += 1 << 19


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
