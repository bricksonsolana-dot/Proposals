@echo off
REM Build a zip file ready to distribute to sales team.
REM Output: dist\DevoxSales-Setup.zip

cd /d "%~dp0"

set OUTDIR=dist
set STAGE=%OUTDIR%\DevoxSales

if exist "%STAGE%" rmdir /s /q "%STAGE%"
mkdir "%STAGE%"

REM Copy only the files needed by the desktop client
copy desktop_client.py "%STAGE%\" >nul
copy crm_url.txt "%STAGE%\" >nul
copy requirements-client.txt "%STAGE%\" >nul
copy install.bat "%STAGE%\" >nul
copy install_shortcut.ps1 "%STAGE%\" >nul
copy DevoxSalesClient.bat "%STAGE%\" >nul
copy README-SALES.txt "%STAGE%\" >nul

mkdir "%STAGE%\static"
copy static\logo.png "%STAGE%\static\" >nul
copy static\logo.ico "%STAGE%\static\" >nul

powershell -Command "Compress-Archive -Path '%STAGE%\*' -DestinationPath '%OUTDIR%\DevoxSales-Setup.zip' -Force"

if exist "%OUTDIR%\DevoxSales-Setup.zip" (
  echo.
  echo Built: %OUTDIR%\DevoxSales-Setup.zip
  echo Send this file to your sales team.
) else (
  echo Failed to create zip.
)

rmdir /s /q "%STAGE%"
