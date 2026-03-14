"""
Solve script for the CTF crypto challenge.

Vulnerability: RC4 uses a 3-byte IV with only 4096 possible values.
The oracle encrypts  \x00 || FLAG  and get_flag encrypts  FLAG  with the same
SECRET_KEY.  When both happen to pick the same IV the keystream is identical,
so we can recover FLAG byte-by-byte:

    oracle_ct[0] = k[0]              (because plaintext byte 0 is 0x00)
    flag_ct[0]   = k[0] ^ FLAG[0]    => FLAG[0] = oracle_ct[0] ^ flag_ct[0]

    For i >= 1:
        k[i]     = oracle_ct[i] ^ FLAG[i-1]
        FLAG[i]  = flag_ct[i]   ^ k[i]
"""

from pwn import *
import sys

context.log_level = "info"

HOST = "tcp.espark.tn"
PORT = 9070


def is_rc4(data: bytes) -> bool:
    """Identify an RC4 ciphertext by its fixed IV structure."""
    return len(data) >= 4 and data[1] == 0xFF and 3 <= data[0] <= 18


def recover_flag(oracle_ct: bytes, flag_ct: bytes) -> bytes:
    """
    Given ciphertexts (after stripping the 3-byte IV) from a matching
    oracle call and a get_flag call that used the same IV/keystream,
    recover FLAG.
    """
    flag = bytearray()

    # k[0] = oracle_ct[0] ^ 0x00 = oracle_ct[0]
    k0 = oracle_ct[0]
    flag.append(flag_ct[0] ^ k0)

    for i in range(1, len(flag_ct)):
        ki = oracle_ct[i] ^ flag[i - 1]
        flag.append(flag_ct[i] ^ ki)

    return bytes(flag)


def main():
    r = remote(HOST, PORT)

    # Consume the banner
    r.recvuntil(b"get flag\n", timeout=10)

    oracle_rc4 = {}   # iv_bytes -> ciphertext_after_iv
    flag_rc4   = {}

    MAX_REQUESTS = 5000

    for attempt in range(1, MAX_REQUESTS + 1):
        # Collect oracle (option 1) twice as often as get_flag (option 2)
        if attempt % 3 != 0:
            r.sendline(b"1")
        else:
            r.sendline(b"2")

        line = r.recvline(timeout=8).strip()
        # consume prompt
        r.recvuntil(b"> ", timeout=8)

        try:
            data = bytes.fromhex(line.decode())
        except Exception:
            continue

        if not is_rc4(data):
            continue

        iv = data[:3]
        ct = data[3:]

        if attempt % 3 != 0:
            # oracle output
            oracle_rc4[iv] = ct
            if iv in flag_rc4:
                flag = recover_flag(ct, flag_rc4[iv])
                log.success(f"Matched IV after {attempt} requests!")
                log.success(f"FLAG = {flag.decode(errors='replace')}")
                r.close()
                return flag
        else:
            # get_flag output
            flag_rc4[iv] = ct
            if iv in oracle_rc4:
                flag = recover_flag(oracle_rc4[iv], ct)
                log.success(f"Matched IV after {attempt} requests!")
                log.success(f"FLAG = {flag.decode(errors='replace')}")
                r.close()
                return flag

        if attempt % 200 == 0:
            log.info(
                f"Attempt {attempt}: "
                f"{len(oracle_rc4)} oracle RC4, {len(flag_rc4)} flag RC4"
            )

    log.failure(f"No IV collision after {MAX_REQUESTS} attempts "
                f"({len(oracle_rc4)} oracle, {len(flag_rc4)} flag)")
    r.close()
    return None


if __name__ == "__main__":
    flag = main()
    if flag is not None:
        print(f"\n{'='*50}")
        print(f"FLAG: {flag.decode(errors='replace')}")
        print(f"{'='*50}")
    else:
        print("[-] Could not recover the flag.")
