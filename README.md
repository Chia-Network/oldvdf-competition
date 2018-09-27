This is an in-development version of the Chia Network proof-of-time verifiable delay function "inkfish".

An optional install is `gmpy2` to potentially speed up primality testing.

On a Mac, run

    $ brew install gmp libmpc


Set up your virtual environments:

    $ python3 -m venv env
    $ ln -s env/bin/activate
    $ . ./activate
    $ pip install -e .

Check out the command-line tools:

    $ pot -h

Generate a proof of time.

    $ pot deadbeef 1000

Generate a small proof of time.

    $ pot -s deadbeef 1000

Verify a proof of time.

    $ pot deadbeef 1000 <proof>


The verifiable delay function used is the iterated squarings / RSA timelock construction. The code implements both RSA and classgroup settings for this.

Furthermore, there are two proof approaches implemented here
1. The [first one](https://eprint.iacr.org/2018/627.pdf) by Krzysztof Pietrzak, that is fast to create, but large and slow to verify.
2. The [second one](https://eprint.iacr.org/2018/623.pdf) by Benjamin Wesolowski which is slower to create (but parallelizable), but small, and quick to verify.

Both approaches are summarized in [this survey paper](https://eprint.iacr.org/2018/712.pdf) by Boneh, Bünz, and Fisch.
