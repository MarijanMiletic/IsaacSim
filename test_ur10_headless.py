import os
import sys

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

from ur10_example import UR10Sim

try:
    print("=== STARTING QUICK TEST FOR UR10 IN HEADLESS MODE ===")
    sim = UR10Sim(headless=True)
    
    print("Testing the simulation loop with 50 steps...")
    for i in range(50):
        sim.world.step(render=False)
        
    print("Closing the simulation...")
    sim.cleanup()
    print("=== TEST COMPLETED SUCCESSFULLY WITH NO ERRORS! ===")
    sys.exit(0)
except Exception as e:
    print(f"=== ERROR ENCOUNTERED ===\n{e}")
    sys.exit(1)