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


def unduh_dan_pasang_update():
    """Tarik rilis terbaru dari GitHub lalu pasang di tempat.

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
    except Exception as e:
        raise RuntimeError('Tidak bisa mengunduh pembaruan (periksa internet): %s' % e)

    try:
        z = zipfile.ZipFile(io.BytesIO(data))
        nama_di_zip = set(z.namelist())
    except Exception as e:
        raise RuntimeError('Berkas rilis yang diunduh rusak: %s' % e)

    if 'server.py' not in nama_di_zip:
        raise RuntimeError('Paket rilis tidak lengkap (server.py tidak ada di dalamnya).')

    folder_cadangan = os.path.join(AKAR, 'cadangan-sebelum-update')
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
        if any(k in self.path for k in ('/api/liga/status', '/api/liga/bids', '/api/liga/nilai', '/api/info')):
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
                })

        if jalur == '/api/liga/nilai':
            if not self.dari_laptop():
                return self.kirim_json({'ok': False, 'pesan': 'Tidak diizinkan.'}, 403)
            with KUNCI:
                return self.kirim_json({'buka': NILAI.get('buka', False), 'tanggal': NILAI.get('tanggal'),
                                        'masuk': NILAI.get('masuk', [])})

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
            try:
                unduh_dan_pasang_update()
            except Exception as e:
                return self.kirim_json({'ok': False, 'pesan': str(e)})
            self.kirim_json({'ok': True, 'pesan': 'Update terpasang. Menyalakan ulang server...'})
            threading.Thread(target=mulai_ulang_server, daemon=True).start()
            return

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
    main()
