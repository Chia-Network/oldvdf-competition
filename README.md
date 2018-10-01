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
## ENTRY FORM 

By providing your legal first and last names, street address, city, zip code, daytime and home phone number, email address, and agreement to the [VDF Contest Challenge Rules and Disclosures](https://www.dropbox.com/s/7c9y6802cdx0hne/Chia%20Network%20-%20VDF%20Contest%20Rules%20and%20Disclosures?dl=0), and  along with the source code and documentation meeting the Entry Specifications described in the VDF Contest Challenge Rules and Disclosures agreement above (specifically the “Technical Submission”) to [Chia's public Keybase group](https://keybase.io/team/chia_network.public) the judges create to communicate with your team using a keybase shared git repo.

The Entry Form and Technical Submission together are considered the entry (“Entry”). An Entry is not complete and will not be considered if either portion is missing. 

An Entry may be submitted by a team of individuals working collaboratively (a “Team Contestant”), in which case, each individual member of the team must complete the Entry Form as described above and all members of the Team Contestant must designate the same point of contact to receive official Challenge correspondence.

### ENTRY FORM REQUIREMENTS

1. Contact Information: 
- First Name(s): 
- Last Name(s): 
- Street Address(es):
- City(ies)
- Zip Code(s):
- Phone number(s): 
- Email address(es):

2. Signed version of the [VDF Contest Challenge Rules and Disclosures](https://www.dropbox.com/s/7c9y6802cdx0hne/Chia%20Network%20-%20VDF%20Contest%20Rules%20and%20Disclosures?dl=0)

3. Source code and documentation meeting the Entry Specifications described in the [VDF Contest Challenge Rules and Disclosures](https://www.dropbox.com/s/7c9y6802cdx0hne/Chia%20Network%20-%20VDF%20Contest%20Rules%20and%20Disclosures?dl=0) agreement specific to the “Technical Submission” guidelines (outlined below).

---
## Technical Specifications
1. All source code and documentation in an Entry must be made and submitted pursuant to the terms of the Apache or MIT License. The Apache Licence and instructions for applying it can be found here: https://www.apache.org/licenses/LICENSE-2.0. The MIT License and instructions for applying it can be found here: https://opensource.org/licenses/MIT. 

2. In the Fastest VDF Implementation category, code must be produced that will solve a VDF at a given number of iterations and security difficulty on the reference hardware. The number of iterations and security difficulty will be provided at least 2 months before the end of the contest, and will be announced on the reddit and the keybase channel.

3. In the Best Discriminant Break category, the judging criteria is the file which gives the best number output from judge_entry.py. The entry needs to have three values each specifying which of our allowed discriminants it's on, and giving an element of the group and its order for each. The smallest of the three discriminants is the quality, and the greatest quality entry wins. The discriminants now are ones which have a four-byte challenge to create_discriminant(). 

4. The Contestant, or each member of a Team Contestant, must certify that the entire contents of the Technical Submission is the sole work of the Contestant, or collective work of the members of the Team Contestant, except to the extent that the Entry incorporates content that is publicly available or covered by an Apache or MIT license and is properly identified as such and that the Contestant has all legal rights necessary to grant the license granted in subsection (a) above.

5. Each Entry must be submitted with a Readme file that completes the entry form and describes in english the methods used in the software.
---
Want to learn more? Join [Chia's public Keybase group](https://keybase.io/team/chia_network.public) or read Chia's [reddit](https://www.reddit.com/r/chia_vdf).

