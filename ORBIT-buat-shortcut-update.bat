@echo off
cd /d "%~dp0"
title ORBIT -- Buat Shortcut Update
color 0B

echo ============================================================
echo   ORBIT - Buat Shortcut "Update ORBIT" di Desktop
echo ============================================================
echo.
echo   Jalankan ini SEKALI SAJA. Setelah ini akan muncul ikon baru
echo   di Desktop bernama "Update ORBIT".
echo.
echo   Lain kali mau update, PTP tinggal klik dua kali ikon itu di
echo   Desktop - tidak perlu buka folder ini lagi.
echo.
pause

set PS1=%TEMP%\orbit-buat-shortcut-%RANDOM%.ps1
(
  echo $ErrorActionPreference = "Stop"
  echo try {
  echo   $DesktopPath = [Environment]::GetFolderPath^("Desktop"^)
  echo   $WshShell = New-Object -ComObject WScript.Shell
  echo   $Shortcut = $WshShell.CreateShortcut^([System.IO.Path]::Combine^($DesktopPath, "Update ORBIT.lnk"^)^)
  echo   $Shortcut.TargetPath = "%~dp0ORBIT-update.bat"
  echo   $Shortcut.WorkingDirectory = "%~dp0"
  echo   $Shortcut.IconLocation = "shell32.dll,46"
  echo   $Shortcut.Save^(^)
  echo } catch {
  echo   Write-Host $_.Exception.Message
  echo   exit 1
  echo }
) > "%PS1%"

powershell -NoProfile -ExecutionPolicy Bypass -File "%PS1%"
set ERR=%errorlevel%
del /q "%PS1%" >nul 2>&1

if not "%ERR%"=="0" (
  echo.
  echo   [GAGAL] Tidak bisa membuat shortcut.
  echo   Coba jalankan lagi, atau minta bantuan admin IT.
  echo.
  pause
  exit /b 1
)

echo.
echo   ============================================================
echo   Selesai! Cek Desktop - ada ikon baru "Update ORBIT".
echo   ============================================================
echo.
pause
