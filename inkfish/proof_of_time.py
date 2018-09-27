import hashlib
import math

from .classgroup import ClassGroup
from .iterate_squarings import iterate_squarings
from .large_proof import generate_large_proof, verify_large_proof, cache_indeces_for_count
from .small_proof import generate_small_proof, verify_small_proof, approximate_parameters


def generate_r_value(x, y, sqrt_mu, int_size_bits):
    """creates an r value by hashing the inputs"""
    if isinstance(x, ClassGroup):
        s = serialize_proof([x, y, sqrt_mu])
    else:
        int_size = int_size_bits // 8
        s = (x.to_bytes(int_size, "big", signed=False) +
             y.to_bytes(int_size, "big", signed=False) +
             sqrt_mu.to_bytes(int_size, "big", signed=False))
    b = hashlib.sha256(s).digest()
    return int.from_bytes(b[:16], "big")


def serialize_proof(proof):
    return b''.join(el.serialize() for el in proof)


def deserialize_proof(proof_blob,  discriminant):
    int_size = (discriminant.bit_length() + 16) >> 4
    proof_arr = [proof_blob[_:_ + 2 * int_size]
                 for _ in range(0, len(proof_blob), 2*int_size)]
    return [ClassGroup.from_bytes(blob, discriminant) for blob in proof_arr]


def create_proof_of_time_large(discriminant, generator, iterations, int_size_bits):
    """
    Returns a serialized proof blob.
    """
    delta = 8

    powers_to_calculate = cache_indeces_for_count(iterations)
    powers = iterate_squarings(generator, powers_to_calculate)
    y = powers[iterations]
    proof = generate_large_proof(generator, iterations, delta, y, powers,
                                 lambda a: a.reduced(), generator.identity(),
                                 generate_r_value, int_size_bits)

    return y.serialize(), serialize_proof(proof)


def create_proof_of_time_small(discriminant, generator, iterations, int_size_bits):
    L, k = approximate_parameters(iterations)

    powers_to_calculate = [i * k * L for i in range(0, math.ceil(iterations/(k*L)) + 1)]
    powers_to_calculate += [iterations]
    powers = iterate_squarings(generator, powers_to_calculate)

    y = powers[iterations]
    identity = ClassGroup.identity_for_discriminant(discriminant)
    proof = generate_small_proof(identity, generator, y, iterations, k, L, powers)
    return y.serialize(), serialize_proof([proof])


def check_proof_of_time(discriminant, generator, proof_blob, iterations, int_size_bits):
    # we add one bit for sign, then 15 bits to round up to the next word
    # BRAIN DAMAGE: can we round to a byte instead of a word?
    int_size = (int_size_bits + 16) >> 4
    result_bytes = proof_blob[: (2 * int_size)]
    proof_bytes = proof_blob[(2 * int_size):]

    proof = deserialize_proof(proof_bytes, discriminant)

    y = ClassGroup.from_bytes(result_bytes, discriminant)
    try:
        if len(proof) == 1:
            return verify_small_proof(generator, y, proof[0], iterations)
        else:
            return verify_large_proof(generator, y, proof, iterations, 8,
                                      lambda a: a.reduced(), generate_r_value,
                                      int_size_bits)
    except Exception:
        return False


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
