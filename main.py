# Calvin Kinateder

"""
Your program should prompt the user to input a positive integer representing the public
key e. If the user enters a number that is not relatively prime to n = pq, then have the user
reenter and keep doing this until e and n are coprime, i.e., gcd(e,φ(n)) = 1. Also prompt
the user to enter the message M (as a character string). For handing purposes, run your
program with M = “TEST”. Output p, q, n, M, C, P where C is the encrypted message,
i.e., cyber text, and P is the decrypted message, i.e., plaintext. If your program is
working correctly then M should be equal to P.
"""

import math
import random
from typing import Tuple


def miller_rabin_prime_test(n: int) -> bool:
    """
    Miller-Rabin primality test. Returns True if n is prime, False otherwise.

    Args:
        n: int - number to test for primality

    Returns:
        bool - True if n is prime, False otherwise
    """
    k = n - 1
    a = random.randint(2, n - 2)

    # fermat's little theorem
    if a**k % n != 1:
        return False

    # other tests basesd on using a^k -1 = (a^k/2 - 1)(a^k/2 + 1)
    while k % 2 == 0:
        k = k // 2  # integer division
        if a**k % n == n - 1:
            return True
        elif a**k % n != 1:
            return False

    return True


def mc_repeat(n: int, k: int) -> bool:
    """Ramp up correctness of Miller-Rabin test by repeating it k times.

    Args:
        n (int): is the number to be tested for primality
        k (int): number of times to repeat the test

    Returns:
        bool: if MC returns .false. for any invocation, .true. otherwise
    """
    for _ in range(k):
        if not miller_rabin_prime_test(n):
            return False

    return True


def encode_string(s: str) -> int:
    """COnverts a string to an integer using the BEATCATII encoding scheme.

    A, B, ..., Z are assigned to 1, 2, ..., 26 respectively.
    Space is assigned to 0.

    Args:
        s (str): input string

    Returns:
        int: encoded integer
    """
    s = s.lower()  # convert to lowercase
    output = 0
    bword = s[::-1]
    for i in range(len(s)):
        output += (ord(bword[i]) - 96) * 27**i
        #        print(f"output+= {ord(bword[i]) - 96} * 27^{i}")

    return output


def decode_string(n: int) -> str:
    """Converts an integer to a string using the BEATCATII encoding scheme.

    A, B, ..., Z are assigned to 1, 2, ..., 26 respectively.
    Space is assigned to 0.

    Args:
        n (int): input integer

    Returns:
        str: decoded string
    """
    output = ""
    while n > 0:
        n, r = divmod(n, 27)
        if r == 0:
            output += " "
        else:
            output += chr(r + 96)

    return output[::-1]


# from https://en.wikibooks.org/wiki/Algorithm_Implementation/Mathematics/Extended_Euclidean_algorithm
def extended_euclidean_gcd(a: int, b: int) -> Tuple[int, int, int]:
    """return (g, x, y) such that a*x + b*y = g = gcd(a, b)"""
    if a == 0:
        return (b, 0, 1)
    else:
        b_div_a, b_mod_a = divmod(b, a)
        g, x, y = extended_euclidean_gcd(b_mod_a, a)
        return (g, y - b_div_a * x, x)


def validate_message(s: str) -> bool:
    """Validates a message to ensure it only contains letters and spaces.

    Args:
        s (str): input message

    Returns:
        bool: True if the message is valid, False otherwise
    """
    return s and s.replace(" ", "").isalpha() and len(s) <= 4


def compute_private_key(e: int, phi_n: int) -> int:
    """Computes the private key d using the extended euclidean algorithm.

    private key d is the modular multiplicative inverse of e mod phi(n),
    where phi(n) is the totient function of n = pq
    We will use the extended euclidean algorithm to find d
    d = s mod phi(n)
    if s < 0, d = s % phi(n) + phi(n)

    Args:
        e (int): public key
        phi_n (int): totient function of n

    Returns:
        int: private key d
    """
    g, s, _ = extended_euclidean_gcd(e, phi_n)
    d = s % phi_n
    if s < 0:
        d = s % phi_n + phi_n

    return d


if __name__ == "__main__":
    # prime generation
    phi_n = None
    e = None
    # check if e and phi(n) are coprime
    # Once primes p and q are computed reject if the totient function of n = pq
    # is not relatively prime to the public key e, i.e., reject if
    # gcd(e,φ(n)) != 1. If this happens, then generate new primes p and q and
    while not (phi_n or e) or math.gcd(e, phi_n) != 1:
        try:
            e = int(input("Enter a positive integer e: "))
            if e < 0:
                raise ValueError
        except ValueError:
            print("Invalid input. Please enter a positive integer.")
            continue
        p = 0
        q = 0
        # generate p and q
        # n = pq must satisfy 456975 < n < 4294967297
        # p and q must satisfy miller-rabin prime test with mc_repeat(10)
        while (
            p * q < 456975
            or p * q > 4294967297
            or not mc_repeat(p, 10)
            or not mc_repeat(q, 10)
        ):
            p = random.randint(1000, 10000)
            q = random.randint(1000, 10000)

        # calculate n
        n = p * q

        # calculate phi(n)
        phi_n = (p - 1) * (q - 1)

    # message
    M = input("Enter a message (<= 4 characters): ")
    while not validate_message(M):
        print(
            "Invalid input. Please enter a message up to four characters long containing only letters and spaces."
        )
        M = input("Enter a message (<= 4 characters): ")

    # encode the message into a number. this is NOT encryption
    m = encode_string(M)
    assert decode_string(m) == M, "Encoding/decoding error"

    # encryption
    # C = M^e mod n
    C = pow(m, e, n)

    # private key calculation
    d = compute_private_key(e, phi_n)

    # decryption
    # M = C^d mod n
    P = pow(C, d, n)

    # print
    indent = " " * 2
    stats = f"\nTesting with M = {M} and e = {e}:\n"
    stats += f"{indent}p: {p}\n"
    stats += f"{indent}q: {q}\n"
    stats += f"{indent}n: {n}\n"
    stats += f"{indent}M: {M}\n"
    stats += f"{indent}C: {C}\n"
    stats += f"{indent}Encoded P: {P}\n"
    stats += f"{indent}Decoded P: {decode_string(P)}"
    print(stats)
