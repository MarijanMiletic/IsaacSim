@echo off
echo Starting the virtual environment and running Franka Pick and Place...
call .\venv_isaac\Scripts\activate.bat
python franka_pick_and_place.py
pause