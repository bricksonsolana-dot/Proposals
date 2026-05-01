@echo off
REM Launcher for Devox Sales — connects to the cloud CRM.
REM Uses pythonw.exe so no console window pops up.

cd /d "%~dp0"

set PYTHON_EXE=pythonw.exe
if exist "%USERPROFILE%\anaconda3\pythonw.exe" set PYTHON_EXE=%USERPROFILE%\anaconda3\pythonw.exe

start "" "%PYTHON_EXE%" "%~dp0desktop_client.py"
