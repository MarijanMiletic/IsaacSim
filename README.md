# NVIDIA Isaac Sim Project

This repository contains robot simulation scripts using NVIDIA Isaac Sim 4.5.0.

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

Once installed, you can test the setup with the provided scripts:

```powershell
# Run the Isaac Sim test script
python test_isaac.py

# Run the Franka Emika example
python franka_example.py
```

## Project Structure
- `test_isaac.py`: Basic connectivity and simulation test.
- `franka_example.py`: Franka robot arm simulation example.
- `test_headless_sim.py`: Script for running simulations without a GUI.
- `check_env.py`: Utility to verify your Python and CUDA environment.
