# RSA Implementation in Python

This is a simple implementation of the RSA algorithm in Python. It is not meant to be used for any serious encryption purposes, but rather as a learning tool to understand how RSA works.

## Usage

This was tested with Python 3.11.3.

Sample I/O:

```
Enter a positive integer e: 13
Enter a message (<= 4 characters): test

Testing with M = test and e = 13:
  p: 3833
  q: 6637
  n: 25439621
  M: test
  C: 3285267
  Encoded P: 397838
  Decoded P: test
```

where C is the encrypted message, i.e., cyber text, and P is the decrypted message, i.e., plaintext, M is the original message, p and q are the prime numbers, and n is the product of p and q.