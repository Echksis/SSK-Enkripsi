import os
import base64
import string
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


# =========================================================
# ALPHABET OUTPUT SETIAP LEVEL
# =========================================================

LEVEL_1 = string.ascii_letters

LEVEL_2 = string.ascii_letters + string.digits

LEVEL_3 = string.ascii_letters + string.digits + \
          "!@#$%^&*()-_=+[]{}<>?/|~"


# =========================================================
# GENERATE AES-256 KEY
# =========================================================

def generate_key():
    # AES-256 = 32 byte = 256 bit
    return AESGCM.generate_key(bit_length=256)


# =========================================================
# ENCODE BYTE KE ALPHABET LEVEL
# =========================================================

def encode_custom(data, alphabet):

    base = len(alphabet)

    # Ubah byte menjadi angka besar
    number = int.from_bytes(data, "big")

    result = []

    while number > 0:
        number, remainder = divmod(number, base)
        result.append(alphabet[remainder])

    # Menjaga byte 0 di awal agar proses decode tetap sempurna
    for byte in data:
        if byte == 0:
            result.append(alphabet[0])
        else:
            break

    return "".join(reversed(result))


# =========================================================
# DECODE ALPHABET KEMBALI KE BYTE
# =========================================================

def decode_custom(text, alphabet):

    base = len(alphabet)

    number = 0

    for char in text:
        number = number * base + alphabet.index(char)

    # Ubah angka kembali menjadi byte
    byte_length = max(1, (number.bit_length() + 7) // 8)

    data = number.to_bytes(byte_length, "big")

    # Kembalikan leading zero
    leading_zero = 0

    for char in text:
        if char == alphabet[0]:
            leading_zero += 1
        else:
            break

    return b"\x00" * leading_zero + data


# =========================================================
# PILIH ALPHABET BERDASARKAN LEVEL
# =========================================================

def get_alphabet(level):

    if level == 1:
        return LEVEL_1

    elif level == 2:
        return LEVEL_2

    elif level == 3:
        return LEVEL_3

    else:
        return None


# =========================================================
# ENKRIPSI
# =========================================================

def encrypt(text, key, level):

    alphabet = get_alphabet(level)

    aes = AESGCM(key)

    # Nonce random 12 byte
    nonce = os.urandom(12)

    # Plaintext boleh berisi karakter apa saja
    plaintext = text.encode("utf-8")

    # AES-256-GCM
    ciphertext = aes.encrypt(
        nonce,
        plaintext,
        None
    )

    # Gabungkan nonce + ciphertext + authentication tag
    data = nonce + ciphertext

    # Ubah hasil AES menjadi karakter sesuai level
    encrypted = encode_custom(data, alphabet)

    return encrypted


# =========================================================
# DEKRIPSI
# =========================================================

def decrypt(encrypted_text, key, level):

    alphabet = get_alphabet(level)

    # Kembalikan karakter menjadi byte
    data = decode_custom(
        encrypted_text,
        alphabet
    )

    # Ambil nonce
    nonce = data[:12]

    # Ambil ciphertext + authentication tag
    ciphertext = data[12:]

    aes = AESGCM(key)

    # Dekripsi
    plaintext = aes.decrypt(
        nonce,
        ciphertext,
        None
    )

    return plaintext.decode("utf-8")


# =========================================================
# PROGRAM UTAMA
# =========================================================

print("======================================")
print("       AES-256-GCM ENCRYPTION")
print("======================================")

print("\nPilih Level:")
print("1. Huruf")
print("2. Huruf + Angka")
print("3. Huruf + Angka + Simbol")

level = int(input("\nLevel: "))

if level not in [1, 2, 3]:
    print("Level harus 1, 2, atau 3.")
    exit()


# =========================================================
# INPUT
# =========================================================

text = input("Masukkan teks: ")


# =========================================================
# GENERATE KEY
# =========================================================

key = generate_key()

key_base64 = base64.b64encode(key).decode("utf-8")


# =========================================================
# ENKRIPSI
# =========================================================

encrypted = encrypt(
    text,
    key,
    level
)


# =========================================================
# OUTPUT ENKRIPSI
# =========================================================

print("\n======================================")
print("HASIL ENKRIPSI")
print("======================================")

print("Level       :", level)
print("AES Key     :", key_base64)
print("Ciphertext  :", encrypted)


# =========================================================
# DEKRIPSI
# =========================================================

decrypted = decrypt(
    encrypted,
    key,
    level
)


# =========================================================
# OUTPUT DEKRIPSI
# =========================================================

print("\n======================================")
print("HASIL DEKRIPSI")
print("======================================")

print("Plaintext   :", decrypted)