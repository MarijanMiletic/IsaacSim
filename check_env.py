import sys

print("=== DETALJNA PROVJERA OKRUŽENJA ===")
print(f"Python verzija: {sys.version}")

print("\n--- Provjera PyTorch i CUDA (Grafička Kartica) ---")
try:
    import torch
    print(f"PyTorch verzija: {torch.__version__}")
    print(f"CUDA dostupna (GPU ubrzanje): {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"CUDA uređaj: {torch.cuda.get_device_name(0)}")
except ImportError:
    print("Greška: PyTorch nije instaliran.")
except Exception as e:
    print(f"Greška s PyTorchom: {e}")

print("\n--- Provjera Isaac Sim modula ---")
try:
    import isaacsim
    print("Isaac Sim modul: USPJEŠNO PRONAĐEN")
except ImportError:
    print("Greška: Isaac Sim modul nije instaliran.")
except Exception as e:
    print(f"Greška pri učitavanju Isaac Sim modula: {e}")
