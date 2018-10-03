import hashlib
import math

from .primes import is_probable_prime


def approximate_parameters(T):
    """
    Creates L and k parameters from papers, based on how many iterations need to be
    performed, and how much memory should be used.
    """
    log_memory = math.log(10000000, 2)

    # For low number of iterations, we can just set L to 1 and we will
    # have enough memory. For high Ts, we can limit memory usage
    L = 1
    if (math.log(T, 2) - log_memory > 0):
        L = math.ceil(pow(2, log_memory - 20))

    # Total time for proof: T/k + L * 2^(k+1)
    # To optimize, set left equal to right, and solve for k
    # k = W(T * log(2) / (2 * L))  / log(2), where W is the product log function
    # W can be approximated by log(x) - log(log(x)) + 0.25
    intermediate = T * math.log(2) / (2 * L)
    k = max([round(math.log(intermediate) - math.log(math.log(intermediate)) + 0.25), 1])
    return (L, k)


def hash_prime(s):
    """
    Creates a random prime based on input s.
    """
    j = 0
    while True:
        h_input = b"prime" + j.to_bytes(8, "big", signed=False) + s
        h_output = hashlib.sha256(h_input).digest()
        n = int.from_bytes(h_output[:16], "big")
        if is_probable_prime(n):
            return n
        j += 1


def get_block(i, k, T, B):
    """
    Get's the ith block of  2^T // B, such that sum(get_block(i) * 2^ki) =
    t^T // B
    """
    return (pow(2, k) * pow(2, T - k * (i + 1), B)) // B


def eval_optimized(identity, h, B, T, k, l, C):
    """
    Optimized evalutation of h ^ (2^T // B)
    """
    k1 = k//2
    k0 = k - k1
    x = identity

    for j in range(l-1, -1, -1):
        x = pow(x, pow(2, k))
        ys = {}
        b_limit = pow(2, k)
        for b in range(0, b_limit):
            ys[b] = identity
        for i in range(0, math.ceil((T)/(k*l))):
            if (T - k * (i*l + j + 1) < 0):
                continue
            b = get_block(i*l + j, k, T, B)
            ys[b] = ys[b] * C[i * k * l]

        for b1 in range(0, pow(2, k1)):
            z = identity
            for b0 in range(0, pow(2, k0)):
                z *= ys[b1 * pow(2, k0) + b0]
            x *= pow(z, b1 * pow(2, k0))

        for b0 in range(0, pow(2, k0)):
            z = identity
            for b1 in range(0, pow(2, k1)):
                z *= ys[b1 * pow(2, k0) + b0]
            x *= pow(z, b0)
    return x


def generate_small_proof(identity, x, y, T, k, l, C):
    """
    Proof construction from Wesolowski paper
    """
    B = hash_prime(x.serialize() + y.serialize())
    return eval_optimized(identity, x, B, T, k, l, C)


def verify_small_proof(x, y, proof, T):
    """
    Verification from Wesolowski paper
    """
    B = hash_prime(x.serialize() + y.serialize())
    r = pow(2, T, B)
    return pow(proof, B) * pow(x, r) == y


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
