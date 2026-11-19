@echo off
cd /d "%~dp0"
where pwsh.exe >nul 2>&1
if %errorlevel% equ 0 (
  pwsh.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0app\launch.ps1"
) else (
  powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0app\launch.ps1"
)
pause
