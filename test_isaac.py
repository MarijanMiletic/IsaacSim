import os
import logging

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

from isaacsim import SimulationApp

# Initialize application - headless: False means the window will open
simulation_app = SimulationApp({"headless": False})

# Silence internal Isaac Sim logs
import carb
logging.getLogger("omni").setLevel(logging.ERROR)
carb.settings.get_settings().set_string("/log/level", "error")

from isaacsim.core.api import World
import isaacsim.core.utils.prims as prims_utils

print("Preparing the scene...")
world = World()
world.scene.add_default_ground_plane()

# Add a cube to the space
prims_utils.create_prim(
    prim_path="/World/Cube",
    prim_type="Cube",
    position=[0.0, 0.0, 5.0],  # High up in the air so we can see the fall
)

world.reset()

print("Simulation started successfully! A window with a cube is displayed. It will close automatically after a short time.")

# Run the simulation for about 1500 steps
for _ in range(1500):
    world.step(render=True)

simulation_app.close()