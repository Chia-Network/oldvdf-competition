# Chia VDF competition and implementation

In an attempt to create a secure, fast, open, decentralized consensus algorithm, Chia is hosting a 3-month competition for the implementation of verifiable delay functions.  Below, we provide links to relevant research papers and a summary of the competition requirements.

This repository contains an in-development version of the Chia Network proof-of-time verifiable delay function "inkfish".  The verifiable delay function used is the iterated squarings / RSA timelock construction. The code implements both RSA and classgroup settings for this.

Two proof approaches are implemented here:
1. The [first one](https://eprint.iacr.org/2018/627.pdf) by Krzysztof Pietrzak is fast to create but large and slow to verify.
2. The [second one](https://eprint.iacr.org/2018/623.pdf) by Benjamin Wesolowski, though parallelizable, is slower to create but small and quick to verify.

Both approaches are summarized in [this survey paper](https://eprint.iacr.org/2018/712.pdf) by Boneh, Bünz, and Fisch.

We have an explanation of class groups and binary quadratic forms [here](https://www.dropbox.com/s/aqupbohwj08s1q3/bqf%20%281%29.pdf?dl=0).

Want to learn more? Join [Chia's public Keybase group](https://keybase.io/team/chia_network.public) or read Chia's [reddit](https://www.reddit.com/r/chia_vdf).

---
## Competition Entry

The Entry Form and Technical Submission together are considered the entry (“Entry”). An Entry is not complete and will not be considered if either portion is missing.

Enter by providing your legal first and last names, street address, city, zipcode, daytime and home phone number, email address, and agreement of entry to the [VDF Contest Challenge Rules and Disclosures agreement](https://www.dropbox.com/s/46b92qfvrxw8jzp/Chia%20Network%20-%20VDF%20Contest%20Rules%20and%20Disclosures%20%284%29.pdf?dl=0),  along with the source code and documentation meeting the Entry Specifications described in the VDF Contest Challenge Rules and Disclosures agreement above (specifically the “Technical Submission”) to [Chia's public Keybase group](https://keybase.io/team/chia_network.public). The judges will communicate with your team using a keybase shared git repo.

An Entry may be submitted by a team of individuals working collaboratively (a “Team Contestant”), in which case, each individual member of the team must complete the Entry Form as described above and all members of the Team Contestant must designate the same point of contact to receive official Competition correspondence.

### Entry Requirements

1. Completed version of the [Entry Form](https://www.dropbox.com/s/odsglm1eu9z6g8v/CHIA%20NETWORK%20APPLICATION%20FORM%204812-8893-1439%20v.1.pdf?dl=0).

2. Signed version of the [VDF Contest Challenge Rules and Disclosures agreement](https://www.dropbox.com/s/46b92qfvrxw8jzp/Chia%20Network%20-%20VDF%20Contest%20Rules%20and%20Disclosures%20%284%29.pdf?dl=0)

3. Source code and documentation meeting the Entry Specifications described in the [VDF Contest Challenge Rules and Disclosures agreement](https://www.dropbox.com/s/46b92qfvrxw8jzp/Chia%20Network%20-%20VDF%20Contest%20Rules%20and%20Disclosures%20%284%29.pdf?dl=0) specific to the Technical Submission Guidelines (outlined below).

### Technical Submission Guidelines

1. All source code and documentation in an Entry must be made and submitted pursuant to the terms of the Apache or MIT License. The Apache Licence and instructions for applying it can be found [here](https://www.apache.org/licenses/LICENSE-2.0). The MIT License and instructions for applying it can be found [here](https://opensource.org/licenses/MIT).

2. In the Fastest VDF Implementation category, code must be produced that will solve a VDF at a given number of iterations and security difficulty on the reference hardware. The [repeated squarings VDF](https://eprint.iacr.org/2018/623.pdf) should be used, but we do not require computation of a proof, and only the speed of computation of the output will be judged. The VDF should be computed in the classgroup setting, and should output the same as our sample code above (see classgroup.py for naive implementation of classgroups). The number of iterations and security difficulty will be provided at least 2 months before the end of the contest, and will be announced on the reddit and the keybase channel.

3. In the Best Discriminant Break category, the judging criteria is the file which gives the best number output from judge_entry.py. The entry needs to have three values, each specifying which of our allowed discriminants it's on, and giving an element of the group and its order for each. The smallest of the three discriminants is the quality, and the greatest quality entry wins. The current discriminants are ones which have a four-byte challenge to create_discriminant().

4. The Contestant, or each member of a Team Contestant, must certify that the entire contents of the Technical Submission is the sole work of the Contestant, or collective work of the members of the Team Contestant, except to the extent that the Entry incorporates content that is publicly available or covered by an Apache or MIT license (and is properly identified as such) and that the Contestant has all legal rights necessary to grant the license granted in guideline (1) above.

5. Each Entry must be submitted with a Readme file that completes the entry form and describes in English the methods used in the software.
---

## VDF Python implementation

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

To see some benchmarks, run

    $ python3 tests/test_classgroup_vdf.py
