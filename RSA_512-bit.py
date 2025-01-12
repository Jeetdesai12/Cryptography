import random
from sympy import isprime

# To find GCD (Required to find e)
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

# To generate large prime p & q
def generate_large_prime(bits=512):
    while True:
        num = random.getrandbits(bits)
        if isprime(num):
            return num

# To calculate modular inverse using Extended Euclidean Algorithm
def calculate_mod_inverse(e, phi_n):
    def extended_gcd(a, b):
        if b == 0:
            return a, 1, 0
        gcd, x1, y1 = extended_gcd(b, a % b)
        x = y1
        y = x1 - (a // b) * y1
        return gcd, x, y

    gcd, x, _ = extended_gcd(e, phi_n)
    if gcd != 1:
        raise ValueError("Modular inverse not found")
    return x % phi_n

# Generate keys in RSA
def generate_keys(bits=512):
    
    # Generate two distinct large primes p and q
    p = generate_large_prime(bits)
    q = generate_large_prime(bits)

    while p == q:  # This ensures p and q are distinct
        q = generate_large_prime(bits)

    n = p * q  # n is modulus
    phi_n = (p - 1) * (q - 1)  # phi_n is totient

    # print("Prime p:", p)
    # print("Prime q:", q)
    # print("Modulus n:", n)
    # print("Totient phi_n:", phi_n)

    # Finding e as small as possible
    e = 2
    while e < phi_n:
        if gcd(e, phi_n) == 1:
            break
        e += 1

    print("Chosen e:", e)

    # Calculate d 
    d = calculate_mod_inverse(e, phi_n)

    print("Calculated d:", d)

    return (e, n), (n, d)

#---------Code Starts here------------------------------------------------------

message= int(input("Enter msg to be encrypted: "))

# Encryption---------------------------------------------------------------------
def encryption(message, public_key):
    e, n = public_key
    return pow(message, e, n)

# Decryption----------------------------------------------------------------------
def decryption(cipher_text, private_key):
    n, d = private_key
    return pow(cipher_text, d, n)

# Generate 512-bit RSA keys
public_key, private_key = generate_keys(bits=512)

# Output---------------------------------------------------------------------------
print("Public key:", public_key)
print("Private key:", private_key)

print("Original message:", message)


cipher_text = encryption(message, public_key)
print("Encrypted message:", cipher_text)

decrypted_message = decryption(cipher_text, private_key)
print("Decrypted message:", decrypted_message)
