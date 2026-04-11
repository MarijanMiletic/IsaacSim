# 🤖 NVIDIA Isaac Sim Project

[![NVIDIA Isaac Sim](https://img.shields.io/badge/Isaac_Sim-4.5.0-76B900?logo=nvidia&logoColor=white)](https://developer.nvidia.com/isaac-sim)
[![Python](https://img.shields.io/badge/Python-3.10.11-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.7.0%2Bcu128-EE4C2C?logo=pytorch&logoColor=white)](https://pytorch.org/)

This repository contains advanced robotics simulation scripts using **NVIDIA Isaac Sim 4.5.0**. It focuses on modern Object-Oriented Programming (OOP) practices, Inverse Kinematics (IK), and dynamic real-time target tracking for industrial robot arms (Franka Emika and UR10).

---

## 🎥 Demonstrations

*(To complete your README, you can record short GIFs/Videos of your simulations and place the links below!)*

### 1. UR10 Dynamic Pick & Throw (Inverse Kinematics)
The UR10 robot dynamically tracks a cube falling from 1.5m in the air, waits for it to settle, and uses an S-Curve smoothed Inverse Kinematics solver to accurately pick and move it to a target zone.

> **[Insert Video / GIF here: e.g. `![UR10 Pick and Throw](assets/ur10_demo.gif)`]**

### 2. Franka Emika Pick and Place
A classic pick-and-place operation using the built-in PickPlaceController for the Franka Emika Panda arm.

> **[Insert Video / GIF here: e.g. `![Franka Pick and Place](assets/franka_demo.gif)`]**

---

## 🚀 Running the Simulations

You can easily start the simulations using the provided **1-click batch scripts** (no need to manually activate the virtual environment):

| Simulation | Script to Run | Description |
| :--- | :--- | :--- |
| **UR10 Dynamic Pick** | `run_ur10_tracking.bat` | Advanced UR10 simulation using IK to dynamically track, pick, and throw a cube. |
| **UR10 Basic Animation**| `run_ur10.bat` | Basic UR10 simulation with a custom sine-wave joint animation. |
| **Franka Pick & Place** | `run_franka.bat` | Main Franka robot arm simulation using built-in controllers. |
| **Headless Physics Test**| `run_headless.bat` | Starts the background physics engine test without a GUI. |

Alternatively, you can run them manually from your activated environment:
```powershell
python ur10_tracking.py
python franka_pick_and_place.py
```

---

## 🛠️ Installation & Prerequisites

- **OS:** Windows 10/11 (with NVIDIA GPU)
- **Python:** 3.10.11
- **NVIDIA Drivers:** Latest drivers supporting CUDA 12.8+

Follow these steps to replicate the environment used in this project:

### 1. Create a Virtual Environment
```powershell
python -m venv venv_isaac
.\venv_isaac\Scripts\activate
```

### 2. Install PyTorch with CUDA 12.8 Support
```powershell
pip install torch==2.7.0 torchvision==0.22.0 --index-url https://download.pytorch.org/whl/cu128
```

### 3. Install NVIDIA Isaac Sim
```powershell
pip install "isaacsim[all,extscache]==4.5.0.0" --extra-index-url https://pypi.nvidia.com
```

### 4. Install Project Requirements
```powershell
pip install -r requirements.txt
```

---

## 📂 Project Structure

- **`ur10_tracking.py`**: Advanced UR10 simulation using Inverse Kinematics (IK) for dynamic picking.
- **`ur10_example.py`**: Basic Universal Robots UR10 example.
- **`franka_pick_and_place.py`**: Main Franka robot arm simulation (OOP structure).
- **`franka_example.py`**: Franka robot arm minimal example.
- **`test_isaac.py`**: Basic connectivity and scene generation test.
- **`test_headless_sim.py`**: Script for running simulations without a GUI.
- **`test_ur10_headless.py` / `test_ik_headless.py`**: Headless automated testing scripts for CI pipelines.
- **`check_env.py`**: Utility to verify your Python and CUDA environment.