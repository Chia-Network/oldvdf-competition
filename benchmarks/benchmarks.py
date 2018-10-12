import time
import textwrap
import math
import binascii

from inkfish.create_discriminant import create_discriminant
from inkfish.classgroup import ClassGroup
from inkfish.iterate_squarings import iterate_squarings
from inkfish import proof_wesolowski
from inkfish.proof_of_time import (create_proof_of_time_nwesolowski,
                                   check_proof_of_time_nwesolowski,
                                   generate_r_value)
from inkfish import proof_pietrzak

from tests.int_mod_n import int_mod_n


start_t = 0
time_multiplier = 1000  # Use milliseconds


def start_bench():
    global start_t
    start_t = time.time() * time_multiplier


def end_bench(name, iterations):
    global start_t
    print("%-80s" % name, round(((time.time() * time_multiplier) - start_t)
          / (iterations), 2), "ms")


def bench_classgroup():
    D = create_discriminant(b"seed", 1024)
    g = ClassGroup.from_ab_discriminant(2, 1, D)
    while g[0].bit_length() < g[2].bit_length() or g[0].bit_length() < g[2].bit_length():
        g = pow(g, 2)
    g2 = pow(g, 2)
    start_bench()
    for _ in range(0, 10000):
        g2 = g2.multiply(g)
    end_bench("Classgroup 1024 bit multiply", 10000)

    start_bench()
    for _ in range(0, 10000):
        g2 = g2.square()
    end_bench("Classgroup 1024 bit square", 10000)

    D = create_discriminant(b"seed", 2048)
    g = ClassGroup.from_ab_discriminant(2, 1, D)
    while g[0].bit_length() < g[2].bit_length() or g[0].bit_length() < g[2].bit_length():
        g = pow(g, 2)

    g2 = pow(g, 2)

    start_bench()
    for _ in range(0, 10000):
        g2 = g2.multiply(g)
    end_bench("Classgroup 2048 bit multiply", 10000)

    start_bench()
    for _ in range(0, 10000):
        g2 = g2.square()
    end_bench("Classgroup 2048 bit square", 10000)


def bench_discriminant_generation():
    start_bench()
    for i in range(10):
        create_discriminant(i.to_bytes(32, "big"), 1024)
    end_bench("Generate 1024 bit discriminant", 10)

    start_bench()
    for i in range(10):
        create_discriminant(i.to_bytes(32, "big"), 2048)
    end_bench("Generate 2048 bit discriminant", 10)


def bench_vdf_iterations():
    D = create_discriminant(b"seed", 512)
    g = ClassGroup.from_ab_discriminant(2, 1, D)

    start_bench()
    for _ in range(10):
        iterate_squarings(g, [10000])
    end_bench("VDF 10000 iterations, 512bit classgroup", 10)

    D = create_discriminant(b"seed", 1024)
    g = ClassGroup.from_ab_discriminant(2, 1, D)

    start_bench()
    for _ in range(2):
        iterate_squarings(g, [10000])
    end_bench("VDF 10000 iterations, 1024bit classgroup", 2)

    D = create_discriminant(b"seed", 2048)
    g = ClassGroup.from_ab_discriminant(2, 1, D)
    start_bench()
    for _ in range(2):
        iterate_squarings(g, [10000])
    end_bench("VDF 10000 iterations, 2048bit classgroup", 2)

    # 2048 bit modulus
    prime = int(''.join(textwrap.dedent("""
        2634427397878110232503205795695468045251992992603340168049253044454387
        1080897872360133472596339100961569230393163880927301060812730934043766
        3646941725034559080490451986171041751558689035115943134790395616490035
        9846986660803055891526943083539429058955074960014718229954545667371414
        8029627597753998530121193913181474174423003742206534823264658175666814
        0135440982296559552013264268674093709650866928458407571602481922443634
        2306826340229149641664159565679297958087282612514993965471602016939198
        7906354607787482381087158402527243744342654041944357821920600344804411
        149211019651477131981627171025001255607692340155184929729""").split(
            "\n")))
    initial_x = int_mod_n(15619920774592561628351138998371642294622340518469892832433140464182509560910157, prime)
    start_bench()
    for _ in range(2):
        iterate_squarings(initial_x, [10000])
    end_bench("VDF 10000 iterations, 2048bit RSA modulus", 2)

    # 4096 bit modulus
    prime = int(''.join(textwrap.dedent("""
        8466908771297228398108729385413406312941234872779790501232479567685076
        4762372651919166693555570188656362906279057098994287649807661604067499
        3053172889374223358861501556862285892231110003666671700028271837785598
        2711897721600334848186874197010418494909265899320941516493102418008649
        1453168421248338831347183727052419170386543046753155080120058844782449
        2367606252473029574371603403502901208633055707823115620627698680602710
        8443465519855901353485395338769455628849759950055397510380800451786140
        7656499749760023191493764704430968335226478156774628814806959050849093
        5035645687560103462845054697907307302184358040130405297282437884344166
        7188530230135000709764482573583664708281017375197388209508666190855611
        3020636147999796942848529907410787587958203267319164458728792653638371
        7065019972034334447374200594285558460255762459285837794285154075321806
        4811493971019446075650166775528463987738853022894781860563097254152754
        1001763544907553312158598519824602240430350073539728131177239628816329
        0179188493240741373702361870220590386302554494325819514615309801491107
        2710093592877658471507118356670261129465668437063636041245619411937902
        0658733974883998301959084381087966405508661151837877497650143949507846
        1522640311670422105209760172585337397687461""").split("\n")))

    initial_x = int_mod_n(15619920774592561628351138998371642294622340518469892832433140464182509560910157, prime)
    start_bench()
    for _ in range(2):
        iterate_squarings(initial_x, [10000])
    end_bench("VDF 10000 iterations, 4096bit RSA modulus", 2)


def bench_wesolowski():
    iterations = 10000
    discriminant_length = 512
    discriminant = create_discriminant(b"seed", discriminant_length)
    L, k, _ = proof_wesolowski.approximate_parameters(iterations)

    x = ClassGroup.from_ab_discriminant(2, 1, discriminant)
    powers_to_calculate = [i * k * L for i in range(0, math.ceil(iterations/(k*L)) + 1)]
    powers_to_calculate += [iterations]
    start_t = time.time() * time_multiplier
    powers = iterate_squarings(x, powers_to_calculate)
    vdf_time = round(time.time() * time_multiplier - start_t)

    y = powers[iterations]
    identity = ClassGroup.identity_for_discriminant(discriminant)

    start_t = time.time() * time_multiplier
    start_bench()
    for _ in range(5):
        proof = proof_wesolowski.generate_proof(identity, x, y, iterations, k, L, powers)
    end_bench("Wesolowski  " + str(discriminant_length) + "b class group, " + str(iterations)
              + " iterations, proof", 5)
    proof_time = round((time.time() * time_multiplier - start_t) / 5)
    print("    - Percentage of VDF time:", (proof_time / vdf_time) * 100, "%")

    start_bench()
    for _ in range(10):
        assert(proof_wesolowski.verify_proof(x, y, proof, iterations))
    end_bench("Wesolowski " + str(discriminant_length) + "b class group, " + str(iterations)
              + " iterations, verification", 10)


def bench_nwesolowski():
    iterations = 10000
    discriminant_length = 512
    discriminant = create_discriminant(b"seed", discriminant_length)
    L, k, _ = proof_wesolowski.approximate_parameters(iterations)

    x = ClassGroup.from_ab_discriminant(2, 1, discriminant)
    powers_to_calculate = [i * k * L for i in range(0, math.ceil(iterations/(k*L)) + 1)]

    start_t = time.time() * time_multiplier
    for _ in range(20):
        iterate_squarings(x, powers_to_calculate)
    vdf_time = round(time.time() * time_multiplier - start_t) / 20

    start_t = time.time() * time_multiplier
    start_bench()
    for _ in range(20):
        result, proof = create_proof_of_time_nwesolowski(discriminant, x, iterations,
                                                         discriminant_length, 2, depth=0)
    end_bench("n-wesolowski depth 2 " + str(discriminant_length) + "b class group, "
              + str(iterations) + " iterations, proof", 20)
    proof_time = round((time.time() * time_multiplier - start_t) / 20)
    print("    - Percentage of VDF time:", (((proof_time - vdf_time) / vdf_time) * 100), "%")

    start_bench()
    for _ in range(20):
        assert(check_proof_of_time_nwesolowski(discriminant, x, result + proof, iterations, discriminant_length))
    end_bench("n-wesolowski depth 2 " + str(discriminant_length) + "b class group, "
              + str(iterations) + " iterations, verification", 20)


def bench_pietrzak():
    iterations = 10000
    discriminant_length = 512
    discriminant = create_discriminant(b"seed", discriminant_length)
    delta = 8

    x = ClassGroup.from_ab_discriminant(2, 1, discriminant)
    powers_to_calculate = proof_pietrzak.cache_indeces_for_count(iterations)
    start_t = time.time() * time_multiplier
    powers = iterate_squarings(x, powers_to_calculate)
    vdf_time = round(time.time() * time_multiplier - start_t)

    y = powers[iterations]
    identity = ClassGroup.identity_for_discriminant(discriminant)

    start_t = time.time() * time_multiplier
    start_bench()
    for _ in range(5):
        proof = proof_pietrzak.generate_proof(x, iterations, delta, y, powers,
                                              identity, generate_r_value, discriminant_length)
    end_bench("Pietrzak  " + str(discriminant_length) + "b class group, " + str(iterations)
              + " iterations, proof", 10)
    proof_time = round((time.time() * time_multiplier - start_t) / 10)
    print("    - Percentage of VDF time:", (proof_time / vdf_time) * 100, "%")

    start_bench()
    for _ in range(10):
        assert(proof_pietrzak.verify_proof(x, y, proof, iterations, delta,
                                           generate_r_value, discriminant_length))
    end_bench("Pietrzak " + str(discriminant_length) + "b class group, " + str(iterations)
              + " iterations, verification", 10)


def bench_main():
    bench_classgroup()
    bench_discriminant_generation()
    bench_vdf_iterations()
    bench_wesolowski()
    bench_nwesolowski()
    bench_pietrzak()


if __name__ == '__main__':
    bench_main()


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

