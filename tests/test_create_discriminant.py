import unittest

from inkfish.create_discriminant import create_discriminant
from inkfish.primes import odd_primes_below_n


class test_generate_prime(unittest.TestCase):

    def test_primes(self):
        actual_value = odd_primes_below_n(256)
        self.assertEqual(actual_value, [
            3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67,
            71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139,
            149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211,
            223, 227, 229, 233, 239, 241, 251
        ])

    def test_known_prime_foo(self):
        prime_foo = -int(
            "0xe5410e122e8cb95583522f57ec7b807177ff1dc53a7ac5c1fa8c3ee63a8a7298e019"
            "4e2048fd130bcebab490427195559a16b67640075770dd27d9fe5d6f9a27c186c3d161"
            "cb277d4f68ce6dc801355b44b472eb39902b7fd717da6e0b43ef9ae64bc49055a21cec"
            "72076359d2d9d754f1bfbb29070ed0cccdb04d8b4622148ad90b3e0779ecfef5f2b299"
            "b039f8e744a99322afef1de7df4dc7165c464a989e103ec27888ca883095bcffe9f6f4"
            "88d790488b98e2d7ccbeb081de5dd3a26be509cf58d632861671195e7daf29ebf81a13"
            "59a66f22c7a9ecd96a693889177be471298d33bb031d0643b591611ac4b20c12858c35"
            "1fa8d29057c8cca877f70e07", 16
        )
        v = create_discriminant(b"foo", 2048)
        self.assertEqual(v, prime_foo)

    def test_known_prime_bar(self):
        prime_bar = -int(
            "0xac8e36c9233c59b94a7d340a90b15533064db1cb8de6e083c3128d8d091ca9eb01fb"
            "ce233d5eb801f71d98a480b413c943d84e9f36ad2ced7928a7288db0d60db14e7a9cbd"
            "53515476344b42bfa2e0d9a35f9cfb6a7a66ba0ebab829b6a71fabf1b202878fed608f"
            "7d6241c27f7efc11b485df7e0b4955404d9be05cf7eaa50d1cd11c170a99767ad5ad63"
            "f6e30fa8e3b3d88a03364a9c403e0609e74f15888d9d91ec9aef5bd2bcab90063eb0d6"
            "001e61a0c374c8d2626ffab951048573ea15da531c4dacf2218139715414cf5828dd10"
            "1b23c01fbafffde1f109780d123673f8b23e41495fa8bbb5b36f39f8d9693835036445"
            "075fbb770554a352ec32c757", 16
        )
        v = create_discriminant(b"bar", 2048)
        self.assertEqual(v, prime_bar)


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
