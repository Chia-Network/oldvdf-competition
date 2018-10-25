
from hashlib import sha256
from .create_discriminant import create_discriminant
from .classgroup import ClassGroup

def judge_entry(mystr):
    assert len(mystr) < 100000
    lines = mystr.strip().split('\n')
    assert len(lines) == 3
    ds = set()
    sha2=sha256()
    for line in lines:
        # challenge(in hex) length a b c order
        vals = [x.strip() for x in line.strip().split(' ')]
        assert len(vals) == 6
        length = int(vals[1])
        assert length < 5000
        assert all(len(x) < length for x in vals[2:])

        #assert len(vals[0]) == 8
        sha2.update(vals[0].encode('utf-8'))
        d = create_discriminant(sha2.digest(), length)
        g = ClassGroup(int(vals[2]), int(vals[3]), int(vals[4]))
        assert g.discriminant() == d
        assert g != g.identity()
        order = int(vals[5])
        assert order > 1
        assert g ** order == g.identity()
        assert d not in ds
        ds.add(d)
    return max(ds)

if __name__ == '__main__':
    from sys import argv
    h = open(argv[1], 'rb')
    s = h.read()
    h.close()
    print(judge_entry(s))
