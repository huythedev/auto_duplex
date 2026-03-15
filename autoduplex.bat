@echo off
:: Change the working directory to the location of this batch file
cd /d "%~dp0"

:: Run python in the background (pythonw) and close this CMD window immediately
start "" pythonw main.py

exit