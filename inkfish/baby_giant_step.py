import math
from itertools import *
from inkfish.classgroup import ClassGroup
from inkfish.create_discriminant import create_discriminant
from binascii import a2b_hex
import binascii
import os
import hashlib


def compute_order(g: ClassGroup) -> int:
    d = g.discriminant()
    quadRoot = int(math.sqrt(math.sqrt(-d)))
    size = quadRoot
    order = 0
    while order == 0:
        babylist = list(accumulate(repeat(g, quadRoot - 1), ClassGroup.multiply))
        babyset = set(babylist)
        gSqrt = (g ** quadRoot).normalized()
        bigStep = gSqrt
        result = next(filter(lambda giant: giant[1] in babyset,
                             accumulate(repeat((1, bigStep), size),
                                        lambda old, new: (old[0] + new[0], old[1] * new[1]))),
                      None)
        if result != None:
            order = (result[0] * quadRoot - babylist.index(result[1]) - 1)
            return order
        size = size * 2


if __name__ == '__main__':
    from sys import argv

    file = open(argv[1], 'w',encoding='utf-8')
    sha2=hashlib.sha256()
    for i in range(3):
        seed ="seed"+str(i)

        sha2.update(seed.encode('utf-8'))
        d = create_discriminant(sha2.digest(), 40)
        g = ClassGroup.from_ab_discriminant(2, 1, d)

        order = compute_order(g)

        c = (1 - d) // (4 * 2)
        arr = [seed, 40, 2,1, c, order]
        line = " ".join([str(x) for x in arr]) + '\n'
        file.write(line)
    file.close()
    from inkfish.judge_entry import judge_entry

    h = open(argv[1], 'r',encoding='utf-8')
    s = h.read()
    h.close()
    print(judge_entry(s))
