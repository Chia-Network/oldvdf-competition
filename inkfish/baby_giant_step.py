from itertools import *
from inkfish.classgroup import ClassGroup
from inkfish.create_discriminant import create_discriminant
from binascii import b2a_hex


def compute_order(g: ClassGroup) -> int:
    d = g.discriminant()
    quadRoot = int((-d) ** 0.25)
    size = quadRoot
    order = 0
    while order == 0:
        babylist = list(accumulate(repeat(g, quadRoot - 1), ClassGroup.multiply))
        babyset = set(babylist)
        gSqrt = (g ** quadRoot).normalized()
        bigStep = gSqrt
        result = next(filter(lambda giant: giant[1] in babyset,
                accumulate(repeat((1, bigStep), size),
                lambda old, new: (old[0] + new[0], old[1] * new[1]))), None)
        if result != None:
            order = (result[0] * quadRoot - babylist.index(result[1]) - 1)
            return order
        size *= 2


def print_entry(length):
    for i in range(3):
        seed = int.to_bytes(i, 4, 'big')

        d = create_discriminant(seed, length)
        g = ClassGroup.from_ab_discriminant(2, 1, d)

        order = compute_order(g)

        c = (1 - d) // (4 * 2)
        print('%s %i %i %i %i %i' % (b2a_hex(seed).decode('latin-1'), length, 2, 1, c, order))

if __name__ == '__main__':
    from sys import argv
    print_entry(int(argv[1]))
