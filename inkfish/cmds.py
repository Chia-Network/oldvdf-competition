import argparse
import binascii
import sys

from inkfish.proof_of_time import (create_proof_of_time_large,
                                   create_proof_of_time_small,
                                   check_proof_of_time)

from .classgroup import ClassGroup
from .create_discriminant import create_discriminant


def create_pot_parser():
    parser = argparse.ArgumentParser(
        description='Generate or verify a proof of time using the Chia ' +
                    'Verfiable Delay Function (VDF)',
    )
    parser.add_argument("-s", "--small", action="store_true",
                        help="Indicate creation of a small proof.")
    parser.add_argument("-l", "--length", type=int, default=2048,
                        help="the number of bits of the discriminant")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="print a bunch of extra stuff about the proof")
    parser.add_argument("discriminant_challenge", type=binascii.unhexlify,
                        help="a hex-encoded challenge used to derive the discriminant")
    parser.add_argument("iterations", type=int,
                        help="number of iterations")
    parser.add_argument("proof", type=binascii.unhexlify,
                        help="the hex-encoded proof", nargs="?")
    return parser


def pot(args=sys.argv):
    parser = create_pot_parser()
    args = parser.parse_args(args=args[1:])

    discriminant = create_discriminant(args.discriminant_challenge)
    if args.verbose:
        print("discriminant: %s" % discriminant)

    generator = ClassGroup.from_ab_discriminant(2, 1, discriminant)
    if args.verbose:
        print("generator: %s" % str(generator))

    if args.proof:
        ok = check_proof_of_time(
            discriminant, generator, args.proof, args.iterations, args.length)
        if ok:
            print("Proof is valid")
        else:
            print("** INVALID PROOF")
            return -1
    else:
        if args.small:
            result, proof = create_proof_of_time_small(
                discriminant, generator, args.iterations, args.length)
        else:
            result, proof = create_proof_of_time_large(
                discriminant, generator, args.iterations, args.length)
        hex_result = binascii.hexlify(result).decode("utf8")
        hex_proof = binascii.hexlify(proof).decode("utf8")
        print(hex_result + hex_proof)


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
