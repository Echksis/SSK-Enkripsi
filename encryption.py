import os
import base64
import string
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

LEVEL_1 = string.ascii_letters

LEVEL_2 = string.ascii_letters + string.digits

LEVEL_3 = string.ascii_letters + string.digits + \
          "!@#$%^&*()-_=+[]{}<>?/|~"

def generate_key():
    # AES-256 membutuhkan key 32 byte = 256 bit
    return AESGCM.generate_key(bit_length=256)

def validate_text(text, level):

    if level == 1:
        charset = LEVEL_1

    elif level == 2:
        charset = LEVEL_2

    elif level == 3:
        charset = LEVEL_3

    else:
        return False

    for char in text:
        if char not in charset:
            return False

    return True

def encrypt(text, key):

    aes = AESGCM(key)

    # Nonce random 12 byte
    nonce = os.urandom(12)

    # Ubah plaintext menjadi byte
    plaintext = text.encode("utf-8")

    # AES-GCM mengenkripsi sekaligus membuat authentication tag
    ciphertext = aes.encrypt(
        nonce,
        plaintext,
        None
    )

    # Nonce digabung dengan ciphertext
    result = nonce + ciphertext

    # Diubah menjadi Base64 agar mudah ditampilkan
    return base64.b64encode(result).decode("utf-8")

def decrypt(encrypted_text, key):

    aes = AESGCM(key)

    # Kembalikan Base64 menjadi byte
    data = base64.b64decode(encrypted_text)

    # 12 byte pertama adalah nonce
    nonce = data[:12]

    # Sisanya adalah ciphertext + authentication tag
    ciphertext = data[12:]

    # Dekripsi
    plaintext = aes.decrypt(
        nonce,
        ciphertext,
        None
    )

    return plaintext.decode("utf-8")

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

text = input("Masukkan teks: ")

if not validate_text(text, level):
    print("\nTeks mengandung karakter yang tidak diperbolehkan.")
    
    if level == 1:
        print("Level 1 hanya menerima huruf.")

    elif level == 2:
        print("Level 2 hanya menerima huruf dan angka.")

    elif level == 3:
        print("Level 3 menerima huruf, angka, dan simbol.")

    exit()

key = generate_key()

key_base64 = base64.b64encode(key).decode("utf-8")

encrypted = encrypt(text, key)

print("\n======================================")
print("HASIL ENKRIPSI")
print("======================================")

print("Level       :", level)
print("AES Key     :", key_base64)
print("Ciphertext  :", encrypted)

decrypted = decrypt(encrypted, key)

print("\n======================================")
print("HASIL DEKRIPSI")
print("======================================")

print("Plaintext   :", decrypted)