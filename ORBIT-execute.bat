@echo off
cd /d "%~dp0"
title ORBIT  --  JANGAN TUTUP JENDELA INI
color 0E

echo ============================================================
echo   ORBIT
echo ============================================================
echo.
echo   Menyiapkan aplikasi...
echo.

REM Cek Python tersedia — coba beberapa nama peluncur. Tidak semua laptop
REM mendaftarkan "python" ke PATH; banyak instalasi Windows hanya punya
REM launcher "py" (terdaftar otomatis oleh installer resmi python.org).
REM Cukup salah satu yang berhasil, supaya lebih banyak laptop terdeteksi.
set PYEXE=
python --version >nul 2>&1
if not errorlevel 1 set PYEXE=python

if not defined PYEXE (
  py -3 --version >nul 2>&1
  if not errorlevel 1 set PYEXE=py -3
)

if not defined PYEXE (
  py --version >nul 2>&1
  if not errorlevel 1 set PYEXE=py
)

if not defined PYEXE (
  python3 --version >nul 2>&1
  if not errorlevel 1 set PYEXE=python3
)

if not defined PYEXE (
  echo   [GAGAL] Python tidak ditemukan di komputer ini.
  echo.
  echo   Aplikasi tetap dibuka, tapi langsung dari berkas HTML-nya —
  echo   fitur DIKTE SUARA tidak akan stabil, izin mikrofon ditanya ulang
  echo   terus. Fitur lain tetap berjalan normal: catat manual, Liga
  echo   Inovasi tanpa bid HP, Unduh PDF/Word.
  echo.
  start "" "%~dp0forum-konsultasi-antar-daerah.html"
  pause
  exit /b 1
)

REM Buka browser 2 detik setelah server siap
start "" /b cmd /c "timeout /t 2 /nobreak >nul & start "" http://localhost:8200/forum-konsultasi-antar-daerah.html"

echo   Aplikasi akan terbuka di browser sebentar lagi.
echo.
echo   ------------------------------------------------------------
echo   JANGAN TUTUP jendela hitam ini selama sesi berlangsung.
echo   Menutup jendela ini akan mematikan aplikasi.
echo   ------------------------------------------------------------
echo.
echo   Selesai sesi? Tutup jendela ini atau tekan Ctrl+C.
echo.

REM server.py = penyaji aplikasi + jendela bid Liga Inovasi untuk HP peserta.
REM Bila berkasnya tidak ada, kembali ke penyaji bawaan (tanpa bid lewat HP).
if exist "%~dp0server.py" (
  echo   Bila Windows menanyakan izin jaringan untuk Python, pilih
  echo   "Allow" / "Izinkan" pada jaringan PRIVATE, supaya HP peserta bisa bid.
  echo.
  %PYEXE% "%~dp0server.py"
) else (
  %PYEXE% -m http.server 8200 --bind 127.0.0.1
)
