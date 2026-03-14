import os, random
from Crypto.Cipher import AES, ARC4, ChaCha20
from Crypto.Util.Padding import pad
import nacl.secret

SECRET_KEY    = os.urandom(16)
SECRET_KEY_32 = os.urandom(32)
FLAG          = b"?????????????????????????????????????????????"
METHODS = ["rc4", "rc4", "rc4", "aes_cbc", "chacha20", "xsalsa20", "aes_ofb"]

def rc4_encrypt(pt):
    a  = random.randint(0, len(SECRET_KEY) - 1)
    x  = random.randint(0, 255)
    iv = bytes([a + 3, 255, x])
    return (iv + ARC4.new(iv + SECRET_KEY).encrypt(pt)).hex()

def aes_cbc_encrypt(pt):
    iv = os.urandom(16)
    return (iv + AES.new(SECRET_KEY, AES.MODE_CBC, iv).encrypt(pad(pt, 16))).hex()

def chacha20_encrypt(pt):
    iv = os.urandom(12)
    return (iv + ChaCha20.new(key=SECRET_KEY_32, nonce=iv).encrypt(pt)).hex()

def xsalsa20_encrypt(pt):
    return bytes(nacl.secret.SecretBox(SECRET_KEY_32).encrypt(pt)).hex()

def aes_ofb_encrypt(pt):
    iv = os.urandom(16)
    return (iv + AES.new(SECRET_KEY, AES.MODE_OFB, iv).encrypt(pt)).hex()

def oracle():
    method = random.choice(METHODS)
    if method == "rc4":   return rc4_encrypt(b"\x00" + FLAG)
    elif method == "aes_cbc":  return aes_cbc_encrypt(FLAG)
    elif method == "chacha20": return chacha20_encrypt(FLAG)
    elif method == "xsalsa20": return xsalsa20_encrypt(FLAG)
    elif method == "aes_ofb":  return aes_ofb_encrypt(FLAG)

def get_flag():
    method = random.choice(METHODS)
    if method == "rc4":   return rc4_encrypt(FLAG)
    elif method == "aes_cbc":  return aes_cbc_encrypt(FLAG)
    elif method == "chacha20": return chacha20_encrypt(FLAG)
    elif method == "xsalsa20": return xsalsa20_encrypt(FLAG)
    elif method == "aes_ofb":  return aes_ofb_encrypt(FLAG)

print("welcome to my oracle you will never be able breake me xD choose a number :")
print("1. encrypt")
print("2. get flag")

while True:
    choice = input("> ")
    if choice == "1":
        print(oracle())
    elif choice == "2":
        print(get_flag())
    else:
        print("invalid")