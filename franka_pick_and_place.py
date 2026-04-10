import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

from isaacsim import SimulationApp
# Start Isaac Sim with GUI
simulation_app = SimulationApp({"headless": False})

import numpy as np
from isaacsim.core.api import World
from isaacsim.robot.manipulators.examples.franka import Franka
from isaacsim.core.api.objects import DynamicCuboid
from isaacsim.robot.manipulators.examples.franka import FrankaController

# 1. Setup the World
world = World(stage_units_in_meters=1.0)
world.scene.add_default_ground_plane()

# 2. Add Franka Robot
franka = world.scene.add(
    Franka(
        prim_path="/World/Franka",
        name="my_franka",
        position=np.array([0, 0, 0])
    )
)

# 3. Add a Cube to pick up
cube = world.scene.add(
    DynamicCuboid(
        prim_path="/World/Cube",
        name="my_cube",
        position=np.array([0.5, 0.2, 0.05]), # Position in front of the robot
        scale=np.array([0.05, 0.05, 0.05]), # 5cm cube
        color=np.array([1.0, 0.0, 0.0]) # Red color
    )
)

# 4. Initialize the Pick and Place Controller
# This is a high-level controller that handles the sequence of movements
controller = FrankaController(name="pick_and_place_controller", deterministic_flag=True)

world.reset()

print("\n--- Starting Pick and Place Simulation ---")
print("The robot will now attempt to pick up the red cube and move it.")

i = 0
while simulation_app.is_running():
    world.step(render=True)
    
    if world.is_playing():
        if world.current_time_step_index == 0:
            world.reset()
            controller.reset()
        
        # Get current state
        observations = world.get_observations()
        
        # Define the target: pick the cube at its current position and place it elsewhere
        # Logic: every 500 steps, we re-calculate or trigger actions
        # In a real scenario, we would use a state machine
        
        # This simple example uses the built-in Franka controller for basic tasks
        # For a full pick-and-place, we usually define a sequence of targets
        
        # Let's make it simple: move the end-effector to the cube
        cube_position, _ = cube.get_world_pose()
        
        # Apply actions from the controller to reach the cube
        actions = controller.forward(
            target_end_effector_position=cube_position + np.array([0, 0, 0.02]), # Slightly above cube
            target_end_effector_orientation=None
        )
        
        franka.apply_action(actions)

simulation_app.close()
