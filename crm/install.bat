@echo off
REM Devox Sales — One-time installer
REM Run this once. It will:
REM  1. Verify Python is installed (or guide to install)
REM  2. Install required Python packages
REM  3. Create a desktop shortcut
REM  4. Launch the app

setlocal
cd /d "%~dp0"

echo.
echo ===============================================
echo   Devox Sales - Installer
echo ===============================================
echo.

REM Check for Python
where python >nul 2>&1
if errorlevel 1 (
  echo Python is not installed.
  echo.
  echo Please install Python 3.10+ from:
  echo   https://www.python.org/downloads/
  echo.
  echo IMPORTANT: During installation, check
  echo   "Add Python to PATH"
  echo.
  pause
  exit /b 1
)

echo Step 1/3: Installing required packages...
python -m pip install --quiet --upgrade pip
python -m pip install --quiet -r requirements-client.txt
if errorlevel 1 (
  echo Failed to install packages. Check your internet connection.
  pause
  exit /b 1
)

echo Step 2/3: Creating desktop shortcut...
powershell -ExecutionPolicy Bypass -File install_shortcut.ps1
if errorlevel 1 (
  echo Shortcut creation failed (you can still run the app manually).
)

echo.
echo ===============================================
echo   Installation complete!
echo ===============================================
echo.
echo Look for "Devox Sales" on your desktop.
echo Double-click it to open the app.
echo.
echo Launching now...
echo.
timeout /t 2 >nul
start "" pythonw.exe desktop_client.py
exit /b 0
