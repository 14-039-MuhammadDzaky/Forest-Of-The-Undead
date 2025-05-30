@echo off
echo Menjalankan Project

cd /d "%~dp0Forest-Of-The-Undead\code"

echo.
echo Memastikan semua module terinstall...
pip install pygame
pip install pytmx

echo.
echo Menjalankan game...
python main.py

pause
