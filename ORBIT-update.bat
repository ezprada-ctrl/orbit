@echo off
cd /d "%~dp0"
title ORBIT -- Cek Pembaruan
color 0B

echo ============================================================
echo   ORBIT - Cek dan Pasang Pembaruan
echo ============================================================
echo.
echo   Ini akan mengunduh versi TERBARU dari internet dan
echo   menggantikan berkas aplikasi di folder ini.
echo.
echo   Data peserta, arsip Liga Inovasi, dan sesi yang tersimpan
echo   di browser TIDAK ikut terhapus atau tertimpa.
echo.
echo   Berkas lama disalin dulu ke folder "cadangan-sebelum-update"
echo   sebelum diganti, supaya bisa dikembalikan kalau perlu.
echo.
pause

set URL=https://github.com/ezprada-ctrl/orbit/releases/latest/download/ORBIT.zip
set TMPZIP=%TEMP%\ORBIT-update-%RANDOM%.zip
set TMPDIR=%TEMP%\ORBIT-update-%RANDOM%

echo.
echo   Mengunduh versi terbaru...
powershell -NoProfile -ExecutionPolicy Bypass -Command "try { Invoke-WebRequest -Uri '%URL%' -OutFile '%TMPZIP%' -UseBasicParsing } catch { Write-Host $_.Exception.Message; exit 1 }"
if errorlevel 1 (
  echo.
  echo   [GAGAL] Tidak bisa mengunduh pembaruan.
  echo   Periksa koneksi internet, lalu jalankan lagi ORBIT-update.bat.
  echo.
  pause
  exit /b 1
)

echo   Mengekstrak...
if exist "%TMPDIR%" rmdir /s /q "%TMPDIR%"
powershell -NoProfile -ExecutionPolicy Bypass -Command "Expand-Archive -Path '%TMPZIP%' -DestinationPath '%TMPDIR%' -Force"
if errorlevel 1 (
  echo   [GAGAL] Berkas unduhan rusak atau tidak lengkap. Coba lagi.
  del /q "%TMPZIP%" >nul 2>&1
  pause
  exit /b 1
)

echo   Menyimpan cadangan berkas lama...
if not exist "cadangan-sebelum-update" mkdir "cadangan-sebelum-update"
for %%F in (ORBIT-execute.bat server.py forum-konsultasi-antar-daerah.html bid.html index.html PANDUAN-OPERASIONAL.md) do (
  if exist "%%F" copy /y "%%F" "cadangan-sebelum-update\%%F" >nul
)

echo   Memasang versi baru...
set ADA=0
for %%F in (ORBIT-execute.bat server.py forum-konsultasi-antar-daerah.html bid.html index.html PANDUAN-OPERASIONAL.md) do (
  if exist "%TMPDIR%\%%F" (
    copy /y "%TMPDIR%\%%F" "%%F" >nul
    set ADA=1
  )
)

del /q "%TMPZIP%" >nul 2>&1
rmdir /s /q "%TMPDIR%" >nul 2>&1

if "%ADA%"=="0" (
  echo.
  echo   [GAGAL] Paket pembaruan tidak berisi berkas yang dikenali.
  echo   Berkas lama tidak diubah.
  pause
  exit /b 1
)

echo.
echo   ============================================================
echo   Selesai! Aplikasi sudah versi terbaru.
echo   ============================================================
echo.
echo   Jalankan seperti biasa lewat ORBIT-execute.bat.
echo   Kalau ada yang aneh, berkas versi sebelumnya ada di folder
echo   "cadangan-sebelum-update" dan bisa dikembalikan manual.
echo.
pause
