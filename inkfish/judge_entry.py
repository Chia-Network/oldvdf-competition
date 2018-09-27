
from binascii import a2b_hex
from create_discriminant import create_discriminant
from classgroup import ClassGroup

def judge_entry(mystr):
    assert len(mystr) < 100000
    lines = mystr.strip().split('\n')
    assert len(lines) == 3
    ds = set()
    for line in lines:
        # challenge(in hex) length a b c order
        vals = [x.strip() for x in line.strip().split(b' ')]
        assert len(vals) == 6
        length = int(vals[1])
        assert length < 5000
        assert all(len(x) < length for x in vals[2:])
        assert len(vals[0]) == 8
        d = create_discriminant(a2b_hex(vals[0]), length)
        g = ClassGroup(int(line[2]), int(line[3]), int(line[4]))
        assert g.discriminant() == d
        assert g != g.identity()
        order = int(line[5])
        assert order > 1
        assert g ** order == g.identity()
        assert d not in ds
        ds.add(d)
    return min(ds)

if __name__ == '__main__':
    from sys import argv
    h = open(argv[1], 'rb')
    s = h.read()
    h.close()
    print(judge_entry(s))
