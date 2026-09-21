Name : Ihsan Rafi Ahmad

NPM : 2506611326

Class : PBP F

# 🚀 Cara Menjalankan Proyek Django

Panduan ini menjelaskan langkah-langkah untuk menyiapkan dan menjalankan proyek Django ini secara lokal.

## 📋 Prasyarat

Pastikan hal-hal berikut sudah terpasang di komputer kamu:

- Python 3.10 atau lebih baru
- pip (biasanya sudah ikut terpasang dengan Python)
- Git (opsional, untuk clone repository)

## 🔧 Instalasi

### 1. Clone Repository

```bash
git clone https://github.com/8ijaan/myportofolio.git
```

### 2. Buat Virtual Environment

Virtual environment digunakan agar dependency proyek tidak bercampur dengan instalasi Python global.

```bash
python -m venv env
```

Aktifkan virtual environment:

**Windows**
```bash
env\Scripts\activate
```

**macOS / Linux**
```bash
source env/bin/activate
```

### 3. Install Dependency

```bash
pip install -r requirements.txt
```

### 4. Buat Superuser (Opsional)

Diperlukan jika ingin mengakses halaman admin Django.

```bash
python manage.py createsuperuser
```

### 5. Jalankan Server

```bash
python manage.py runserver
```

Server akan berjalan di `http://127.0.0.1:8000/`.

### TUGAS 1

1. In Tutorial 1 and Individual Assignment 1, you were given the freedom to decide your portfolio website’s design. When you designed the HTML structure you used, did you use semantic HTML5 elements such as <section>, <article>, or <aside>? If so, how did those elements help you build the static web? If not, why did your design’s needs stay met without them?

Penggunaan elemen semantik seperti section, article atau aside itu memiliki fungsi readability bagi developer dari website tersebut, penggunaan elemen tersebut opsional tapi akan membantu readability.

2. When you set up your CSS to stay responsive, what layout challenges did you encounter? How did you evaluate which elements needed to be repositioned or prioritized in size when moving from the desktop view to mobile?

Tantangan utamanya adalah penyesuaian ukuran dan penempatan elemen-elemen agar terlihat bagus di mobile

3. The website you’ve built right now is a purely static web. What limitations did you feel while trying to present your portfolio’s information optimally? Based on those limitations, what dynamic functionality would you most want to prepare and add in the next iteration of the project?

Saya mencoba untuk membuat carousel myskills saya untuk infinite loop, namun hal tersebut mustahil dengan pure html & css dan memerlukan bantuan script


### TUGAS 2

1. Jelaskan apa yang terjadi ketika pengguna membuka halaman portofolio baru, mulai dari request yang diterima oleh project hingga data muncul di browser. Dalam jawabanmu, jelaskan peran dari urls.py milik project, urls.py milik aplikasi, view, model, dan template.

Ketika pengguna pertama kali membuka halaman portofolio baru, request pertama kali diterima oleh urls milik portofolio. Kemudian, request diteruskan ke urls milik aplikasi, dalam kasus saya adalah "main", yang tujuannya untuk mencocokkan url path dan memicu fungsi python untuk halaman tersebut.
Selanjutnya, view memproses request dan menentukan data apa saja yang dibutuhkan untuk halaman tersebut. Model mengambil data dari database dan mengembalikannya ke view.
View mengemas data dari database tersebut dan mengirimkannya ke template. Template engine kemudian mengubah data mentah ini menjadi file HTML.

2. Mengapa data untuk bagian portofolio baru sebaiknya disimpan dalam model, bukan ditulis langsung di dalam template? Jelaskan bagaimana pilihan ini memengaruhi maintenance aplikasi dan pengembangan ke depannya.

Data disimpan dalam model, bukan ditulis langsung di template, karena hal ini membuat template lebih bersih dan tidak mengharuskan kita menggali banyak baris HTML hanya untuk memperbarui data. Pilihan ini saja sudah memberikan banyak manfaat untuk pengembangan ke depannya. Misalnya, jika ingin memperbarui data, dengan Django kita bisa mengelolanya melalui dashboard bawaan (built-in admin).
Dengan menggunakan dashboard bawaan tersebut, kita tidak perlu langsung mengubah template dan berpotensi merusak tata letak (layout) halaman.

3. Apa perbedaan antara makemigrations dan migrate di Django? Berikan contoh perubahan pada model yang mengharuskan kita menjalankan kedua perintah tersebut.

makemigrations memeriksa models.py untuk mencari perubahan dan mengubahnya menjadi blueprint yang disimpan di dalam folder migration.
migrate mengambil blueprint tersebut dan mengeksekusinya ke database sesungguhnya, menjalankan perintah untuk membuat atau mengubah tabel.

Mari kita ambil contoh potongan kode dari codebase saya sendiri

``` python
class Skill(models.Model): 
    ...
    def logo_url(self):
        return f"/static/img/skills/{self.name.lower()}.svg"
    ...
```

Misalkan saya ingin bisa menyimpan url gambar langsung di dalam database, alih-alih di dalam folder static img, sehingga saya membuat field baru bertipe URLField bernama "thumbnail".

``` python
class Skill(models.Model): 
    ...
    thumbnail = models.URLField(blank=True, null=True)
    ...
```

makemigrations memindai perubahan tersebut dan menerjemahkannya menjadi blueprint agar migrate bisa mengeksekusinya ke database saya. Sekarang saya bisa menyimpan URL gambar ke dalam database saya.

### TUGAS 3: REFLEKSI
1. Explain why we use Django’s ModelForm instead of creating HTML forms manually. Additionally, explain why we are required to add {% csrf_token %} to these forms!

Kita menggunakan Django's ModelForm daripada membuat form HTML secara manual karena hal ini membuat kode jauh lebih bersih dan efisien, serta secara otomatis menghubungkan field form dengan model database kita tanpa harus menulis ulang validasi satu per satu. Pilihan ini saja sudah memberikan banyak manfaat untuk pengembangan ke depannya, seperti meminimalisir potensi error dan menghemat waktu penulisan kode. Selain itu, kita wajib menambahkan {% csrf_token %} ke dalam form tersebut untuk melindungi aplikasi dari serangan Cross-Site Request Forgery (CSRF), di mana token unik ini memastikan bahwa request POST yang dikirim benar-benar berasal dari pengguna yang sah di dalam situs kita, bukan dari pihak luar yang berbahaya

2. In Tutorial 03, we discussed JSON and XML data formats. Why is JSON preferred in modern web application development compared to XML?

JSON lebih disukai dalam pengembangan aplikasi web modern dibandingkan XML karena strukturnya yang jauh lebih ringan, ringkas, dan sangat mudah dibaca oleh manusia maupun diproses oleh komputer. Pilihan ini saja sudah memberikan banyak manfaat untuk performa jaringan karena ukuran file JSON yang lebih kecil membuat proses transfer data dari server ke klien menjadi lebih cepat. Selain itu, JSON terintegrasi secara langsung dengan JavaScript, sehingga data dapat langsung digunakan tanpa memerlukan parser tambahan yang rumit seperti pada XML.

3. Explain the flow that occurs when you use a view function to return your portfolio data in JSON format. Why do we need to perform the serialization process on Django models before returning the data?

Alur yang terjadi ketika kita menggunakan fungsi view untuk mengembalikan data portofolio dalam format JSON dimulai saat klien mengirimkan request ke URL tertentu, kemudian view fungsi akan mengambil data dari model database, mengubahnya melalui proses serialization menjadi format teks yang kompatibel (seperti JSON), lalu mengembalikannya sebagai HttpResponse. Kita perlu melakukan proses serialisasi terlebih dahulu pada model Django karena objek model Django merupakan objek kompleks berbasis Python yang tidak bisa langsung dibaca atau dikirim melalui protokol HTTP dalam bentuk teks mentah. Pilihan ini saja sudah memberikan banyak manfaat untuk memastikan data dari database dapat diterjemahkan dengan sempurna ke format standar yang dapat dipahami oleh berbagai platform atau frontend.

### AI DISCLOSURE
Tools AI yang digunakan: Gemini, Claude.

Bagaimana saya menggunakan AI:
- Mempelajari flow MVT
- Mencari tutorial untuk beberapa fitur css seperti layout, animasi, gradasi, dll (coding masih tetap saya lakukan secara manual)
- Mencari cara menata README.md dengan baik
- Menanyakan commit messages yang appropriate terhadap apa yang saya ubah/tambahkan pada code.
- Mencari akar permasalahan apabila terjadi error.
- Mempelajari flow dari Form & Data Delivery dalam Django


Catatan Tambahan: Saya tidak menggunakan AI untuk mengubah codebase secara langsung. Semua perubahan pada codebase dilakukan secara manual oleh saya sendiri.