import sys

print("=== DETAILED ENVIRONMENT CHECK ===")
print(f"Python version: {sys.version}")

print("\n--- Checking PyTorch and CUDA (GPU) ---")
try:
    import torch
    print(f"PyTorch version: {torch.__version__}")
    print(f"CUDA available (GPU acceleration): {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"CUDA device: {torch.cuda.get_device_name(0)}")
except ImportError:
    print("Error: PyTorch is not installed.")
except Exception as e:
    print(f"Error with PyTorch: {e}")

print("\n--- Checking Isaac Sim modules ---")
try:
    import isaacsim
    print("Isaac Sim module: SUCCESSFULLY FOUND")
except ImportError:
    print("Error: Isaac Sim module is not installed.")
except Exception as e:
    print(f"Error loading Isaac Sim module: {e}")