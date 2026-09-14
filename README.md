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

