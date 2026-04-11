# NVIDIA Isaac Sim Project

This repository contains robot simulation scripts using NVIDIA Isaac Sim 4.5.0.

## Overview
The main highlight of this project is a pick-and-place simulation using the **Franka Emika** robot arm. The project utilizes modern object-oriented programming (OOP) practices for the main simulation script and silences verbose internal Isaac Sim logs for a cleaner terminal output.

## Prerequisites

- **OS:** Windows 10/11 (with NVIDIA GPU)
- **Python:** 3.10.11
- **NVIDIA Drivers:** Latest drivers supporting CUDA 12.8+

## Installation

Follow these steps to replicate the environment used in this project:

### 1. Create a Virtual Environment
It is highly recommended to use a virtual environment to manage dependencies:
```powershell
# Create the environment
python -m venv venv_isaac

# Activate it (Windows PowerShell)
.\venv_isaac\Scripts\activate
```

### 2. Install PyTorch with CUDA 12.8 Support
Isaac Sim 4.5.0 requires a specific PyTorch version. Install it using the official wheel index:
```powershell
pip install torch==2.7.0 torchvision==0.22.0 --index-url https://download.pytorch.org/whl/cu128
```

### 3. Install NVIDIA Isaac Sim
Install the main Isaac Sim package and its extensions from the NVIDIA PyPI repository:
```powershell
pip install "isaacsim[all,extscache]==4.5.0.0" --extra-index-url https://pypi.nvidia.com
```

### 4. Install Project Requirements
Install additional libraries like NumPy, SciPy, and Gymnasium:
```powershell
pip install -r requirements.txt
```

## Running the Simulation

You can easily start the simulations using the provided batch scripts (no need to manually activate the virtual environment):

- **`run_franka.bat`**: Starts the main Franka Pick and Place visual simulation.
- **`run_headless.bat`**: Starts the physics engine test in headless mode.

Alternatively, you can run them manually from your activated environment:

```powershell
# Run the Isaac Sim test script
python test_isaac.py

# Run the Franka Emika example
python franka_example.py

# Run the OOP Franka Pick and Place simulation
python franka_pick_and_place.py
```

## Project Structure
- `franka_pick_and_place.py`: Main Franka robot arm simulation (OOP structure).
- `test_isaac.py`: Basic connectivity and simulation test.
- `franka_example.py`: Franka robot arm minimal example.
- `test_headless_sim.py`: Script for running simulations without a GUI.
- `check_env.py`: Utility to verify your Python and CUDA environment.
- `run_franka.bat` / `run_headless.bat`: 1-click startup scripts.