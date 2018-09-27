import unittest

from inkfish.classgroup import ClassGroup


class test_ClassGroup(unittest.TestCase):

    def test_paper_check(self):
        t12_11_3 = ClassGroup(12, 11, 3)
        t93_109_32 = ClassGroup(93, 109, 32)

        self.assertEqual(t12_11_3.discriminant(), -23)
        self.assertEqual(t93_109_32.discriminant(), -23)

        t = t12_11_3 * t93_109_32
        self.assertEqual(t, ClassGroup(1, -15, 62))
        self.assertEqual(t.discriminant(), -23)

        t1 = t93_109_32 * t12_11_3
        self.assertEqual(t, t1)

        # the normalize and reduce example from the paper
        f = ClassGroup(195751, 1212121, 1876411)
        self.assertEqual(f.normalized(), (195751, 37615, 1807))
        self.assertEqual(f.reduced(), (1, 1, 1))

    def test_generator_element(self):
        D = -103
        e_id = ClassGroup.identity_for_discriminant(D)
        self.assertEqual(e_id.discriminant(), D)
        self.assertEqual(e_id, (1, 1, 26))
        e = ClassGroup.from_ab_discriminant(2, 1, D)
        self.assertEqual(e.discriminant(), D)
        self.assertEqual(e, (2, 1, 13))
        e_inv = e.inverse()
        self.assertEqual(e_inv.discriminant(), D)
        self.assertEqual(e_inv, (2, -1, 13))
        self.assertEqual(e * e_inv, e_id)
        e2 = e.square()
        self.assertEqual(e2, (4, -3, 7))
        assert e2 == e * e
        e4 = e2.square()
        self.assertEqual(e4, (13, 1, 2))
        self.assertEqual(e4, e2 * e2)

    def test_many_generators(self):

        def all_powers(e):
            d = e.discriminant()
            e0 = e
            items = []
            while e0 not in items:
                items.append(e0)
                self.assertEqual(e0 * e0, e0.square())
                e0 *= e
                e0 = e0.normalized()
                if e0.discriminant() != d:
                    import pdb
                    pdb.set_trace()
            return items

        for _ in range(1000):
            D = -7 - _ * 8
            e_id = ClassGroup.identity_for_discriminant(D)
            self.assertEqual(e_id, (1, 1, 2 + 2 * _))
            e_id_inv = e_id.inverse()
            self.assertEqual(e_id, e_id_inv)
            e0 = ClassGroup.from_ab_discriminant(2, 1, D)
            e1 = e0.inverse()
            p0 = all_powers(e0)
            p1 = all_powers(e1)
            assert len(p0) == len(p1)
            assert e_id == p0[-1]
            assert e_id == p1[-1]
            for _0, _1 in zip(p0, p1):
                _ = _0 * _1
                assert _ == e_id
            print("discriminant = %d; group order = %d" % (D, len(p0)))

    def test_identity(self):
        for _ in range(1000):
            D = -7 - _ * 8
            e_id = ClassGroup.identity_for_discriminant(D)
            e_prod = e_id * e_id
            self.assertEqual(e_prod, e_id)

    def test_inverse(self):
        for _ in range(1000):
            D = -7 - _ * 8
            e_id = ClassGroup.identity_for_discriminant(D)
            e_gen = ClassGroup.from_ab_discriminant(2, 1, D)
            e_gen_inv = e_gen.inverse()
            e_prod = e_gen * e_gen_inv
            self.assertEqual(e_prod, e_id)

    def test_bad_multiply(self):
        n1 = ClassGroup(2243390248, -565721959, 35664920)
        n2 = ClassGroup(2, 1, 370)
        n = n1 * n2
        self.assertEqual(n.discriminant(), n1.discriminant())
        self.assertEqual(n.discriminant(), n2.discriminant())

    def test_pow(self):
        for _ in range(100):
            D = -7 - _ * 8
            e_gen = ClassGroup.from_ab_discriminant(2, 1, D)
            p = ClassGroup.identity_for_discriminant(D)
            for _ in range(10):
                self.assertEqual(pow(e_gen, _), p)
                p *= e_gen


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
