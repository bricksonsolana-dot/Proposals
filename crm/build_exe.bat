@echo off
REM Build a single-file Windows .exe of the Devox Sales desktop client.
REM Output: dist\DevoxSales.exe

cd /d "%~dp0"

set PYTHON_EXE=%USERPROFILE%\anaconda3\python.exe
if not exist "%PYTHON_EXE%" set PYTHON_EXE=python

echo Building DevoxSales.exe...
"%PYTHON_EXE%" -m PyInstaller ^
  --onefile ^
  --windowed ^
  --name DevoxSales ^
  --icon static\logo.ico ^
  --add-data "static\logo.ico;static" ^
  --add-data "static\logo.png;static" ^
  --add-data "crm_url.txt;." ^
  desktop_client.py

if errorlevel 1 (
  echo BUILD FAILED
  exit /b 1
)

echo.
echo Built dist\DevoxSales.exe
echo Distribute this single file to your sales team.
