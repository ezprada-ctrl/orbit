# Panduan Operasional
## Forum Konsultasi Antar-Daerah — Sesi Berbagi Praktik Pendapatan Daerah

Panduan pengoperasian aplikasi di kelas. Disusun untuk PTP (operator) dan WI (pemandu).
Dokumen ini bisa dicetak dan ditaruh di sebelah laptop.

> **Belum punya aplikasinya?** Unduh di sini:
> **https://github.com/ezprada-ctrl/orbit/releases/latest**
> Klik `ORBIT.zip`, ekstrak ke folder mana saja di laptop, lalu ikuti Bagian 0 di bawah.
>
> **Sudah punya, tapi mau pastikan versi terbaru?** Klik dua kali
> `ORBIT-update.bat` di folder yang sama. Data peserta dan arsip Liga Inovasi
> tidak ikut terhapus — hanya berkas aplikasinya yang diperbarui.
>
> **Malas buka folder tiap mau update?** Klik dua kali `ORBIT-buat-shortcut-update.bat`
> **sekali saja** — muncul ikon baru **"Update ORBIT"** di Desktop. Sesudah itu,
> tinggal klik dua kali ikon itu kapan saja untuk menarik versi terbaru,
> tanpa perlu buka folder ini lagi.
>
> **Paling praktis: tanpa keluar dari aplikasi sama sekali.** Selama aplikasi
> terbuka di browser (lewat `ORBIT-execute.bat`), tekan **Ctrl+Shift+U**.
> Sistem otomatis menarik versi terbaru, memasangnya, menyalakan ulang server,
> lalu memuat ulang halaman sendiri. Jendela hitam boleh berkedip sebentar —
> jangan ditutup sampai halaman terbuka lagi.

---

## Daftar Isi

1. [Sebelum kelas mulai](#1-sebelum-kelas-mulai-15-menit)
2. [Siapa pegang apa](#2-siapa-pegang-apa)
3. [Membuka sesi](#3-membuka-sesi)
4. [Putaran satu masalah](#4-putaran-satu-masalah-inti-sesi)
5. [Dua cara memasukkan tanggapan](#5-dua-cara-memasukkan-tanggapan)
6. [Soal Dikte: apa yang terjadi saat peserta bicara](#6-soal-dikte-apa-yang-terjadi-saat-peserta-bicara)
7. [Giliran Widyaiswara](#7-giliran-widyaiswara)
8. [Kalau salah](#8-kalau-salah)
9. [Menutup sesi](#9-menutup-sesi)
10. [Kalau ada masalah](#10-kalau-ada-masalah)
11. [Pantangan](#11-pantangan)
12. [Daftar tombol cepat](#12-daftar-tombol-cepat)
13. [Liga Inovasi](#13-liga-inovasi)
14. [Mode Standar](#14-mode-standar-notulen-tanpa-gamifikasi)
15. [Layar Panggung, Pengumuman Peringkat & Peta](#15-layar-panggung-pengumuman-peringkat--peta)
16. [Cek Siap Kelas & Penilaian Sesi](#16-cek-siap-kelas--penilaian-sesi)

---

## 0. Cara membuka aplikasi — ini menentukan dikte jalan atau tidak

**Klik dua kali `ORBIT-execute.bat`.** Akan muncul jendela hitam, lalu browser terbuka sendiri.

> **Jendela hitam itu jangan ditutup** selama sesi berlangsung. Menutupnya =
> mematikan aplikasi. Setelah sesi selesai, barulah ditutup.

### Kenapa tidak boleh klik dua kali file HTML-nya langsung?

Kalau dibuka langsung, alamatnya jadi `file://`. Pada alamat itu browser
**tidak menyimpan izin mikrofon** — izinnya ditanyakan berulang kali, dan tiap
pertanyaan memutus rekaman di tengah jalan. Inilah penyebab dikte yang mati
sendiri setelah beberapa menit.

Lewat `ORBIT-execute.bat`, alamatnya jadi `localhost`. Izin mikrofon cukup diberikan
**sekali** dan tersimpan seterusnya.

Kalau aplikasi terlanjur dibuka dari file, akan muncul kotak peringatan kuning
di bagian atas layar. Fitur lain tetap normal — **hanya dikte** yang bermasalah.

---

## 1. Sebelum kelas mulai (15 menit)

- [ ] **Colok mic eksternal** ke laptop
- [ ] Cek di Windows: tekan `Win + R` → ketik `ms-settings:sound` → bicara, pastikan bar indikatornya bergerak
- [ ] Matikan **Audio Enhancements** di properti mikrofon (fitur ini sering memotong awal kalimat)
- [ ] **Jalankan lewat `ORBIT-execute.bat`** (klik dua kali) — jangan klik ganda file HTML-nya
- [ ] Tekan **Ctrl+Shift+R** sekali, untuk memastikan yang terbuka versi terbaru
- [ ] **Pastikan internet nyala.** Dua hal butuh internet: tombol Dikte, dan unduh PDF
- [ ] Klik tombol **Dikte** sekali, lalu klik **Allow** saat browser bertanya. Cukup sekali, tidak ditanya lagi
- [ ] Coba dulu pakai tombol **"Data Contoh"** — lihat tampilannya saat penuh, biar tidak kaget di depan kelas
- [ ] Lalu klik **"Sesi Baru"** untuk mengosongkan. Kelas harus mulai dari nol
- [ ] **Atur tema**: ikon matahari/bulan di pojok kanan atas. Ruangan gelap → mode gelap. Ruangan terang → mode terang
- [ ] Colok proyektor, cek tulisan terbaca dari bangku paling belakang
- [ ] **Terakhir: klik Cek Siap Kelas** (layar pembuka atau dashboard). Semua hijau = siap. Yang kuning/merah punya tombol perbaikan (lihat Bagian 16)

---

## 2. Siapa pegang apa

| Peran | Tugas |
|---|---|
| **PTP** | Duduk di laptop. Mengetik dan menekan tombol. Tidak perlu ikut memikirkan isi |
| **WI** | Berdiri memandu. Mengatur siapa bicara, dan menutup dengan kesimpulan |
| **Peserta** | Memegang mic saat bicara, lalu mengoper ke penanggap berikutnya |

> **Aturan emas: satu orang bicara satu waktu.**
> Kalau dua orang bicara bersamaan, hasil dikte suara hancur total.

---

## 3. Membuka sesi

1. Klik **"Mulai Sesi"**
2. Muncul dashboard — ini "rumah". Sepanjang sesi Anda akan bolak-balik ke sini
3. Di pojok kanan atas ada saklar **PTP | WIDYAISWARA**. Sekarang yang menyala PTP

---

## 4. Putaran satu masalah (inti sesi)

Ulangi langkah ini untuk tiap pejabat yang mengangkat masalah.

### Langkah 1 — Catat masalahnya

1. Klik **"+ Angkat Masalah Baru"**
2. **Kolom daerah**: ketik **3 huruf** saja, misal `sur` → tekan **panah bawah** → **Enter**.
   Kursor pindah sendiri ke kolom judul
3. **Judul**: tulis pendek, 5–8 kata. Ini yang muncul di daftar riwayat dan jadi tajuk di PDF
4. **Uraian**: ketik, atau klik **Dikte** dan biarkan pejabatnya bercerita
5. Klik **"Simpan & Buka untuk Tanggapan"**

### Langkah 2 — Kumpulkan tanggapan

- Di atas layar muncul **Sasaran Babak: tanggapan dari 3 daerah berbeda**
- Angka di kanan menunjukkan progres: `0 dari 3` → `1 dari 3` → dan seterusnya
- Isi tanggapan satu per satu (lihat bagian 5 untuk pilihan caranya)
- Begitu sasaran tercapai, panel berubah hijau dan tombol besar mulai berdenyut — tanda forum siap disimpulkan

> **Sasaran ini tidak mengunci.** Kalau cuma dapat 2 daerah, tetap boleh lanjut.

### Langkah 3 — Serahkan ke WI

1. Klik **"Alihkan ke Widyaiswara untuk Kesimpulan"**
2. Layar berubah hijau, muncul tulisan besar **"MODE WIDYAISWARA AKTIF"**
3. Mulai detik itu, PTP berhenti mengetik. Giliran WI

---

## 5. Dua cara memasukkan tanggapan

Pilih sesuai keadaan. Keduanya bisa dicampur dalam satu sesi.

### Cara A — Ketik (selalu jalan, tanpa syarat apa pun)

1. Kolom daerah: 3 huruf → panah bawah → Enter → kursor pindah sendiri
2. Kolom isi: ketik singkat, satu kalimat
3. Tekan **Ctrl+Enter** → tersimpan, kursor balik ke kolom daerah, siap untuk penanggap berikutnya

Tidak perlu menyentuh mouse sama sekali.

### Cara B — Dikte (paling cepat, butuh internet)

1. Pilih daerahnya dulu
2. Klik **Dikte**. Tombol menyala hijau dan berdenyut — artinya sedang merekam
3. Pejabat bicara. Tulisan masuk sendiri ke kolom, kalimat demi kalimat
4. Di bawah kolom ada **baris abu-abu miring** — itu kata yang sedang didengar,
   belum masuk kolom. Anggap saja jendela intip, bukan hasil akhir
5. **Anda boleh menyunting sambil dikte jalan.** Klik kata mana pun di tengah,
   betulkan, kursor tetap di tempat Anda menaruhnya
6. Klik **Dikte** lagi untuk berhenti
7. Hapus bagian yang bertele-tele, sisakan satu kalimat inti
8. Tekan **Ctrl+Enter**

> **Trik paling berguna:** minta tiap penanggap **menyebut nama daerahnya lebih dulu**
> sebelum bicara — *"Kabupaten Sleman. Di tempat kami..."*
> Dengan begitu nama daerahnya ikut terekam dan PTP tidak perlu menebak.

---

## 6. Soal Dikte: apa yang terjadi saat peserta bicara

**Ya — tulisannya masuk otomatis sambil orangnya masih bicara.**
Tidak perlu menunggu dia selesai.

Ada dua lapis yang perlu Anda bedakan:

| Yang Anda lihat | Artinya |
|---|---|
| Teks di dalam **kolom isian** | Sudah final, sudah masuk, boleh disunting |
| **Baris abu-abu miring di bawah kolom** | Sedang didengar, belum final. Berubah-ubah. Jangan diutak-atik |

Pemisahan ini disengaja. Kalau kata yang belum final ikut ditaruh di dalam kolom,
ekornya ditulis ulang terus-menerus dan kursor akan terus terlempar ke ujung —
kolomnya jadi tidak bisa disunting sama sekali selama dikte berjalan.

### Yang aplikasi lakukan

- ✅ Menulis otomatis ke kolom, **langsung saat orang bicara**
- ✅ Menyambung terus meski ada jeda napas (tidak putus tiap kalimat)
- ✅ **Boleh disunting sambil dikte jalan.** Klik kata di tengah, betulkan —
  kursor tetap di tempat Anda menaruhnya, tidak ketarik ke ujung
- ✅ Suntingan manual Anda **tidak akan tertimpa** kata yang masuk berikutnya
- ✅ Kalau kursor sedang di ujung, kata baru mengalir di ujung seperti mengetik biasa

### Yang aplikasi TIDAK lakukan

- ❌ **Tidak menyimpan sendiri.** Tulisannya muncul, tapi tetap harus Anda tekan **Ctrl+Enter**
- ❌ **Tidak tahu siapa yang bicara.** Nama daerah tetap Anda yang pilih
- ❌ **Tidak mendengarkan ruangan terus-menerus.** Hanya merekam selama tombol Dikte menyala
- ❌ **Tidak memisahkan pembicara.** Kalau dua orang bicara, keduanya tercampur jadi satu tulisan
- ❌ **Tidak merapikan kalimat.** Yang keluar adalah apa adanya ucapan, termasuk yang bertele-tele

### Kesimpulannya

Ini **bukan notulis otomatis**. Ini **tekan-bicara per orang**:

```
PTP tekan Dikte  →  peserta bicara  →  tulisan muncul  →
PTP tekan Dikte lagi  →  PTP rapikan  →  Ctrl+Enter
```

Kerja PTP berubah dari **mengetik** menjadi **memangkas**. Jauh lebih ringan,
tapi tetap ada pekerjaannya.

### Istilah teknis dibetulkan otomatis

Mesin pengenal suara selalu salah pada singkatan yang sama — ia mengejanya
secara bunyi, misalnya "be pe ha te be" untuk BPHTB. Aplikasi membetulkannya
sendiri setelah teks masuk.

Yang sudah dikenali: `BPHTB` `PBB-P2` `PBJT` `SPTPD` `SPPT` `NJOP` `opsen`
`Bapenda` `Samsat` `BPN` `OSS` `PAD` `BUMD` `DJP` `APKD` `Widyaiswara`
`Kemenkeu` `tapping box` `e-billing`.

Kalau ada istilah lain yang sering salah di kelas Anda, catat bentuk salahnya
dan minta ditambahkan — daftarnya ada di bagian `KAMUS_ISTILAH` dalam file HTML.

### Nama daerah terisi sendiri

Kalau penanggap **menyebut daerahnya lebih dulu** — *"Kabupaten Sleman. Di
tempat kami..."* — aplikasi mengenali nama itu, mengisi kolom daerah otomatis,
lalu membuangnya dari isi tanggapan supaya tidak tertulis dua kali.

Syaratnya: kolom daerah masih kosong, dan namanya tidak ambigu. "Sleman" saja
cukup. "Bandung" tidak dipakai karena ada Kota Bandung, Kabupaten Bandung, dan
Kabupaten Bandung Barat — dalam kasus begitu Anda tetap memilih sendiri.

### Kalau dikte berhenti sendiri

Chrome **rutin memutus** sesi pengenalan suara — setelah hening beberapa detik,
setelah sekitar semenit bicara, atau saat jaringan berkedip. Ini normal dan
tidak bisa dicegah.

Aplikasi menyambungnya kembali sendiri. **Anda tidak perlu melakukan apa pun** —
tombolnya tetap hijau pekat dan tulisan tetap masuk.

Di baris abu-abu bawah kolom ada **penghitung waktu** (`Mendengarkan… · 03:42`).
Angka itu terus berjalan selama dikte hidup — jadi sekali lihat, Anda tahu
mikrofonnya masih bekerja. Kalau sesekali berubah jadi `Menyambung ulang…`,
itu normal: aplikasi sedang membangun sesi baru, dan akan kembali sendiri.

Kalau sambungannya gagal lima kali beruntun (biasanya internet benar-benar mati),
barulah dikte menyerah. Tandanya:

- Tombol Dikte padam
- Di bawah kolom muncul tulisan menetap: **"Dikte terputus — periksa koneksi
  internet, lalu klik Dikte lagi."**

Tulisan itu sengaja dibuat **menetap**, tidak hilang sendiri — supaya tidak
terlewat saat Anda sedang menatap pembicara.

**Teks yang sudah masuk tetap aman.** Klik Dikte lagi untuk melanjutkan.

---

## 7. Giliran Widyaiswara

1. Di layar sudah tersedia ringkasan masalah dan seluruh tanggapan — WI tinggal membaca
2. Ketik kesimpulan di kotak besar, atau klik **Dikte** dan WI bicara saja
3. Klik **"Simpan Kesimpulan & Kembali ke PTP"**
4. Muncul layar **"TERSIMPULKAN"** dengan tanda centang selama 3 detik, lalu kembali sendiri ke dashboard
5. Kalau buru-buru, klik saja layarnya supaya langsung lewat

Kendali otomatis kembali ke PTP. Siap untuk masalah berikutnya.

---

## 8. Kalau salah

| Masalah | Cara memperbaiki |
|---|---|
| Tanggapan salah ketik | Arahkan mouse ke kartunya, klik tanda **×** di pojok kanan |
| Nama daerah / judul salah | Dari dashboard, klik baris masalahnya → **"Ubah / hapus"** |
| Nama daerah salah ketik di banyak tempat | Saat mengubah nama, aplikasi menawarkan *ganti di seluruh sesi* — jawab **OK** |
| Tombol simpan seperti tidak berfungsi | Ada kolom wajib yang kosong. Kolom itu akan **bergetar dan disoroti merah**, lalu layar menggulir ke sana. Isi kolomnya, simpan lagi |
| Terlanjur keluar dari pembahasan | Di dashboard, tombol biru **"Lanjutkan: (judul masalah) →"** ada paling atas, tepat di bawah angka |
| Tersesat di layar mana pun | Tombol **"Dashboard"** selalu ada di pojok kanan atas |
| WI terlanjur masuk tapi belum siap | Klik **PTP** di saklar. Draf yang sudah diketik tidak hilang |
| Browser ter-refresh / laptop hang di tengah pembahasan | Buka lagi. Aplikasi langsung kembali ke pembahasan yang sedang berjalan; draf kesimpulan WI yang sedang diketik ikut tersimpan |
| Lupa klik **Catat** lalu langsung alihkan ke WI | Aplikasi menahan dan bertanya — jawab **OK** supaya tanggapan itu ikut tercatat sebelum WI menyimpulkan |
| PDF gagal diunduh karena internet sempat mati | Nyalakan internet, klik tombol PDF lagi — tidak perlu muat ulang halaman |

---

## 9. Menutup sesi

1. Di dashboard, klik **"Tutup Sesi & Tampilkan Hasil"**
2. Layar penutupan muncul: jaring forum digambar ulang dari nol, angka capaian, dan daftar seluruh kesimpulan
3. **Biarkan ini tampil di proyektor.** Inilah momen peserta melihat apa yang mereka bangun bersama
4. Klik **"Unduh Risalah Lengkap (PDF)"**
5. Untuk PDF per daerah: **"Rekap per Daerah →"** → pilih daerah di dropdown → unduh

---

## 10. Kalau ada masalah

| Kejadian | Yang terjadi | Lakukan |
|---|---|---|
| Browser ter-refresh tak sengaja | **Data aman**, tersimpan otomatis | Lanjutkan saja |
| Internet mati | Dikte mati, **PDF tidak bisa diunduh** | Catat dengan mengetik biasa. Unduh PDF setelah internet nyala |
| Mic tidak tertangkap | Tombol Dikte tidak jalan | Pakai ketik biasa. Jangan buang waktu membetulkan di depan kelas |
| Tombol Dikte tidak muncul | Browser tidak mendukung | Pakai Chrome atau Edge |
| Dikte banyak salah | Wajar, terutama singkatan | Betulkan manual. Tetap lebih cepat daripada mengetik dari nol |
| Dikte berhenti sendiri | Chrome rutin memutus sesi | **Tidak perlu apa-apa** — aplikasi menyambung sendiri dalam sekejap |
| Muncul "Dikte terputus" di bawah kolom | Gagal menyambung 5× beruntun, biasanya internet | Klik tombol **Dikte** lagi. Teks yang sudah masuk tetap aman |
| Peserta bicara bersamaan | Hasil dikte kacau | WI menegur: satu-satu |
| Laptop mati | Data tersimpan di browser | Nyalakan, buka alamat yang sama, data kembali |
| Pakai laptop lain / laptop baru, `ORBIT-execute.bat` bilang "Python tidak ditemukan" | Aplikasi tetap terbuka langsung dari berkas HTML — **Dikte tidak stabil**, fitur lain normal | Kalau perlu Dikte stabil, minta IT pasang Python dari python.org (centang "Add to PATH" saat instal), lalu jalankan `ORBIT-execute.bat` lagi |
| `ORBIT-execute.bat` bilang "Port 8200 sudah dipakai" | Aplikasi sudah jalan di jendela hitam lain (mungkin belum ditutup dari sesi sebelumnya) | Cari jendela hitam yang sudah terbuka dan pakai itu, atau tutup dulu baru jalankan lagi |
| Windows bertanya izin jaringan untuk Python | Wajar saat pertama kali dijalankan di laptop itu | Pilih **Allow / Izinkan** untuk jaringan **Private** — kalau ditolak, bid HP peserta tidak akan tersambung |

---

## 11. Pantangan

- ❌ **Jangan klik "Sesi Baru" sebelum PDF diunduh.** Semua data hilang permanen, tidak bisa dikembalikan
- ❌ **Jangan buka lewat klik ganda file** kalau mau pakai Dikte. Harus lewat `localhost`
- ❌ **Jangan kejar verbatim.** Cukup satu kalimat inti per penanggap. Transkrip lengkap justru membuat risalah jadi jelek
- ❌ **Jangan biarkan dua orang bicara bersamaan** saat Dikte menyala
- ❌ **Jangan tutup tab browser** sebelum PDF selesai diunduh
- ❌ **Jangan klik "Mulai kelas baru"** di Liga Inovasi sebelum Excel liga diunduh (lihat bagian 13)

---

## 12. Daftar tombol cepat

| Tombol | Fungsi |
|---|---|
| `3 huruf` + `↓` + `Enter` | Pilih daerah, kursor pindah ke kolom berikutnya |
| `Ctrl + Enter` | **Simpan** — berlaku di ketiga babak: simpan masalah, simpan tanggapan, simpan kesimpulan |
| `Esc` | Tutup jendela detail / lewati layar "Tersimpulkan" |
| `Ctrl + Shift + R` | Muat ulang paksa (pakai ini kalau aplikasi terasa versi lama) |
| `Win + R` → `ms-settings:sound` | Buka pengaturan suara Windows |

---

## 13. Liga Inovasi

Lapisan kompetisi di atas forum. Alur forum **tidak berubah** — Liga hanya
menyisipkan dua langkah: **bid** sebelum tanggapan, dan **pemilihan pemenang**
sebelum kesimpulan WI.

### Aturan singkat

| | |
|---|---|
| Pemilik masalah | Peserta yang mengangkat masalah. **Tidak bisa bid** di masalahnya sendiri |
| Bidder | Peserta lain yang mau menjawab. Kirim nama (pilih dari daftar) + keypoint jawaban |
| Pemenang | Dipilih pemilik masalah — boleh lebih dari satu, boleh juga tidak ada |
| Skor | Ada pemenang: tiap pemenang **+3**, bidder lain **−1**. Tidak ada pemenang: semua bidder **0** |
| Peringkat | Skor tertinggi; kalau sama, yang **paling banyak bid** menang |

### Sebelum kelas (sekali per kelas)

1. Dashboard → **Liga Inovasi** → tab **Daftar Peserta**
2. Isi **nama kelas** (mis. `Angkatan II · Kelas B`) — ini nama arsipnya nanti
3. Impor Excel berkolom **nama | daerah**. Tanpa internet: salin dua kolom itu di
   Excel, tempel di kotak tempelan, klik **Tambahkan dari tempelan**
4. Salah ejaan nama? Klik **Ubah** — semua bid orang itu ikut, tidak pecah
5. Nama daerah diseragamkan otomatis ke nama wilayah resmi (`Jawa Barat` → `Provinsi Jawa Barat`,
   `DKI Jakarta`, `Kab. Sleman`, `Jatim`, dst.). Yang ambigu atau tidak dikenal (mis. `Bandung`)
   ditandai **merah** di tabel peserta — klik **Ubah** dan tulis lengkap (`Kota Bandung`)

### Putaran satu masalah

1. Angkat masalah seperti biasa → masuk layar tanggapan
2. Di kartu oranye **Liga Inovasi** → **Buka Jendela Bid**. Pemilik masalah terisi
   otomatis bila hanya ada satu peserta dari daerah itu (tautan **ganti** tersedia);
   bila ada beberapa atau tidak ada yang cocok, ketik namanya di kolom cari
3. QR dan alamat muncul. Peserta memindai dengan HP (WiFi yang sama dengan laptop),
   pilih namanya, tulis keypoint, kirim. Bid masuk sendiri ke layar dalam 2 detik.
   **Tampilkan QR besar** untuk proyektor
4. Peserta yang tidak pakai HP: PTP catat di **Catat bid manual** (pilih nama, ketik keypoint, Ctrl+Enter)
5. Klik **Tutup Jendela Bid → Presentasi Jawaban**. Mulai detik ini HP tidak bisa bid lagi
6. Tiap bidder bicara: klik **Giliran bicara** pada kartunya → daerahnya terisi
   sendiri di kolom tanggapan → catat tanggapan seperti biasa (dikte/ketik, Ctrl+Enter).
   Tanggapan itu otomatis tertaut ke bid-nya
7. Pemilik masalah menyebut jawaban yang paling relevan → PTP **centang** → **Tetapkan Pemenang**.
   Tidak ada yang pas? Klik **Tidak ada yang relevan** (tidak ada yang kehilangan poin)
8. Baru sekarang **Alihkan ke Widyaiswara**. Aplikasi menolak masuk mode WI
   selama pemenang belum ditetapkan

> Salah tetapkan? Kartu hijau punya tombol **Ubah penetapan**.

### HP masuk dari jaringan apa pun

QR mengarah ke **alamat internet** (`https://….trycloudflare.com/bid`) yang dibuka
otomatis oleh `cloudflared.exe` saat `ORBIT-execute.bat` dijalankan. HP peserta cukup
punya internet — WiFi diklat, WiFi lain, atau data seluler — tidak perlu satu
jaringan dengan laptop.

- Alamatnya **berganti tiap kali** `ORBIT-execute.bat` dijalankan. Tidak masalah: QR selalu dibuat ulang
- Siapnya sekitar **15 detik** setelah jendela hitam terbuka. Kalau jendela bid dibuka lebih cepat,
  QR sementara memakai alamat lokal lalu **berganti sendiri** begitu alamat internet siap
- Dari internet hanya halaman bid yang bisa dibuka. Buka/tutup jendela, daftar bid, dan arsip tetap khusus laptop
- Menutup jendela hitam ikut mematikan alamat internet itu
- Jendela hitam **tidak sengaja tertutup** saat bid terbuka? Jalankan lagi `ORBIT-execute.bat` —
  dalam beberapa detik jendela bid pulih sendiri dan bid dari HP kembali masuk
- `ORBIT-execute.bat` diklik dua kali? Jendela kedua menolak jalan dengan pesan jelas — pakai yang pertama
- `cloudflared.exe` wajib ada di folder yang sama dengan `ORBIT-execute.bat`

### Kalau internet / HP bermasalah

Tidak perlu apa-apa selain beralih ke **catat bid manual**. Liga tetap jalan penuh
dari laptop saja — HP hanya jalur tambahan, bukan syarat.

Pertama kali `ORBIT-execute.bat` dijalankan, Windows bisa bertanya soal izin jaringan
untuk Python — pilih **Allow / Izinkan** untuk jaringan **Private**. Kalau terlanjur
ditolak, HP tidak bisa masuk, tapi aplikasi di laptop tetap normal.

### Durasi liga

Atur sekali di awal: Dashboard → **Liga Inovasi** → **Daftar Peserta** → **Durasi liga**.

- **1** = game dimainkan satu sesi lalu langsung selesai (rencana saat ini: hari ke-3 saja)
- **2, 3, …** = skor terakumulasi lintas hari; peringkat akhir diumumkan di hari terakhir

### Papan peringkat

Dashboard → **Liga Inovasi** → **Papan Peringkat** → **Layar penuh**.
Bila liga lebih dari satu hari, tampilkan tiap akhir hari.

- **Top 3** tampil dengan angka skor (hanya skor positif yang naik podium). Penentu seri: skor → jumlah bid → paling sering terpilih.
  Yang **seri penuh** (ketiganya sama) naik podium bersama — tidak ada yang tersingkir karena urutan abjad
- Sisanya tampil **nama saja**, tanpa angka, disorot oranye — makin ke bawah makin terang
- Akhir sesi terakhir: klik **Umumkan Peringkat Akhir** → pengumuman dibuka bertahap (lihat Bagian 15) →
  peringkat 1 diberi keterangan *Penerima sertifikat*. Mau diulang? **Putar ulang pengumuman**
- **Tabel skor lengkap (khusus PTP)** memuat angka minus — **jangan dibuka saat proyektor menyala**

### Data liga & sertifikat

- Liga **tidak ikut terhapus** oleh "Sesi Baru" — skor menumpuk selama durasi liga
- Tiap perubahan otomatis diarsip ke folder **`arsip-liga`** di sebelah aplikasi (satu berkas JSON per kelas)
- Setelah peringkat akhir diumumkan: tab **Arsip & Ekspor** → **Unduh Excel kelas ini** → serahkan ke panitia.
  Isinya: Ringkasan (termasuk Peserta Terbaik), Peringkat, Bid per Masalah (keypoint,
  tanggapan, pemenang, poin), dan daftar Peserta
- Pindah laptop / browser terhapus: **Pulihkan dari JSON** (pakai berkas di `arsip-liga` atau JSON yang diunduh)
- Kelas berikutnya: **Mulai kelas baru** — hanya setelah Excel diunduh
- Ekspor liga **terpisah** dari PDF risalah forum. PDF tetap seperti biasa

---

## Satu kalimat untuk WI

Diucapkan tiap kali seorang penanggap selesai bicara:

> ### *"Ringkas satu kalimat — praktik apa yang Bapak/Ibu terapkan?"*

Kalimat itulah yang PTP ketik. Sisanya dibuang.

Ini **satu-satunya hal yang paling meringankan beban PTP** — dampaknya lebih besar
daripada fitur apa pun di aplikasi ini, dan sekaligus menghasilkan risalah yang lebih baik.

---

*Dokumen pendamping aplikasi `forum-konsultasi-antar-daerah.html`*

## 14. Mode Standar (Notulen tanpa Gamifikasi)

Untuk rapat, pelatihan lain, atau forum yang tidak memakai game.

- **Beralih mode:** ikon roda gigi (Setelan) di kanan atas → pilih *Mode Standar* → konfirmasi. Mode yang dipilih diingat browser.
- **Data gamifikasi dibekukan, tidak dihapus.** Forum & Liga Inovasi lanjut persis dari titik terakhir saat kembali ke Mode Gamifikasi. Tidak ada skor yang dihitung di Mode Standar. Peralihan ditolak selama jendela bid Liga masih terbuka.
- **Peserta:** tab *Peserta* → impor Excel/CSV (kolom Nama | Unit Kerja), tempel dari Excel, salin dari sesi lain, atau tambah satu per satu. Nama yang diketik saat mencatat tapi belum terdaftar otomatis jadi peserta baru (format `Nama (Unit)` ikut terbaca).
- **Mencatat:** tab *Percakapan* → pilih pembicara → ketik atau **Dikte** → Ctrl+Enter. Pembicara tetap terpilih agar ucapan panjang bisa didikte beberapa potong.
- **Transkrip luar:** bagian *Masukkan transkrip dari luar* menerima chat WhatsApp/Zoom, berkas `.vtt` Teams/Zoom, atau teks `Nama: isi`.
- **Ekspor:** tombol *Unduh PDF* / *Unduh Word* (sampul → daftar peserta → transkrip bernomor).
- **Knowledge base:** tab *Cari & Arsip* menelusuri seluruh sesi (isi, pembicara, unit, judul). Klik hasil untuk lompat ke catatannya.
- **Cadangan:** data Mode Standar hanya di browser laptop itu — rutin klik *Simpan cadangan (JSON)* ke OneDrive; *Muat cadangan* menggabungkan arsip di laptop lain.

## 15. Layar Panggung, Pengumuman Peringkat & Peta

### Layar Panggung: proyektor punya tampilannya sendiri

Laptop tetap dipakai PTP untuk mengetik. Proyektor menampilkan versi yang bersih dan besar,
yang **berganti sendiri mengikuti alur kelas**. PTP tidak perlu mengatur apa pun.

**Cara menyalakan (sekali di awal kelas):**

1. Klik ikon **layar kecil** di kanan atas (sebelah roda gigi). Jendela *Layar Panggung* terbuka.
2. Tekan **Windows + P** → pilih **Perluas** (*Extend*).
3. Seret jendela *Layar Panggung* ke layar proyektor, lalu **klik sekali** di jendela itu (otomatis layar penuh).

Titik hijau di ikon layar = proyektor sedang tersambung.

**Yang tampil di proyektor, otomatis:**

| Saat PTP… | Proyektor menampilkan |
|---|---|
| di dashboard | Peta Indonesia: daerah yang saling berbagi praktik + angka sesi |
| mencatat masalah & tanggapan | Judul masalah, tanggapan yang masuk, peta kecil yang menyorot daerah pemilik masalah |
| membuka jendela bid | QR besar, jumlah bid yang terus bertambah, kartu nama bidder, **hitung mundur** |
| presentasi jawaban | Bidder yang sedang **Giliran bicara** disorot besar |
| menetapkan pemenang | Jawaban terpilih dengan **+3** dan konfeti. Bidder lain disebut dengan ucapan terima kasih, **tanpa angka minus** |
| mengalihkan ke WI | Layar hijau "Giliran Widyaiswara" |
| WI selesai menyimpulkan | Teks kesimpulan tampil besar (sekitar 2 menit) |
| membuka Papan Peringkat | Papan peringkat (muat satu layar walau pesertanya 50) |
| Tutup Sesi | Rangkuman sesi + peta yang tergambar ulang dari awal |

**Hitung mundur bid:** di kartu *Jendela Bid Terbuka* pilih **1 / 2 / 3 / 5 menit**. Waktunya berjalan
besar di proyektor dan kecil di laptop. Saat waktu habis, jendela **tidak** tertutup sendiri; PTP tetap
yang menekan *Tutup Jendela Bid*.

**Mau menampilkan hal lain?** Klik lagi ikon layar → pilih **Otomatis**, **Peta Jejaring**,
**Papan Peringkat**, atau **Layar Jeda** (logo ORBIT, untuk sebelum mulai atau istirahat).

> Layar Panggung hanya **menampilkan**. Ia tidak pernah mengubah data. Ditutup kapan pun, tidak ada yang hilang.
> Tanpa proyektor kedua pun aplikasi tetap berjalan seperti biasa.

### Pengumuman Peringkat Akhir yang dibuka bertahap

Liga Inovasi → Papan Peringkat → **Umumkan Peringkat Akhir**. Urutannya:

1. **Pembuka**: judul besar "Peringkat Akhir" + ringkasan liga. Saatnya WI/PTP memberi pengantar.
2. **Peringkat 3** → **Peringkat 2**: kartu "?" dibuka satu per satu, skor dihitung naik.
3. **Peringkat 1**: kartu bergetar, hitung mundur **3-2-1**, lalu nama dibuka + konfeti.
4. **Papan lengkap**.

Maju ke tahap berikutnya: tombol **Lanjut**, **Spasi**, **panah kanan**, atau **clicker presentasi**.
Mundur: panah kiri. Keluar: **Esc**.

- Layar Panggung terbuka → pengumuman tampil di proyektor, laptop menampilkan panel kendali.
- Tidak ada Layar Panggung → pengumuman tampil layar penuh di laptop itu sendiri.
- Seri penuh di satu peringkat → namanya dibuka bersama dalam satu kartu. Di peringkat 1 tertulis *Seri — penentuan panitia*.

### Peta Indonesia

Di dashboard (bagian *Jaring Forum*) dan di layar penutupan ada pilihan **Jaring | Peta Indonesia**.

- **Titik hijau** = daerah pengangkat masalah. **Titik biru** = daerah penanggap.
- **Garis lengkung dengan titik yang bergerak** = praktik yang mengalir dari penanggap ke pemilik masalah.
- Klik titik hijau untuk menyorot siapa saja yang menanggapi daerah itu.
- Peta bekerja **tanpa internet**. Daerah yang namanya diketik tidak resmi (bukan dari daftar saran) tidak
  muncul di peta; aplikasi menyebutkan namanya di bawah peta supaya bisa dibetulkan.

## 16. Cek Siap Kelas & Penilaian Sesi

### Cek Siap Kelas

Tombol **Cek Siap Kelas** ada di layar pembuka dan di dashboard. Sekali klik, aplikasi memeriksa:

- dibuka lewat `ORBIT-execute.bat` atau tidak
- internet laptop
- HP peserta bisa masuk atau tidak. Ada **QR uji**: pindai dengan HP sendiri; muncul tulisan *"Jendela bid sedang tertutup"* = berhasil
- mikrofon untuk dikte (tombol **Uji mikrofon** supaya izin tidak ditanyakan di depan kelas)
- sisa data kelas sebelumnya, data contoh yang lupa dikembalikan
- daftar peserta Liga, nama kelas, nama daerah yang tidak dikenali
- Simpan Otomatis dan Layar Panggung

**Hijau** = beres. **Kuning** = catatan / opsional. **Merah** = bereskan sebelum mulai. Tiap yang belum hijau diberi tombol perbaikan.
Klik **Periksa ulang** setelah memperbaiki.

### Penilaian Sesi (skala 1–5 dari HP)

Satu pertanyaan: *"Seberapa bermanfaat sesi forum hari ini bagi pekerjaan Anda?"*. Peserta menggeser penilaian
dari **1 (tidak bermanfaat)** sampai **5 (sangat bermanfaat)**, boleh menambah satu kalimat komentar.

- **Muncul sendiri** di HP peserta begitu WI menyimpulkan masalah pertama. Tampil di halaman yang sama dengan bid
  (QR yang sama), hanya saat jendela bid sedang tertutup.
- **Sekali per orang per sesi.** Setelah mengirim, di HP itu tidak muncul lagi. Nama yang sudah menilai juga
  ditolak bila dicoba lewat HP lain.
- **Peserta yang tidak pernah bid** tetap bisa menilai lewat QR yang sama. Waktu terbaik menagihnya: saat PTP menekan
  **Umumkan Peringkat Akhir**. Bila masih ada yang belum menilai, aplikasi menahan dulu dan menawarkan
  **Tampilkan QR penilaian**. Proyektor lalu menampilkan QR besar + titik-titik yang berubah hijau satu per satu
  (tanpa nama, tanpa nilai). Setelah cukup, tekan **Umumkan sekarang**.
- Daftar nama yang **belum menilai** bisa dilihat PTP (khusus laptop, untuk diingatkan langsung).
- **Unduh Penilaian (Excel)**: di layar Penutupan Sesi atau Liga Inovasi → Arsip & Ekspor. Isinya:
  **Nama | Pemda | Penilaian (1–5)** + keterangan, komentar, tanggal, jam; ringkasan rata-rata dan sebaran nilai; daftar yang belum menilai.
  Penilaian juga ikut masuk ke Excel kelas utama (lembar *Penilaian Sesi*).
- Nilai perorangan **tidak pernah** tampil di proyektor. Di layar Penutupan Sesi hanya jumlah yang sudah menilai;
  rata-rata hanya ada di tab Arsip & Ekspor dan Excel.
- Penilaian butuh daftar peserta Liga Inovasi dan aplikasi yang dibuka lewat `ORBIT-execute.bat`.

