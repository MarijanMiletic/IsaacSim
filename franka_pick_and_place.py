import os
import numpy as np
import logging

# Windows fix
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

from isaacsim import SimulationApp

class FrankaSim:
    def __init__(self, headless=False):
        """Initializes the Isaac Sim simulation application and scene."""
        print("Starting Isaac Sim...")
        self.simulation_app = SimulationApp({"headless": headless})
        
        # Silence internal Isaac Sim logs
        import carb
        logging.getLogger("omni").setLevel(logging.ERROR)
        carb.settings.get_settings().set_string("/log/level", "error")

        from isaacsim.core.api import World
        from isaacsim.robot.manipulators.examples.franka import Franka
        from isaacsim.core.api.objects import DynamicCuboid
        from isaacsim.robot.manipulators.examples.franka.controllers.pick_place_controller import PickPlaceController

        self.World = World
        self.Franka = Franka
        self.DynamicCuboid = DynamicCuboid
        self.PickPlaceController = PickPlaceController

        # Initialize the world
        self.world = self.World(stage_units_in_meters=1.0)
        self.world.scene.add_default_ground_plane()

        self.setup_scene()
        
    def setup_scene(self):
        """Adds the robot and the cube to the scene."""
        print("Setting up the scene...")
        # Add Franka Robot
        self.franka = self.world.scene.add(
            self.Franka(
                prim_path="/World/Franka",
                name="my_franka",
                position=np.array([0, 0, 0])
            )
        )

        # Add a Cube with better physics properties
        self.cube = self.world.scene.add(
            self.DynamicCuboid(
                prim_path="/World/Cube",
                name="my_cube",
                position=np.array([0.5, 0.2, 0.1]), # Start higher (10cm) to drop safely
                scale=np.array([0.05, 0.05, 0.05]),
                color=np.array([1.0, 0.0, 0.0]),
                mass=0.2 # Heavier cube is more stable
            )
        )
        
        # We must reset the world before creating the controller
        self.world.reset()

        # Specialized Franka PickPlaceController
        self.controller = self.PickPlaceController(
            name="pick_place_controller",
            gripper=self.franka.gripper,
            robot_articulation=self.franka
        )

        # Define goal position for the cube
        self.goal_position = np.array([0.5, -0.2, 0.05])

    def run(self):
        """Runs the main simulation loop."""
        print("\n" + "🚀" * 10)
        print("ISAAC SIM 4.5.0 ACTIVE - PICK AND PLACE")
        print("Physics tuned: Cube mass increased for stability.")
        print("🚀" * 10 + "\n")

        while self.simulation_app.is_running():
            self.world.step(render=True)
            
            if self.world.is_playing():
                if self.world.current_time_step_index == 0:
                    self.world.reset()
                    self.controller.reset()
                
                cube_pos, _ = self.cube.get_world_pose()
                
                # Get actions
                actions = self.controller.forward(
                    picking_position=cube_pos,
                    placing_position=self.goal_position,
                    current_joint_positions=self.franka.get_joint_positions()
                )
                
                # Apply the action
                self.franka.apply_action(actions)
                
                if self.world.current_time_step_index % 100 == 0:
                    print(f"[STATUS] Step: {self.world.current_time_step_index} | Action phase: {self.controller.get_current_event()}")
                    
                if self.controller.is_done():
                    print("\n✅ TASK COMPLETED SUCCESSFULLY!")
                    self.world.pause()

        self.cleanup()
        
    def cleanup(self):
        """Closes the simulation cleanly."""
        print("Shutting down the simulation...")
        self.simulation_app.close()

if __name__ == "__main__":
    # Create the simulation instance and run it
    sim = FrankaSim(headless=False)
    sim.run()