# -*- coding: utf-8 -*-
"""
Server ringan Forum Konsultasi Antar-Daerah + Liga Inovasi.

Menggantikan `python -m http.server`. Hanya pustaka bawaan Python (tanpa pip).

  - Laptop PTP tetap membuka http://localhost:8200/... -> izin mikrofon dikte
    tetap tersimpan seperti sebelumnya (localhost = secure context).
  - HP peserta membuka /bid lewat alamat internet (terowongan cloudflared, lihat
    TEROWONGAN) atau http://<IP-laptop>:8200/bid saat jendela bid dibuka.
  - Aksi yang MENGUBAH keadaan liga (buka/tutup jendela, arsip ke disk)
    hanya diterima dari laptop itu sendiri (127.0.0.1). HP hanya bisa
    membaca status jendela yang sedang dibuka dan mengirim bid.
  - Yang disajikan ke jaringan hanya berkas dalam daftar IZIN — folder
    project (termasuk arsip) tidak bisa dijelajah dari HP.

Keadaan jendela bid disimpan di memori saja. Sumber kebenaran tetap
aplikasi di laptop (localStorage + arsip JSON di folder arsip-liga/).
"""
import json
import os
import re
import socket
import sys
import threading
import time
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler

PORT = int(os.environ.get('FORUM_PORT', 8200))   # FORUM_PORT hanya untuk uji
AKAR = os.path.dirname(os.path.abspath(__file__))
FOLDER_ARSIP = os.path.join(AKAR, 'arsip-liga')

RILIS_ZIP_URL = 'https://github.com/ezprada-ctrl/orbit/releases/latest/download/ORBIT.zip'
BERKAS_APLIKASI = [
    'ORBIT-execute.bat', 'ORBIT-update.bat', 'ORBIT-buat-shortcut-update.bat',
    'server.py', 'forum-konsultasi-antar-daerah.html', 'bid.html', 'index.html',
    'PANDUAN-OPERASIONAL.md',
]


def salinan_pengembang():
    """Laptop pengembang (folder ini punya .git) vs laptop PTP biasa (dari ZIP rilis).
    Rilis GitHub bisa tertinggal dari commit lokal yang belum dirilis — menimpa
    salinan pengembang dengan rilis lama akan menghapus balik pekerjaan yang
    sedang berjalan. Salinan PTP tidak punya .git sama sekali, tidak terpengaruh."""
    return os.path.isdir(os.path.join(AKAR, '.git'))

IZIN = {
    '/forum-konsultasi-antar-daerah.html',
    '/bid.html',
    '/palet-pilihan.html',
}

KUNCI = threading.Lock()
JENDELA = {'buka': False}   # {buka, masalahId, judul, daerah, pemilik, peserta[], bids[], seq}
# Penilaian sesi (skala 1-5) dari HP. Satu peserta satu penilaian per tanggal;
# laptop PTP menarik 'masuk' lalu menyimpannya di data liga (sumber kebenaran).
NILAI = {'buka': False}     # {buka, tanggal, peserta[], sudah:set(id), masuk[]}


def ip_lokal():
    """Semua alamat IPv4 laptop yang mungkin dijangkau HP di jaringan kelas."""
    hasil = []
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('10.255.255.255', 1))   # tidak benar-benar mengirim paket
        hasil.append(s.getsockname()[0])
        s.close()
    except OSError:
        pass
    try:
        for ip in socket.gethostbyname_ex(socket.gethostname())[2]:
            if ip not in hasil:
                hasil.append(ip)
    except OSError:
        pass
    hasil = [ip for ip in hasil if not ip.startswith(('127.', '169.254.'))]
    # Hotspot Windows (192.168.137.x) didahulukan: WiFi kelas/kantor sering
    # memblokir HP <-> laptop (client isolation), hotspot laptop tidak.
    return sorted(hasil, key=lambda ip: not ip.startswith('192.168.137.'))


"""
TEROWONGAN PUBLIK — supaya HP bisa masuk dari jaringan APA PUN (WiFi diklat
yang memblokir antar-perangkat, data seluler, WiFi berbeda). cloudflared.exe
(rilis resmi Cloudflare, mode "quick tunnel" tanpa akun) membuka alamat
https://<acak>.trycloudflare.com yang meneruskan ke server ini. Alamatnya
baru tiap kali dijalankan; QR di aplikasi selalu mengikuti alamat terbaru.
Bila berkasnya tidak ada / internet mati, QR kembali ke IP lokal.
"""
TEROWONGAN = {'url': None, 'proses': None}


def ikat_ke_server(proses):
    """Menutup jendela hitam mematikan Python secara paksa — tanpa sempat
    menjalankan `finally`. Supaya cloudflared tidak tertinggal sebagai proses
    yatim (terowongan tetap terbuka), ia dimasukkan ke Job Object Windows
    yang otomatis mematikan anggotanya begitu server ini berhenti."""
    if os.name != 'nt':
        return
    try:
        import ctypes
        from ctypes import wintypes
        k32 = ctypes.WinDLL('kernel32', use_last_error=True)
        k32.CreateJobObjectW.restype = wintypes.HANDLE
        k32.OpenProcess.restype = wintypes.HANDLE

        class DASAR(ctypes.Structure):
            _fields_ = [('PerProcessUserTimeLimit', ctypes.c_int64), ('PerJobUserTimeLimit', ctypes.c_int64),
                        ('LimitFlags', wintypes.DWORD), ('MinimumWorkingSetSize', ctypes.c_size_t),
                        ('MaximumWorkingSetSize', ctypes.c_size_t), ('ActiveProcessLimit', wintypes.DWORD),
                        ('Affinity', ctypes.c_size_t), ('PriorityClass', wintypes.DWORD),
                        ('SchedulingClass', wintypes.DWORD)]

        class IO(ctypes.Structure):
            _fields_ = [(n, ctypes.c_uint64) for n in ('R', 'W', 'O', 'RB', 'WB', 'OB')]

        class LENGKAP(ctypes.Structure):
            _fields_ = [('Basic', DASAR), ('Io', IO), ('ProcessMemoryLimit', ctypes.c_size_t),
                        ('JobMemoryLimit', ctypes.c_size_t), ('PeakProcessMemoryUsed', ctypes.c_size_t),
                        ('PeakJobMemoryUsed', ctypes.c_size_t)]

        job = k32.CreateJobObjectW(None, None)
        info = LENGKAP()
        info.Basic.LimitFlags = 0x2000   # JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE
        k32.SetInformationJobObject(job, 9, ctypes.byref(info), ctypes.sizeof(info))
        h = k32.OpenProcess(0x0100 | 0x0001, False, proses.pid)   # SET_QUOTA | TERMINATE
        k32.AssignProcessToJobObject(wintypes.HANDLE(job), wintypes.HANDLE(h))
        TEROWONGAN['job'] = job   # handle dipegang sampai proses Python berakhir
    except Exception:
        pass


def jalankan_terowongan():
    exe = os.path.join(AKAR, 'cloudflared.exe')
    if not os.path.exists(exe):
        return
    import subprocess
    try:
        p = subprocess.Popen(
            [exe, 'tunnel', '--url', 'http://localhost:%d' % PORT, '--no-autoupdate'],
            stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True,
            encoding='utf-8', errors='replace',
            creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
    except OSError as e:
        print('  [!] Terowongan publik gagal dijalankan: %s' % e)
        return
    TEROWONGAN['proses'] = p
    ikat_ke_server(p)

    def baca():
        for baris in p.stderr:
            m = re.search(r'https://[a-z0-9-]+\.trycloudflare\.com', baris)
            if m and not TEROWONGAN['url']:
                TEROWONGAN['url'] = m.group(0)
                print('  HP peserta : %s/bid   (jaringan apa pun, lewat internet)' % m.group(0), flush=True)
        TEROWONGAN['url'] = None   # proses berhenti -> kembali ke IP lokal
    threading.Thread(target=baca, daemon=True).start()


def nama_berkas_aman(s):
    s = re.sub(r'[^\w\s-]', '', str(s or ''), flags=re.UNICODE).strip()
    return re.sub(r'\s+', '-', s).lower()[:80] or 'kelas'


"""
INGATAN KOREKSI BERSAMA — pembetulan kata dikte yang dipelajari di satu laptop
ikut dipakai laptop lain. Tempatnya satu folder OneDrive/SharePoint bernama
ORBIT-Bersama yang dibagikan ke semua PTP; OneDrive yang menyalinkannya antar
laptop, server ini cukup membaca/menulis berkas biasa.

Tiap laptop HANYA menulis berkasnya sendiri (koreksi-<id-laptop>.json) dan
membaca berkas semua laptop lain. Tidak ada dua laptop yang menulis berkas
yang sama, jadi OneDrive tidak pernah membuat salinan "konflik". Penggabungan
(suara terbanyak, pembatalan terbaru menang) dikerjakan di aplikasi.

Folder dicari otomatis di OneDrive & folder pengguna. Bila ditaruh di tempat
lain, alamatnya bisa diisi manual dari Setelan (disimpan di .folder-bersama).
"""
NAMA_FOLDER_BERSAMA = 'ORBIT-Bersama'
BERKAS_FOLDER_BERSAMA = os.path.join(AKAR, '.folder-bersama')   # lokal: tidak ikut zip/git
# Satu berkas per nama komputer: folder aplikasi yang ikut tersinkron OneDrive ke
# laptop lain tidak membuat dua laptop memakai identitas (dan berkas) yang sama.
BERKAS_ID_LAPTOP = os.path.join(AKAR, '.id-laptop-' + nama_berkas_aman(socket.gethostname())[:30])
BERSAMA = {'folder': None, 'dicari': 0.0}


def id_laptop():
    try:
        with open(BERKAS_ID_LAPTOP, encoding='utf-8') as f:
            i = f.read().strip()
        if i:
            return i
    except OSError:
        pass
    import uuid
    i = nama_berkas_aman(socket.gethostname())[:30] + '-' + uuid.uuid4().hex[:6]
    try:
        with open(BERKAS_ID_LAPTOP, 'w', encoding='utf-8') as f:
            f.write(i)
    except OSError:
        pass
    return i


def folder_manual():
    try:
        with open(BERKAS_FOLDER_BERSAMA, encoding='utf-8') as f:
            p = f.read().strip()
        return p or None
    except OSError:
        return None


def cari_folder_bersama(paksa=False):
    """Alamat folder ORBIT-Bersama, atau None. Pencarian dibatasi kedalaman &
    jumlah folder supaya cepat, dan hasil 'tidak ketemu' diingat 2 menit."""
    manual = folder_manual()
    if manual:
        return manual if os.path.isdir(manual) else None
    f = BERSAMA['folder']
    if f and os.path.isdir(f) and not paksa:
        return f
    if not paksa and time.time() - BERSAMA['dicari'] < 120:
        return None
    BERSAMA['dicari'] = time.time()
    BERSAMA['folder'] = None

    # folder di samping aplikasi (ORBIT-Bersama di dalam folder ORBIT) didahulukan
    for dekat in (os.path.join(AKAR, NAMA_FOLDER_BERSAMA), os.path.join(os.path.dirname(AKAR), NAMA_FOLDER_BERSAMA)):
        if os.path.isdir(dekat):
            BERSAMA['folder'] = dekat
            return dekat

    pangkal = []
    for kunci in ('OneDriveCommercial', 'OneDrive', 'OneDriveConsumer'):
        p = os.environ.get(kunci)
        if p and os.path.isdir(p) and p not in pangkal:
            pangkal.append(p)
    profil = os.environ.get('USERPROFILE') or os.path.expanduser('~')
    if profil and os.path.isdir(profil):
        pangkal.append(profil)   # pustaka SharePoint tersinkron ada di sini (mis. "Kemenkeu\...")

    target = NAMA_FOLDER_BERSAMA.lower()
    dikunjungi = 0
    for akar in pangkal:
        antrean = [(akar, 0)]
        while antrean:
            p, d = antrean.pop(0)
            try:
                isi = list(os.scandir(p))
            except OSError:
                continue
            for e in isi:
                try:
                    if not e.is_dir() or e.name.startswith(('.', '$')) or e.name in ('AppData', 'node_modules'):
                        continue
                except OSError:
                    continue
                if e.name.lower() == target:
                    BERSAMA['folder'] = e.path
                    return e.path
                dikunjungi += 1
                if d < 3 and dikunjungi < 6000:
                    antrean.append((e.path, d + 1))
    return None


def status_bersama(paksa=False):
    folder = cari_folder_bersama(paksa)
    hasil = {'ok': True, 'tersambung': bool(folder), 'folder': folder, 'nama': NAMA_FOLDER_BERSAMA,
             'manual': folder_manual(), 'laptop': id_laptop(), 'lain': []}
    if not folder:
        return hasil
    sendiri = 'koreksi-%s.json' % id_laptop()
    try:
        nama_nama = os.listdir(folder)
    except OSError:
        return dict(hasil, tersambung=False)
    semua = [n[:-5] for n in nama_nama if n.startswith('koreksi-') and n.endswith('.json')]
    for inti in semua:
        nama = inti + '.json'
        if nama == sendiri:
            continue
        # salinan "konflik" buatan OneDrive (koreksi-<id>-NAMAPC.json) bukan laptop lain:
        # suara laptop aslinya tidak boleh terhitung dua kali
        if any(inti != lain and inti.startswith((lain + '-', lain + ' ')) for lain in semua + [sendiri[:-5]]):
            continue
        p = os.path.join(folder, nama)
        try:
            with open(p, encoding='utf-8-sig') as f:
                isi = json.load(f)
            hasil['lain'].append({'laptop': nama[8:-5], 'ingatan': isi.get('ingatan') or {},
                                  'waktu': os.path.getmtime(p)})
        except Exception:
            continue   # berkas yang sedang disalin OneDrive / rusak dilewati; dicoba lagi nanti
    return hasil


def unduh_dan_pasang_update():
    """Tarik rilis terbaru dari GitHub lalu pasang di tempat. Mengembalikan
    ETag rilis yang baru dipasang (dicatat pemanggil ke TANDA_VERSI), atau
    None bila server rilis tidak mengirim ETag/Last-Modified.

    Unduh + baca ZIP dulu SAMPAI SELESAI sebelum menyentuh berkas apa pun di
    folder aplikasi — supaya koneksi putus di tengah jalan tidak pernah
    meninggalkan sebagian berkas versi baru dan sebagian versi lama.
    """
    import io
    import urllib.request
    import zipfile

    permintaan = urllib.request.Request(RILIS_ZIP_URL, headers={'User-Agent': 'ORBIT-update'})
    try:
        with urllib.request.urlopen(permintaan, timeout=30) as r:
            data = r.read()
            etag = r.headers.get('ETag') or r.headers.get('Last-Modified')
    except Exception as e:
        raise RuntimeError('Tidak bisa mengunduh pembaruan (periksa internet): %s' % e)

    try:
        z = zipfile.ZipFile(io.BytesIO(data))
        nama_di_zip = set(z.namelist())
    except Exception as e:
        raise RuntimeError('Berkas rilis yang diunduh rusak: %s' % e)

    if 'server.py' not in nama_di_zip:
        raise RuntimeError('Paket rilis tidak lengkap (server.py tidak ada di dalamnya).')

    # per-waktu, bukan menimpa satu folder cadangan yang sama tiap kali —
    # update sebelumnya tetap bisa ditengok/dipulihkan manual bila perlu.
    folder_cadangan = os.path.join(AKAR, 'cadangan-sebelum-update', time.strftime('%Y%m%d-%H%M%S'))
    os.makedirs(folder_cadangan, exist_ok=True)
    for nama in BERKAS_APLIKASI:
        asal = os.path.join(AKAR, nama)
        if os.path.exists(asal):
            with open(asal, 'rb') as f:
                isi = f.read()
            with open(os.path.join(folder_cadangan, nama), 'wb') as f:
                f.write(isi)

    for nama in BERKAS_APLIKASI:
        if nama not in nama_di_zip:
            continue
        with z.open(nama) as sumber, open(os.path.join(AKAR, nama), 'wb') as tujuan:
            tujuan.write(sumber.read())
    return etag


TANDA_VERSI = os.path.join(AKAR, '.versi-terpasang')   # dicatat lokal saja — tidak ikut ke-zip, tidak ikut git


def cek_dan_pasang_update_otomatis():
    """Dipanggil ORBIT-execute.bat lewat `server.py --auto-update` SEBELUM
    aplikasi dibuka, supaya PTP selalu pakai versi terbaru tanpa perlu ingat
    pencet Ctrl+Shift+U atau buka ORBIT-update.bat manual tiap ada rilis baru.

    Cuma HEAD request kecil (bandingkan ETag rilis dengan tanda lokal) —
    zip baru diunduh kalau memang ada versi baru. Gagal/offline dilewati
    diam-diam: sesi harus tetap bisa dibuka tanpa internet.

    Belum ada tanda lokal (laptop PTP yang baru mengekstrak ORBIT.zip, yang
    bisa saja sudah basi) -> langsung unduh rilis terbaru di jalan pertama.
    Salinan pengembang tidak terpengaruh: ia sudah dilewati di atas lewat
    salinan_pengembang()."""
    if salinan_pengembang():
        print('  (salinan pengembang terdeteksi — cek pembaruan otomatis dilewati; pakai git)')
        return
    import urllib.request
    try:
        req = urllib.request.Request(RILIS_ZIP_URL, headers={'User-Agent': 'ORBIT-update'}, method='HEAD')
        with urllib.request.urlopen(req, timeout=5) as r:
            etag = r.headers.get('ETag') or r.headers.get('Last-Modified')
    except Exception:
        print('  (lewati cek pembaruan — tidak ada internet)')
        return
    if not etag:
        return
    try:
        with open(TANDA_VERSI, encoding='utf-8') as f:
            lama = f.read().strip()
    except OSError:
        lama = None   # belum ada tanda -> dianggap perlu update
    if etag == lama:
        print('  Sudah versi terbaru.')
        return
    print('  Versi baru ditemukan — memasang...')
    try:
        etag = unduh_dan_pasang_update() or etag
    except Exception as e:
        print('  [!] Gagal memasang pembaruan otomatis: %s' % e)
        print('  Aplikasi tetap dibuka dengan versi yang ada.')
        return
    try:
        with open(TANDA_VERSI, 'w', encoding='utf-8') as f:
            f.write(etag)
    except OSError:
        pass
    print('  Selesai — aplikasi dibuka dengan versi terbaru.')


def mulai_ulang_server():
    """Menyalakan proses server.py yang baru (versi yang baru saja dipasang),
    lalu mematikan proses saat ini. Proses baru mewarisi konsol yang sama,
    jadi tidak ada jendela hitam kedua yang muncul."""
    import subprocess
    time.sleep(0.5)   # beri waktu respons HTTP di atas benar-benar terkirim
    env = dict(os.environ)
    env['ORBIT_AUTO_RESTART'] = '1'
    try:
        subprocess.Popen([sys.executable, os.path.abspath(__file__)], cwd=AKAR, env=env)
    except Exception as e:
        print('  [!] Gagal menyalakan ulang otomatis: %s' % e)
        print('  Tutup jendela ini lalu jalankan ORBIT-execute.bat lagi secara manual.')
        return
    os._exit(0)


class ServerTunggal(ThreadingHTTPServer):
    # Di Windows, SO_REUSEADDR (bawaan HTTPServer) membiarkan server KEDUA ikut
    # mengikat port yang sama — permintaan lalu tetap jatuh ke server lama.
    # Dimatikan supaya menjalankan ORBIT-execute.bat dua kali gagal dengan jelas.
    allow_reuse_address = False


class Penangan(SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=AKAR, **kw)

    # --- utilitas ---
    def dari_laptop(self):
        # Permintaan lewat terowongan Cloudflare juga tiba dari 127.0.0.1
        # (cloudflared berjalan di laptop ini) — dikenali dari header Cloudflare
        # dan diperlakukan sebagai HP, bukan laptop.
        if self.headers.get('Cf-Connecting-Ip') or self.headers.get('Cf-Ray'):
            return False
        return self.client_address[0] in ('127.0.0.1', '::1')

    def kirim_json(self, obj, kode=200):
        data = json.dumps(obj, ensure_ascii=False).encode('utf-8')
        self.send_response(kode)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Cache-Control', 'no-store')
        self.send_header('Content-Length', str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def baca_json(self):
        n = int(self.headers.get('Content-Length') or 0)
        if n > 5_000_000:
            raise ValueError('terlalu besar')
        return json.loads(self.rfile.read(n).decode('utf-8') or '{}')

    def log_message(self, fmt, *args):
        # log ringkas: sembunyikan polling rutin supaya jendela hitam tetap terbaca
        if any(k in self.path for k in ('/api/liga/status', '/api/liga/bids', '/api/liga/nilai', '/api/info', '/api/koreksi')):
            return
        sys.stderr.write('  %s  %s\n' % (self.client_address[0], fmt % args))

    # --- GET ---
    def do_GET(self):
        jalur = self.path.split('?', 1)[0]
        if jalur in ('/', ''):
            jalur = '/forum-konsultasi-antar-daerah.html' if self.dari_laptop() else '/bid.html'
            self.path = jalur
        if jalur == '/bid':
            self.path = jalur = '/bid.html'

        if jalur == '/api/info':
            return self.kirim_json({'ok': True, 'port': PORT, 'ip': ip_lokal(),
                                    'publik': TEROWONGAN['url'],
                                    'terowongan': TEROWONGAN['proses'] is not None})

        if jalur == '/api/liga/status':
            with KUNCI:
                j = JENDELA
                nilai = None
                if NILAI.get('buka'):
                    nilai = {'buka': True, 'tanggal': NILAI['tanggal'], 'peserta': NILAI['peserta'],
                             'sudah': sorted(NILAI['sudah'])}
                if not j.get('buka'):
                    return self.kirim_json({'buka': False, 'nilai': nilai})
                return self.kirim_json({
                    'buka': True, 'masalahId': j['masalahId'], 'judul': j['judul'],
                    'daerah': j['daerah'], 'peserta': j['peserta'], 'nilai': nilai,
                    'pemilikNama': j.get('pemilikNama', ''),
                })

        if jalur == '/api/liga/nilai':
            if not self.dari_laptop():
                return self.kirim_json({'ok': False, 'pesan': 'Tidak diizinkan.'}, 403)
            with KUNCI:
                return self.kirim_json({'buka': NILAI.get('buka', False), 'tanggal': NILAI.get('tanggal'),
                                        'masuk': NILAI.get('masuk', [])})

        if jalur == '/api/koreksi':
            if not self.dari_laptop():
                return self.kirim_json({'ok': False, 'pesan': 'Tidak diizinkan.'}, 403)
            return self.kirim_json(status_bersama(paksa='cari=1' in self.path))

        if jalur == '/api/liga/bids':
            if not self.dari_laptop():
                return self.kirim_json({'ok': False, 'pesan': 'Tidak diizinkan.'}, 403)
            with KUNCI:
                return self.kirim_json({'buka': JENDELA.get('buka', False),
                                        'masalahId': JENDELA.get('masalahId'),
                                        'bids': JENDELA.get('bids', [])})

        # dari luar laptop (HP, terowongan internet) hanya halaman bid yang tersaji
        if jalur not in (IZIN if self.dari_laptop() else {'/bid.html'}):
            self.send_error(404, 'Tidak ditemukan')
            return
        return super().do_GET()

    def end_headers(self):
        # berkas aplikasi selalu versi terbaru — tidak perlu Ctrl+Shift+R
        if not self.path.startswith('/api/'):
            self.send_header('Cache-Control', 'no-cache')
        super().end_headers()

    # --- POST ---
    def do_POST(self):
        jalur = self.path.split('?', 1)[0]
        try:
            data = self.baca_json()
        except Exception:
            return self.kirim_json({'ok': False, 'pesan': 'Data tidak terbaca.'}, 400)

        if jalur == '/api/liga/bid':
            return self.terima_bid(data)
        if jalur == '/api/liga/nilai':
            return self.terima_nilai(data)

        # semua aksi di bawah ini hanya dari laptop PTP
        if not self.dari_laptop():
            return self.kirim_json({'ok': False, 'pesan': 'Tidak diizinkan.'}, 403)

        if jalur == '/api/liga/buka':
            with KUNCI:
                sama = JENDELA.get('buka') and JENDELA.get('masalahId') == data.get('masalahId')
                lama = JENDELA.get('bids', []) if sama else []
                JENDELA.clear()
                JENDELA.update({
                    'buka': True,
                    'masalahId': str(data.get('masalahId') or ''),
                    'judul': str(data.get('judul') or '')[:300],
                    'daerah': str(data.get('daerah') or '')[:200],
                    'pemilik': str(data.get('pemilik') or ''),
                    'pemilikNama': str(data.get('pemilikNama') or '')[:200],
                    'peserta': [{'id': str(p.get('id')), 'nama': str(p.get('nama')),
                                 'daerah': str(p.get('daerah') or '')}
                                for p in (data.get('peserta') or [])],
                    'bids': lama,
                    'seq': len(lama),
                })
            return self.kirim_json({'ok': True})

        if jalur == '/api/liga/tutup':
            with KUNCI:
                JENDELA.clear()
                JENDELA['buka'] = False
            return self.kirim_json({'ok': True})

        if jalur == '/api/liga/nilai-buka':
            with KUNCI:
                tgl = str(data.get('tanggal') or '')
                lama = NILAI.get('masuk', []) if NILAI.get('tanggal') == tgl else []
                NILAI.clear()
                NILAI.update({
                    'buka': True, 'tanggal': tgl,
                    'peserta': [{'id': str(p.get('id')), 'nama': str(p.get('nama')),
                                 'daerah': str(p.get('daerah') or '')}
                                for p in (data.get('peserta') or [])],
                    'sudah': set(str(x) for x in (data.get('sudah') or [])) | {m['pesertaId'] for m in lama},
                    'masuk': lama,
                })
            return self.kirim_json({'ok': True})

        if jalur == '/api/liga/nilai-tutup':
            with KUNCI:
                NILAI.clear()
                NILAI['buka'] = False
            return self.kirim_json({'ok': True})

        if jalur == '/api/update':
            if salinan_pengembang():
                return self.kirim_json({'ok': False, 'pesan':
                    'Ini salinan pengembang (folder .git ada) — pembaruan lewat tombol ini '
                    'dimatikan supaya tidak menimpa balik pekerjaan yang belum dirilis. '
                    'Perbarui salinan ini lewat git, bukan lewat tombol Update.'})
            try:
                etag = unduh_dan_pasang_update()
            except Exception as e:
                return self.kirim_json({'ok': False, 'pesan': str(e)})
            if etag:
                try:
                    with open(TANDA_VERSI, 'w', encoding='utf-8') as f:
                        f.write(etag)
                except OSError:
                    pass
            self.kirim_json({'ok': True, 'pesan': 'Update terpasang. Menyalakan ulang server...'})
            threading.Thread(target=mulai_ulang_server, daemon=True).start()
            return

        if jalur == '/api/koreksi':
            folder = cari_folder_bersama()
            if not folder:
                return self.kirim_json({'ok': True, 'tersambung': False})
            ingatan = data.get('ingatan')
            if not isinstance(ingatan, dict):
                return self.kirim_json({'ok': False, 'pesan': 'Data tidak terbaca.'}, 400)
            tujuan = os.path.join(folder, 'koreksi-%s.json' % id_laptop())
            sementara = tujuan + '.tmp'
            try:
                with open(sementara, 'w', encoding='utf-8') as f:
                    json.dump({'laptop': id_laptop(), 'waktu': time.strftime('%Y-%m-%dT%H:%M:%S'),
                               'ingatan': ingatan}, f, ensure_ascii=False)
                os.replace(sementara, tujuan)
            except OSError as e:
                return self.kirim_json({'ok': False, 'tersambung': True, 'pesan': str(e)})
            return self.kirim_json({'ok': True, 'tersambung': True})

        if jalur == '/api/koreksi/folder':
            p = str(data.get('folder') or '').strip().strip('"')
            if p and not os.path.isdir(p):
                return self.kirim_json({'ok': False, 'pesan': 'Folder itu tidak ditemukan di laptop ini.'})
            try:
                if p:
                    with open(BERKAS_FOLDER_BERSAMA, 'w', encoding='utf-8') as f:
                        f.write(p)
                elif os.path.exists(BERKAS_FOLDER_BERSAMA):
                    os.remove(BERKAS_FOLDER_BERSAMA)
            except OSError as e:
                return self.kirim_json({'ok': False, 'pesan': str(e)})
            return self.kirim_json(status_bersama(paksa=True))

        if jalur == '/api/liga/arsip':
            kelas = (data.get('kelas') or {})
            nama = nama_berkas_aman(kelas.get('nama')) + '__' + nama_berkas_aman(kelas.get('id'))
            os.makedirs(FOLDER_ARSIP, exist_ok=True)
            tujuan = os.path.join(FOLDER_ARSIP, 'liga-' + nama + '.json')
            sementara = tujuan + '.tmp'
            with open(sementara, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            os.replace(sementara, tujuan)   # tulis atomik: arsip tidak pernah setengah jadi
            return self.kirim_json({'ok': True, 'berkas': os.path.relpath(tujuan, AKAR)})

        return self.kirim_json({'ok': False, 'pesan': 'Alamat tidak dikenal.'}, 404)

    def terima_bid(self, data):
        with KUNCI:
            j = JENDELA
            if not j.get('buka'):
                return self.kirim_json({'ok': False, 'pesan': 'Jendela bid sudah ditutup.'}, 409)
            if str(data.get('masalahId')) != j['masalahId']:
                return self.kirim_json({'ok': False, 'pesan': 'Masalah yang dibuka sudah berganti. Muat ulang halaman.'}, 409)
            pid = str(data.get('pesertaId') or '')
            if pid == j.get('pemilik'):
                return self.kirim_json({'ok': False, 'pesan': 'Pemilik masalah tidak bisa bid di masalahnya sendiri.'}, 400)
            if not any(p['id'] == pid for p in j['peserta']):
                return self.kirim_json({'ok': False, 'pesan': 'Nama tidak ada di daftar peserta.'}, 400)
            kp = str(data.get('keypoint') or '').strip()[:2000]
            if not kp:
                return self.kirim_json({'ok': False, 'pesan': 'Keypoint belum diisi.'}, 400)
            # satu orang satu bid per masalah — kiriman ulang memperbarui keypoint
            for b in j['bids']:
                if b['pesertaId'] == pid:
                    b['keypoint'] = kp
                    b['waktu'] = time.strftime('%Y-%m-%dT%H:%M:%S')
                    b['rev'] = b.get('rev', 0) + 1
                    return self.kirim_json({'ok': True, 'diperbarui': True})
            j['seq'] += 1
            j['bids'].append({'id': 'hp%d-%s' % (j['seq'], j['masalahId']), 'pesertaId': pid,
                              'keypoint': kp, 'waktu': time.strftime('%Y-%m-%dT%H:%M:%S'), 'rev': 0})
        return self.kirim_json({'ok': True, 'diperbarui': False})

    def terima_nilai(self, data):
        with KUNCI:
            n = NILAI
            if not n.get('buka'):
                return self.kirim_json({'ok': False, 'pesan': 'Penilaian sesi sedang ditutup.'}, 409)
            if str(data.get('tanggal') or '') != n['tanggal']:
                return self.kirim_json({'ok': False, 'pesan': 'Sesi sudah berganti. Muat ulang halaman.'}, 409)
            pid = str(data.get('pesertaId') or '')
            if not any(p['id'] == pid for p in n['peserta']):
                return self.kirim_json({'ok': False, 'pesan': 'Nama tidak ada di daftar peserta.'}, 400)
            if pid in n['sudah']:
                return self.kirim_json({'ok': False, 'sudah': True, 'pesan': 'Nama ini sudah memberi penilaian untuk sesi ini.'}, 409)
            try:
                nilai = int(data.get('nilai'))
            except (TypeError, ValueError):
                nilai = 0
            if nilai < 1 or nilai > 5:
                return self.kirim_json({'ok': False, 'pesan': 'Geser dulu untuk memilih nilai 1 sampai 5.'}, 400)
            n['sudah'].add(pid)
            n['masuk'].append({'pesertaId': pid, 'nilai': nilai,
                               'komentar': str(data.get('komentar') or '').strip()[:500],
                               'waktu': time.strftime('%Y-%m-%dT%H:%M:%S')})
        return self.kirim_json({'ok': True})


def main():
    # Restart otomatis (habis /api/update): proses lama baru saja melepas port,
    # tapi Windows kadang butuh sesaat sebelum benar-benar bisa dipakai lagi —
    # dicoba beberapa kali dulu sebelum menyerah. Peluncuran manual biasa (klik
    # ORBIT-execute.bat dua kali) tetap gagal seketika seperti sebelumnya.
    auto_restart = os.environ.get('ORBIT_AUTO_RESTART') == '1'
    percobaan_maks = 20 if auto_restart else 1
    srv = None
    for percobaan in range(percobaan_maks):
        try:
            srv = ServerTunggal(('0.0.0.0', PORT), Penangan)
            break
        except OSError as e:
            if percobaan < percobaan_maks - 1:
                time.sleep(0.5)
                continue
            print('  [GAGAL] Port %d sudah dipakai (%s).' % (PORT, e))
            print('  Aplikasi sudah berjalan di jendela hitam lain — pakai yang itu,')
            print('  atau tutup jendela itu dulu lalu jalankan ORBIT-execute.bat lagi.')
            input('  Tekan Enter untuk menutup...')
            sys.exit(1)
    if auto_restart:
        print('  (dinyalakan ulang otomatis setelah update)')
    ips = ip_lokal()
    print('  Laptop PTP : http://localhost:%d/forum-konsultasi-antar-daerah.html' % PORT)
    if ips:
        for ip in ips:
            print('  HP peserta : http://%s:%d/bid   (hanya saat jendela bid dibuka)' % (ip, PORT))
    else:
        print('  HP peserta : laptop belum tersambung ke WiFi — bid lewat HP tidak tersedia,')
        print('               PTP tetap bisa mencatat bid secara manual.')
    jalankan_terowongan()
    if TEROWONGAN['proses']:
        print('  Menyiapkan alamat internet untuk HP peserta (beberapa detik)...')
    print()
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        if TEROWONGAN['proses']:
            TEROWONGAN['proses'].terminate()


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--auto-update':
        cek_dan_pasang_update_otomatis()   # cek + pasang lalu keluar; tidak menyalakan server
    else:
        main()
