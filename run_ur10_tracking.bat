@echo off
echo Starting the virtual environment and running Intelligent UR10 Tracking...
call .\venv_isaac\Scripts\activate.bat
python ur10_tracking.py
pause