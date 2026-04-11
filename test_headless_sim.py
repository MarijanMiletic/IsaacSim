import os
import sys
import time
import logging

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

print("Starting Isaac Sim in 'headless' mode (without window) for physics test...")

try:
    from isaacsim import SimulationApp
    # Here we use headless mode so the window doesn't open while testing in the terminal
    simulation_app = SimulationApp({"headless": True, "anti_aliasing": 0})

    # Optional: Silence internal Isaac Sim logs to keep the terminal clean
    import carb
    logging.getLogger("omni").setLevel(logging.ERROR)
    carb.settings.get_settings().set_string("/log/level", "error")

    from isaacsim.core.api import World
    import isaacsim.core.utils.prims as prims_utils

    print("Creating the world and adding physics objects (ground and cube).")
    world = World()
    world.scene.add_default_ground_plane()

    # A falling cube
    prims_utils.create_prim(
        prim_path="/World/TestCube",
        prim_type="Cube",
        position=[0.0, 0.0, 10.0]
    )

    world.reset()

    print("Simulating 200 frames of a falling cube...")
    start_time = time.time()
    for i in range(200):
        world.step(render=False)
    
    elapsed = time.time() - start_time
    print(f"SUCCESS: Simulation completed in {elapsed:.2f} seconds. Physics engine is working.")

    simulation_app.close()
    sys.exit(0)

except Exception as e:
    print(f"\n--- CRITICAL ERROR DURING SIMULATION --- \n{e}")
    sys.exit(1)