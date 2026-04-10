import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

from isaacsim import SimulationApp
simulation_app = SimulationApp({"headless": False})

import numpy as np
from isaacsim.core.api import World
from isaacsim.robot.manipulators.examples.franka import Franka
from isaacsim.core.api.objects import DynamicCuboid
from isaacsim.robot.manipulators.examples.franka.controllers.pick_place_controller import PickPlaceController

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

# 3. Add a Cube with better physics properties
cube = world.scene.add(
    DynamicCuboid(
        prim_path="/World/Cube",
        name="my_cube",
        position=np.array([0.5, 0.2, 0.1]), # Start higher (10cm) to drop safely
        scale=np.array([0.05, 0.05, 0.05]),
        color=np.array([1.0, 0.0, 0.0]),
        mass=0.2 # Heavier cube is more stable
    )
)

# 4. Initialize the Controller
world.reset()

# Specialized Franka PickPlaceController
controller = PickPlaceController(
    name="pick_place_controller",
    gripper=franka.gripper,
    robot_articulation=franka
)

# Define goal position for the cube
goal_position = np.array([0.5, -0.2, 0.05])

print("\n" + "🚀" * 10)
print("ISAAC SIM 4.5.0 ACTIVE - PICK AND PLACE")
print("Physics tuned: Cube mass increased for stability.")
print("🚀" * 10 + "\n")

while simulation_app.is_running():
    world.step(render=True)
    
    if world.is_playing():
        if world.current_time_step_index == 0:
            world.reset()
            controller.reset()
        
        cube_pos, _ = cube.get_world_pose()
        
        # Get actions
        actions = controller.forward(
            picking_position=cube_pos,
            placing_position=goal_position,
            current_joint_positions=franka.get_joint_positions()
        )
        
        # Apply the action
        franka.apply_action(actions)
        
        if world.current_time_step_index % 100 == 0:
            print(f"[STATUS] Step: {world.current_time_step_index} | Action phase: {controller.get_current_event()}")
            
        if controller.is_done():
            print("\n✅ TASK COMPLETED SUCCESSFULLY!")
            world.pause()

simulation_app.close()
