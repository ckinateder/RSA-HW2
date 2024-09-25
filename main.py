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
    output = 0
    bword = s[::-1]
    for i in range(len(s)):
        output += (ord(bword[i]) - 96) * 27**i
        print(f"output+= {ord(bword[i]) - 96} * 27^{i}")

    print(output)

    return output


if __name__ == "__main__":
    # prime generation
    phi_n = None
    e = None
    # check if e and phi(n) are coprime
    # Once primes p and q are computed reject if the totient function of n = pq
    # is not relatively prime to the public key e, i.e., reject if
    # gcd(e,φ(n)) != 1. If this happens, then generate new primes p and q and
    while not (phi_n or e) or math.gcd(e, phi_n) != 1:
        e = int(input("Enter a positive integer e: "))
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

    M = input("Enter a message M (case-insensitive): ")
    M = M.lower()

    # encryption
    C = encode_string(M)

    # decryption
    P = C

    # output
    print(f"p: {p}")
    print(f"q: {q}")
    print(f"n: {n}")
    print(f"M: {M}")
    print(f"C: {C}")
    print(f"P: {P}")
