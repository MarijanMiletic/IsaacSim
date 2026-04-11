import os
import numpy as np
import logging

# Mandatory fix for Windows environment
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

from isaacsim import SimulationApp

# Start Isaac Sim in visible (non-headless) mode with a window
simulation_app = SimulationApp({"headless": False})

# Silence internal Isaac Sim logs
import carb
logging.getLogger("omni").setLevel(logging.ERROR)
carb.settings.get_settings().set_string("/log/level", "error")

# Import basic 'World' for physics and scene from the new Isaac Sim API
from isaacsim.core.api import World
# Import the ready-made 'Franka' robot from manipulator examples
from isaacsim.robot.manipulators.examples.franka import Franka

print("Initializing the scene and loading the robot model (this may take a few seconds)...")

# 1. Create a world with a ground plane and lighting
world = World()
world.scene.add_default_ground_plane()

# 2. Add the Franka robot to the scene
# Instantiate the robot by specifying its path in the USD tree and initial position
franka_robot = world.scene.add(
    Franka(
        prim_path="/World/My_Franka",
        name="franka_robot",
        position=np.array([0.0, 0.0, 0.0]) # Place it exactly in the center of the world [X, Y, Z]
    )
)

# 3. MANDATORY: Reset the world before starting the simulation loop
# This forces the robot to instantiate and prepare its physics
world.reset()

print("\n" + "="*50)
print("Robot successfully loaded and the simulation is running!")
print("You can rotate the camera by holding the Left Mouse Button + ALT.")
print("Move around using W, A, S, D keys (like in a video game) while holding the Right Mouse Button.")
print("To exit and stop the script, simply close the Isaac Sim window.")
print("="*50 + "\n")

# 4. Main simulation loop
# Runs infinitely, until you click 'X' on the Isaac Sim window
while simulation_app.is_running():
    # In this loop, we compute one step of physics (step) and refresh the screen (render)
    # This is where you would normally inject logic to send commands to the robot
    world.step(render=True)

# 5. Cleanly shut down the application upon exiting the loop
simulation_app.close()