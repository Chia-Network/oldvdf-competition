import time
import math

from inkfish.iterate_squarings import iterate_squarings
from inkfish import proof_wesolowski
from inkfish import proof_pietrzak
from inkfish.proof_of_time import generate_r_value


def exercise_code_verbosely(group_functions):
    # Perform T squarings, can be any even number
    # T = 500k approx= 2 ** 19
    T = 10000

    # This denotes the number of rounds to skip, at the end. This
    # reduces proof size, but setting it too large, will slow down
    # verification. delta is 8 in the paper
    delta = 8

    # T = k * l * 2^k
    L, k, w = proof_wesolowski.approximate_parameters(T)
    print("Using L: ", L, " k: ", k, " and w:", w)

    x, identity, element_size_bytes, int_size_bits = group_functions()

    print("Starting to compute the VDF...")
    start_t = time.time() * 1000
    powers_to_calculate = proof_pietrzak.cache_indeces_for_count(T)
    powers_to_calculate_small = [i * k * L for i in range(0, math.ceil(T/(k*L)) + 1)]
    powers_to_calculate += powers_to_calculate_small
    powers_raw = iterate_squarings(x, powers_to_calculate)
    powers = {k: powers_raw[k] for k in powers_raw if k in powers_to_calculate}
    powers_small = {k: powers_raw[k] for k in powers_raw if k in powers_to_calculate_small}
    y = powers[T]
    print("Finished computing VDF in", round(((time.time() * 1000) - start_t)
          / 1000, 2), "seconds")
    print("Storing", len(powers), "Items in cache, total", (len(powers)*32)
          / (1024), "KB of RAM")

    print("y = %s" % str(y))

    print("")
    print("Starting to compute the large proof...")
    start_t = time.time() * 1000
    proof = proof_pietrzak.generate_proof(x, T, delta, y, powers, identity,
                                          generate_r_value, int_size_bits)
    print("Finished computing large proof in", round(((time.time() * 1000)
                                                     - start_t), 2), "ms")
    print("Proof size: %.2f KB" % (len(proof) * element_size_bytes / 1024.0))
    print("Large proof: %s" % str(proof))

    print("")
    print("Starting to compute the small proof...")
    start_t = time.time() * 1000
    small_proof = proof_wesolowski.generate_proof(identity, x, y, T, k, L, powers_small)
    print("Proof size: %.2f KB" % (element_size_bytes / 1024.0))
    print("Finished computing small proof in", round(((time.time() * 1000)
                                                     - start_t), 2), "ms")
    print("Small proof: %s" % str(small_proof))

    print("")
    print("Starting to verify the large proof...")
    start_t = time.time() * 1000
    ok = proof_pietrzak.verify_proof(x, y, proof, T, delta,
                                     generate_r_value, int_size_bits)
    assert ok
    print("Finished verifying large proof in", round(((time.time() * 1000)
                                                      - start_t), 2), "ms")

    print("")
    print("Starting to verify the small proof...")
    start_t = time.time() * 1000
    ok2 = proof_wesolowski.verify_proof(x, y, small_proof, T)
    assert(ok2)
    print("Finished verifying small proof in", round(((time.time() * 1000)
                                                     - start_t), 2), "ms")


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
