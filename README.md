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

AI Disclosure: Saya memakai LLM Claude dan Gemini sebagian besar untuk mengurus style.css, sisanya berupa menganalisis mengapa kode buatan saya error dan mengkoreksi secara manual sesuai dengan saran AI.
