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

---
ENTRY FORM: 

By providing your legal first and last names, street address, city, zip code, daytime and home phone number, email address, and agreement to the [VDF Contest Challenge Rules and Disclosures](https://www.dropbox.com/s/7c9y6802cdx0hne/Chia%20Network%20-%20VDF%20Contest%20Rules%20and%20Disclosures?dl=0), and  along with the source code and documentation meeting the Entry Specifications described in the VDF Contest Challenge Rules and Disclosures agreement above (specifically the “Technical Submission”) to [Chia's public Keybase group](https://keybase.io/team/chia_network.public) the judges create to communicate with your team using a keybase shared git repo.

The Entry Form and Technical Submission together are considered the entry (“Entry”). An Entry is not complete and will not be considered if either portion is missing. 

An Entry may be submitted by a team of individuals working collaboratively (a “Team Contestant”), in which case, each individual member of the team must complete the Entry Form as described above and all members of the Team Contestant must designate the same point of contact to receive official Challenge correspondence.

ENTRY FORM REQUIREMENTS:

First Name(s): 
Last Name(s): 
street address(es):
City(ies)
Zip Code(s):
Phone number(s): 
Email address(es):

Signed version of the [VDF Contest Challenge Rules and Disclosures](https://www.dropbox.com/s/7c9y6802cdx0hne/Chia%20Network%20-%20VDF%20Contest%20Rules%20and%20Disclosures?dl=0)

Source code and documentation meeting the Entry Specifications described in the [VDF Contest Challenge Rules and Disclosures](https://www.dropbox.com/s/7c9y6802cdx0hne/Chia%20Network%20-%20VDF%20Contest%20Rules%20and%20Disclosures?dl=0) agreement specific to the “Technical Submission”

