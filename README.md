# Chia VDF competition and implementation

In an attempt to create a secure, open and decentralized consensus algorithm, Chia is hosting a 3 month long competition, with a total of around $100,000 in prizes, for the implementation of fast and secure verifiable delay functions using class groups.

This is an in-development version of the Chia Network proof-of-time verifiable delay function "inkfish". Below, you can also find a summary of the rules, a link to the rules and disclosures, relevant research papers. Also, check out the [blog post](https://medium.com/@chia_network/chia-vdf-competition-guide-5382e1f4bd39) which explains how to participate.

The verifiable delay function used is the iterated squarings / RSA timelock construction. The code implements this verifiable delay function using class groups.

Furthermore, there are two proof approaches implemented here
1. The [first one](https://eprint.iacr.org/2018/627.pdf) by Krzysztof Pietrzak, that is fast to create, but large and slow to verify.
2. The [second one](https://eprint.iacr.org/2018/623.pdf) by Benjamin Wesolowski which is slower to create (but parallelizable), but small, and quick to verify. There is also a variation of wesolowski called n-wesolowski, that allows computing the proof faster, with some added parallelism, proof size, and verification time.

Both approaches are summarized in [this survey paper](https://eprint.iacr.org/2018/712.pdf) by Boneh, Bünz, and Fisch, and we have an explanation of class groups and binary quadratic forms [here](https://github.com/Chia-Network/vdf-competition/tree/master/classgroups.pdf).

A sample submission with a C++ implementation can be found [here](https://github.com/Chia-Network/vdf-competition/tree/master/sample-entry-1).

Want to learn more? Join [Chia's public Keybase group](https://keybase.io/team/chia_network.public) or read Chia's [reddit](https://www.reddit.com/r/chia_vdf).


---
## ENTRY FORM

By providing your legal first and last names, street address, city, zip code, daytime and home phone number, email address, and agreement to the [VDF Contest Challenge Rules and Disclosures agreement](https://www.dropbox.com/s/3hmxe7717x5a0pp/Chia%20Network%20-%20VDF%20Contest%20Rules%20and%20Disclosures%20%286%29.pdf?dl=0), and  along with the source code and documentation meeting the Entry Specifications described in the VDF Contest Challenge Rules and Disclosures agreement above (specifically the “Technical Submission”) to [Chia's public Keybase group](https://keybase.io/team/chia_network.public). The judges will communicate with your team using a keybase shared git repo.

The Entry Form and Technical Submission together are considered the entry (“Entry”). An Entry is not complete and will not be considered if either portion is missing.

### Entry Form Requirements
An Entry may be submitted by a team of individuals working collaboratively (a “Team Contestant”), in which case, each individual member of the team must complete the Entry Form as described above and all members of the Team Contestant must designate the same point of contact to receive official Challenge correspondence.

1. Completed version of the [Entry Form](https://www.dropbox.com/s/odsglm1eu9z6g8v/CHIA%20NETWORK%20APPLICATION%20FORM%204812-8893-1439%20v.1.pdf?dl=0).

2. Signed version of the [VDF Contest Challenge Rules and Disclosures agreement](https://www.dropbox.com/s/3hmxe7717x5a0pp/Chia%20Network%20-%20VDF%20Contest%20Rules%20and%20Disclosures%20%286%29.pdf?dl=0)

3. Source code and documentation meeting the Entry Specifications described in the [VDF Contest Challenge Rules and Disclosures agreement](https://www.dropbox.com/s/3hmxe7717x5a0pp/Chia%20Network%20-%20VDF%20Contest%20Rules%20and%20Disclosures%20%286%29.pdf?dl=0) specific to the “Technical Submission” guidelines (outlined below).

### Technical Specifications
1. All source code and documentation in an Entry must be made and submitted pursuant to the terms of the Apache, MIT, or LGPL License. The Apache Licence and instructions for applying it can be found [here](https://www.apache.org/licenses/LICENSE-2.0). The MIT License and instructions for applying it can be found [here](https://opensource.org/licenses/MIT). The GNU Lesser General Public License Version 3.0 (“LGPL”) License can be found [here](https://www.gnu.org/licenses/lgpl-3.0.en.html).

2. In the Fastest VDF Implementation category, code must be produced that will solve a VDF at a given number of iterations and security difficulty on the reference hardware. The [repeated squarings VDF](https://eprint.iacr.org/2018/623.pdf) should be used, but we do not require computation of a proof, and only the speed of computation of the output will be judged. The VDF should be computed in the class group setting, and should output the same as our sample code above (see classgroup.py for naive implementation of class groups). The number of iterations and security difficulty will be provided at least 2 months before the end of the contest, and will be announced on the reddit and the keybase channel.

3. In the Best Discriminant Break category, the judging criteria is the file which gives the best number output from judge_entry.py. The entry needs to have three values each specifying which of our allowed discriminants it's on, and giving an element of the group and its order for each. The smallest of the three discriminants is the quality, and the greatest quality entry wins. The discriminants now are ones which have a four-byte challenge to create_discriminant().

4. The Contestant, or each member of a Team Contestant, must certify that the entire contents of the Technical Submission is the sole work of the Contestant, or collective work of the members of the Team Contestant, except to the extent that the Entry incorporates content that is publicly available or covered by an Apache or MIT license and is properly identified as such and that the Contestant has all legal rights necessary to grant the license granted in subsection (a) above.

5. Each Entry must be submitted with a Readme file that completes the entry form and describes in english the methods used in the software.
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

Generate a wesolowski proof of time.

    $ pot deadbeef 1000

Generate an n-wesolowski proof of time, with verbose logging.

    $ pot -t n-wesolowski --depth 2 deadbeef --verbose 1000

Verify an n-wesolowski proof of time.

    $ pot -t n-wesolowski deadbeef 1000 <proof>

To see some benchmarks, run

    $ python3 benchmarks/benchmarks.py

## Benchmarks

Some sample benchmarks on dual core 3.5GHz i7. For the first part of the competition, the relevant benchmarks are the class group squaring times.

```
Classgroup 512 bit multiply                                                      0.16 ms
Classgroup 512 bit square                                                        0.17 ms
Classgroup 1024 bit multiply                                                     0.34 ms
Classgroup 1024 bit square                                                       0.35 ms
Classgroup 2048 bit multiply                                                     0.83 ms
Classgroup 2048 bit square                                                       0.82 ms
Generate 512 bit discriminant                                                    17.56 ms
Generate 1024 bit discriminant                                                   28.33 ms
Generate 2048 bit discriminant                                                   216.82 ms
VDF 10000 iterations, 512bit classgroup                                          1576.67 ms
VDF 10000 iterations, 1024bit classgroup                                         3383.61 ms
VDF 10000 iterations, 2048bit classgroup                                         8320.66 ms
VDF 10000 iterations, 2048bit RSA modulus                                        115.71 ms
VDF 10000 iterations, 4096bit RSA modulus                                        369.17 ms
Wesolowski  512b class group, 10000 iterations, proof                            287.43 ms
    - Percentage of VDF time: 18.2453909726637 %
Wesolowski 512b class group, 10000 iterations, verification                      62.54 ms
n-wesolowski depth 2 512b class group, 10000 iterations, proof                   1630.58 ms
    - Percentage of VDF time: 3.707000699434091 %
n-wesolowski depth 2 512b class group, 10000 iterations, verification            172.94 ms
Pietrzak  512b class group, 10000 iterations, proof                              382.78 ms
    - Percentage of VDF time: 24.379376193507323 %
Pietrzak 512b class group, 10000 iterations, verification                        434.43 ms
```

```
C Classgroup 2048 bit multiply                                                   0.09 ms
C Classgroup 2048 bit square                                                     0.075 ms
```
