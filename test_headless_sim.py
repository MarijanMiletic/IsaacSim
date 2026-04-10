import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import sys
import time

print("Pokrećem Isaac Sim u 'headless' načinu rada (bez prozora) za test fizike...")

try:
    from isaacsim import SimulationApp
    # Ovdje koristimo headless mod kako se prozor ne bi otvarao dok testiramo u terminalu
    simulation_app = SimulationApp({"headless": True, "anti_aliasing": 0})

    from omni.isaac.core import World
    import omni.isaac.core.utils.prims as prims_utils

    print("Stvaram svijet i dodajem fizikalne objekte (podloga i kocka).")
    world = World()
    world.scene.add_default_ground_plane()

    # Kocka koja će padati
    prims_utils.create_prim(
        prim_path="/World/TestKocka",
        prim_type="Cube",
        position=[0.0, 0.0, 10.0]
    )

    world.reset()

    print("Simuliram 200 frame-ova pada kocke...")
    start_time = time.time()
    for i in range(200):
        world.step(render=False)
    
    elapsed = time.time() - start_time
    print(f"USPJEH: Simulacija odrađena u {elapsed:.2f} sekundi. Fizikalni engine radi.")

    simulation_app.close()
    sys.exit(0)

except Exception as e:
    print(f"\n--- KRITIČNA GREŠKA TIJEKOM SIMULACIJE --- \n{e}")
    sys.exit(1)
