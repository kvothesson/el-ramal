@echo off
cd /d "%~dp0"
start "" http://127.0.0.1:5361/
python -m http.server 5361 --bind 127.0.0.1
