@echo off
REM Launcher for Devox Lead Finder (desktop app)
REM Double-click this to open the Lead Finder dashboard in a native window.

cd /d "%~dp0"

set PYTHON_EXE=
if exist "%USERPROFILE%\anaconda3\pythonw.exe" set PYTHON_EXE=%USERPROFILE%\anaconda3\pythonw.exe
if "%PYTHON_EXE%"=="" if exist "%USERPROFILE%\anaconda3\python.exe" set PYTHON_EXE=%USERPROFILE%\anaconda3\python.exe
if "%PYTHON_EXE%"=="" set PYTHON_EXE=pythonw.exe

start "" "%PYTHON_EXE%" "%~dp0desktop_app.py"
