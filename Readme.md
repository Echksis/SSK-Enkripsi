# Logika Enkripsi AES-256-GCM

Program ini menggunakan **AES-256-GCM** untuk mengenkripsi teks dengan 3 level. Perbedaan setiap level terletak pada karakter yang digunakan untuk menampilkan **hasil enkripsi**.

## Level Enkripsi

```text
Level 1 → Huruf
Level 2 → Huruf + Angka
Level 3 → Huruf + Angka + Simbol
```

Ketiga level tetap menggunakan **AES-256-GCM**. Input teks dapat berisi karakter apa saja, sedangkan level menentukan karakter yang digunakan pada hasil enkripsi.

## Cara Kerja

Alur utama program:

```text
Input Teks
    ↓
Pilih Level
    ↓
Generate Key AES-256
    ↓
Generate Nonce Random
    ↓
AES-256-GCM
    ↓
Ciphertext + Authentication Tag
    ↓
Encoding berdasarkan Level
    ↓
Hasil Enkripsi
```

### 1. Input dan Level

User memasukkan teks dan memilih level.

Berbeda dengan pembatasan input, program ini **menerima teks dengan karakter apa saja**.

Contoh:

```text
NAJIB
NAJIB123
NAJIB @#$ 123
Hello_World!
```

Semua input tersebut dapat diproses pada Level 1, 2, maupun 3.

Perbedaannya terdapat pada karakter yang digunakan untuk menampilkan hasil enkripsi.

```text
Level 1 → hanya huruf
Level 2 → huruf + angka
Level 3 → huruf + angka + simbol
```

### 2. Key AES-256

Program membuat **key berukuran 256 bit** secara random.

```text
Generate Key
     ↓
  256 bit
     ↓
AES-256 Key
```

Key digunakan untuk proses enkripsi dan harus sama ketika melakukan dekripsi.

Key bersifat rahasia dan tidak digabungkan dengan ciphertext.

### 3. Random Nonce

Setiap proses enkripsi membuat **nonce random sebesar 12 byte**.

```text
Teks yang sama
     +
Key yang sama
     +
Nonce berbeda
     ↓
Ciphertext berbeda
```

Nonce digunakan agar teks dan key yang sama tidak selalu menghasilkan ciphertext yang sama.

Nonce tidak perlu dirahasiakan dan disimpan bersama ciphertext agar dapat digunakan kembali saat dekripsi.

### 4. AES-256-GCM

Plaintext diproses menggunakan AES-256-GCM dengan key dan nonce.

```text
Plaintext
    +
AES-256 Key
    +
Random Nonce
    ↓
AES-256-GCM
    ↓
Ciphertext + Authentication Tag
```

Authentication tag digunakan untuk memeriksa apakah ciphertext masih valid dan tidak mengalami perubahan saat proses dekripsi.

### 5. Encoding Berdasarkan Level

Hasil dari AES berupa data binary sehingga tidak langsung ditampilkan sebagai karakter biasa.

Program kemudian mengubah data tersebut menggunakan alphabet sesuai level.

```text
Level 1
↓
Huruf

Level 2
↓
Huruf + Angka

Level 3
↓
Huruf + Angka + Simbol
```

Contohnya, hasil AES yang sama dapat diubah menggunakan alphabet yang berbeda sehingga karakter pada hasil akhirnya mengikuti level yang dipilih.

Proses ini bukan enkripsi tambahan, tetapi **encoding** agar ciphertext dapat ditampilkan menggunakan karakter yang sesuai dengan level.

### 6. Proses Dekripsi

Saat dekripsi, hasil encoding dikembalikan menjadi data binary.

```text
Ciphertext
    ↓
Decode berdasarkan Level
    ↓
Ambil Nonce
    ↓
Ambil Ciphertext + Authentication Tag
    ↓
AES-256-GCM
    ↓
Plaintext
```

Key dan level yang digunakan harus sesuai dengan proses enkripsi.

## Inti Logika

```text
INPUT BEBAS
     ↓
Pilih Level
     ↓
Generate AES-256 Key
     ↓
Generate Random Nonce
     ↓
AES-256-GCM
     ↓
Ciphertext + Authentication Tag
     ↓
Encoding sesuai Level
     ↓
HASIL ENKRIPSI
```

Perbedaan ketiga level hanya terletak pada **karakter yang digunakan untuk menampilkan hasil enkripsi**:

```text
Level 1 → Huruf

Level 2 → Huruf + Angka

Level 3 → Huruf + Angka + Simbol
```

Sedangkan algoritma enkripsi yang digunakan pada semua level tetap:

```text
AES-256-GCM
```