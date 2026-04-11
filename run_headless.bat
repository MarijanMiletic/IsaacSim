@echo off
echo Starting the virtual environment and running Headless Simulation...
call .\venv_isaac\Scripts\activate.bat
python test_headless_sim.py
pause