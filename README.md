Nama: Razan Alif Azhima

NPM: 2506632942

Kelas: PBP F

### TUGAS 1
1.
2.
3.

### TUGAS 2

1.
urls.py projek -> mengarahkan local server (komputer anda) ke index.html
urls.py app -> mengarahkan ke app yg terbuat di server luar
view:
- menerima permintaan HttpRequest
- mengolalah data dari Model (kasus ini untuk experience)
- render template html
- mengembalikan respons HttpResponse
template -> pemisahan logika dan tampilan, penyajian data dinamis

2. alasan utamanya adalah pembaruan data tanpa mengubah kode

3. 
makemigrations -> (pada kasus ini) memeriksa perubahan di models.py, then membuat berkas skrip migrasi baru di migrations/. 
                    TIDAK mengubah dan memakai basis data 
migrate -> Membaca berkas skrip migrasi yang belum diterapkan dan menjalankan perintah SQL ke basis data untuk memperbarui struktur tabel

lets say...
mau tambah is_active ke:

class Skill(models.Model):
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
            v
python manage.py makemigrations -> Django detects new changes dan membuat berkas baru, misal 0067_skill_is_active.py. basis data belum berubah
            v
python manage.py migrate
Django eksekusi perintah SQL sehingga kolom "is_active" benar-benar terbuat di dalam basis data

### TUGAS 3

1. Alasan memakai ModelForm:
    - Prinsip dont repeat yourself (dry) -> render field form otomatis jadi tidak perlu nulis ulang 1 per 1 di HTML
    - data validation -> langsung memvalidasi data saat kita input di formnya
    alasan memakai {% csrf_token %}:
    - CSRF protection: mencegah Cross-Site Request Forgery (CSRF)
    - kasih session cookie (seperti nilai rahasia) -> django check token cocok

2. Keunggulan JSON Dibandingkan XML dalam Pengembangan Web Modern
    - Ukuran kecil, dibanding dengan XML
    - mendukung JSON
    - lebih cepat
    - lebih mudah dibaca

3. Alur Pengembalian Data Portofolio dalam Bentuk JSON & Pentingnya Serialisasi:
    1. permintaan dari client
    2. routing url
    3. pengambilan data
    4. proses serialisasi
    5. pengiriman respons
    6. penerimaan data

    Alasan perlunya proses serialiasi:
    - struktur data Django amat kompleks
    - Http hanya bisa send data berupa teks

### TUGAS 7 — Django REST Framework

1.  REST (REpresentational State Transfer) adalah gaya arsitektur perangkat lunak yang mendeskripsikan antarmuka seragam di antara komponen-komponen yang terpisah secara fisik,
    sering kali melalui Internet dalam arsitektur klien-server.
    Constraints/Batasan: 
    - Client-Server Separation
    - Stateless: setiap request memiliki semua informasi yang dibutuhkan
    - Cacheable: respons harus menyatakan apakah boleh di-cache
    - Uniform Interface: resource diidentifikasi lewat URL, dimanipulasi lewat representasi, pesan bersifat self-descriptive, dan (idealnya) memakai hypermedia
    - Layered System & Code on Demand

    untuk JSON, itu hanya format DATA. API hanya mengembalikan JSON bisa saja melanggar prinsip REST

    Aspek                       PUT                                         PATCH
    Semantik                Menganti seluruh resource            mengubah sebagian resource
    Payload                 representasi lengkap                 hanya field yang berubah
    Field tak terkirim      Dianggap hilang                      dibiarkan seperti semula
    idempoten               Ya                                    tidak dijamin

2.  Serializer adalah lapisan yang menjembatani objek Python/model Django dan format yang bisa dikirim lewat jaringan (biasanya JSON)
    1) serialisasi: model/queryset → tipe data primitif → JSON (untuk respons)
    2) Deserialisasi: JSON → tipe data Python tervalidasi → objek/model (untuk request).
    3) Validasi: memeriksa tipe, panjang, keunikan

3.  Autentikasi vs Otorisasi

Perbedaan               Autentikasi (Authentication)                Otorisasi (Authorization)
Pertanyaan              basically, siapa kamu?                      apa yang boleh kamu lakukan?
Hasil                   Mengisi request.user dan request.auth       Mengizinkan atau menolak akses
komponen DRF            authentication_classes                      permission_classes
respons gagal           401 Unauthorized                            403 Forbidden

4.  SessionAuthentication mengandalkan cookie sesi (sessionid) yang dikirim otomatis oleh browser pada setiap request ke domain tersebut,
    termasuk request yang dipicu situs lain. Contoh dasar serangan CSRF:
    1) Pengguna login di bank.com
    2) Ia membuka cesillia.com, yang berisi form/skrip hidden: POST/bank.com/api/transfer
    3) Browser menyertakan cookie sesi secara otomatis, sehingga server mengira itu permintaan sah pengguna

    Token CSRF memutuf serangan ini karena  nilainya tidak dapat dibaca oleh website lain
    karena itu DRF perlu CSRF untuk metode yang mengubah data

AI Disclosure: Saya memakai LLM Claude dan Gemini sebagian besar untuk mengurus style.css, sisanya berupa menganalisis mengapa kode buatan saya error dan mengkoreksi secara manual sesuai dengan saran AI.
