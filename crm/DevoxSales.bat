@echo off
REM Launcher for Devox Sales CRM (desktop app)
REM Double-click this file to open the CRM in a native window.

cd /d "%~dp0"

REM Try to find Python: prefer Anaconda, fall back to system python
set PYTHON_EXE=
if exist "%USERPROFILE%\anaconda3\pythonw.exe" set PYTHON_EXE=%USERPROFILE%\anaconda3\pythonw.exe
if "%PYTHON_EXE%"=="" if exist "%USERPROFILE%\anaconda3\python.exe" set PYTHON_EXE=%USERPROFILE%\anaconda3\python.exe
if "%PYTHON_EXE%"=="" set PYTHON_EXE=pythonw.exe

REM Use pythonw.exe so no console window pops up
start "" "%PYTHON_EXE%" "%~dp0desktop_app.py"
