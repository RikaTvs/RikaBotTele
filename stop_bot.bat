@echo off
setlocal
title Stop Rika Bot Tele To AI
color 0C

echo ========================================================
echo             DANG DUNG RIKA BOT TELE TO AI
echo ========================================================
echo.

cd /d "%~dp0"

:: Đóng tiến trình python chạy bot.py
powershell -NoProfile -Command "Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -like '*bot.py*' } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue; Write-Host ('[+] Da dung bot process PID: ' + $_.ProcessId) }"

echo.
echo [*] Da dung tat ca cac tien trinh Bot thanh cong!
timeout /t 2 >nul
