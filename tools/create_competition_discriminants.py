from inkfish.create_discriminant import create_discriminant
import hashlib
import sys

# This is the script that will get used to generate the
# classgroup discriminants for the competition. The secret
# seed will be revealed only after the deadline for
# submissions. Here you can verify that commitment matches
# the secret, once the secret is released.
number_of_discriminants = 10
discriminant_bit_size = 2048
secret_seed_commitment = "2fe1e53289900911495b570a6ef9bed17b90a7eb02922631563fca641b83b8ef"


if __name__ == '__main__':
    # Checks that the commitment is valid, given an input secret seed
    # passed in from the command line. The secret seed will be released
    # at the end of the competition.
    seed = str.encode(sys.argv[1], "latin-1")
    hash_of_secret = hashlib.sha256(seed).digest()
    assert(hash_of_secret.hex() == secret_seed_commitment)

    # Generates the discriminants
    for i in range(10):
        print(create_discriminant(seed + bytes([i]), 2048))
