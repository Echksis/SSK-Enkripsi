import string

# =========================================================
# 3-LEVEL ENKRIPSI
# =========================================================

ALPHABET = string.ascii_letters

NUMBERS = string.digits

SYMBOLS = "!@#$%^&*()-_=+[]{}<>?/|~"


def encrypt(text, level, key):
    """
    Level 1 : huruf
    Level 2 : huruf + angka
    Level 3 : huruf + angka + simbol
    """

    if level == 1:
        charset = string.ascii_letters
    elif level == 2:
        charset = string.ascii_letters + string.digits
    elif level == 3:
        charset = string.ascii_letters + string.digits + SYMBOLS
    else:
        return "Level harus 1, 2, atau 3"

    result = []

    # Membuat angka kunci dari karakter key
    key_value = sum(ord(c) for c in key)

    for i, char in enumerate(text):

        # Karakter yang tidak ada dalam charset tetap dipertahankan
        if char not in charset:
            result.append(char)
            continue

        # Pola pergeseran berubah berdasarkan:
        # 1. posisi karakter
        # 2. nilai ASCII
        # 3. nilai key
        shift = (
            key_value
            + (i + 1) ** 2
            + ord(char) * (i + 3)
        )

        # Tambahan pengacakan berdasarkan level
        if level == 1:
            shift += 17

        elif level == 2:
            shift += 43 + (i * 7)

        elif level == 3:
            shift += 91 + (i * 13)

        # Cari posisi karakter
        index = charset.index(char)

        # Geser karakter
        new_index = (index + shift) % len(charset)

        result.append(charset[new_index])

    # Tahap kedua: membalik blok berdasarkan level
    encrypted = "".join(result)

    if level == 1:
        encrypted = encrypted[::-1]

    elif level == 2:
        encrypted = encrypted[::2] + encrypted[1::2]

    elif level == 3:
        encrypted = encrypted[::-1]
        encrypted = encrypted[::2] + encrypted[1::2]

    return encrypted


# =========================================================
# PROGRAM UTAMA
# =========================================================

print("===================================")
print("       ENKRIPSI 3 LEVEL")
print("===================================")

text = input("Masukkan teks : ")
key = input("Masukkan kunci : ")

print("\nPilih level:")
print("1. Huruf")
print("2. Huruf + Angka")
print("3. Huruf + Angka + Simbol")

level = int(input("Level : "))

hasil = encrypt(text, level, key)

print("\nHasil Enkripsi:")
print(hasil)