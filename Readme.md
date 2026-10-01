# Logika Enkripsi AES-256-GCM

Program ini menggunakan **AES-256-GCM** untuk mengenkripsi teks dengan 3 level berdasarkan jenis karakter yang diperbolehkan.

## Level Enkripsi

```text
Level 1 → Huruf
Level 2 → Huruf + Angka
Level 3 → Huruf + Angka + Simbol
```

Ketiga level tetap menggunakan **AES-256-GCM**. Perbedaannya hanya pada karakter yang dapat dimasukkan.

## Cara Kerja

Alur utama program:

```text
Input Teks
    ↓
Pilih Level
    ↓
Validasi Karakter
    ↓
Generate Key AES-256
    ↓
Generate Nonce Random
    ↓
AES-256-GCM
    ↓
Ciphertext
    ↓
Base64
    ↓
Hasil Enkripsi
```

### 1. Input dan Level

User memasukkan teks dan memilih level.

Program kemudian memeriksa apakah karakter pada teks sesuai dengan level yang dipilih.

Contoh:

```text
Level 1 → Hello       ✓
Level 2 → Hello123    ✓
Level 3 → Hello123!   ✓
```

### 2. Key AES-256

Program membuat **key berukuran 256 bit** yang digunakan untuk proses enkripsi.

```text
Plaintext + Key
       ↓
    AES-256-GCM
```

Key yang digunakan saat dekripsi harus sama dengan key saat enkripsi.

### 3. Random Nonce

Setiap enkripsi membuat **nonce random 12 byte**.

```text
Teks yang sama
     +
Key yang sama
     +
Nonce berbeda
     ↓
Ciphertext berbeda
```

Karena itu, jika teks yang sama dienkripsi beberapa kali, hasilnya tetap dapat berbeda.

### 4. AES-256-GCM

Plaintext diproses menggunakan AES-256-GCM bersama key dan nonce.

```text
Plaintext
    +
AES-256 Key
    +
Random Nonce
    ↓
AES-256-GCM
    ↓
Ciphertext
```

GCM juga menghasilkan **authentication tag** yang digunakan untuk memastikan data tidak berubah saat proses dekripsi.

### 5. Base64

Hasil enkripsi berupa data binary kemudian diubah menjadi Base64 agar dapat ditampilkan sebagai teks.

```text
Ciphertext
    ↓
Base64
    ↓
Encrypted Text
```

## Inti Logika

```text
LEVEL
  ↓
Validasi Input
  ↓
Plaintext
  ↓
AES-256 Key + Random Nonce
  ↓
AES-256-GCM
  ↓
Ciphertext + Authentication Tag
  ↓
Base64
  ↓
Hasil Enkripsi
```