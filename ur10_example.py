import os
import numpy as np
import logging

# Windows fix
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

from isaacsim import SimulationApp

class UR10Sim:
    def __init__(self, headless=False):
        """Initializes the Isaac Sim simulation application and scene."""
        print("Starting Isaac Sim...")
        self.simulation_app = SimulationApp({"headless": headless})
        
        # Silence internal Isaac Sim logs
        import carb
        logging.getLogger("omni").setLevel(logging.ERROR)
        carb.settings.get_settings().set_string("/log/level", "error")

        from isaacsim.core.api import World
        from isaacsim.robot.manipulators.examples.universal_robots import UR10
        from isaacsim.core.api.objects import DynamicCuboid

        self.World = World
        self.UR10 = UR10
        self.DynamicCuboid = DynamicCuboid

        # Initialize the world
        self.world = self.World(stage_units_in_meters=1.0)
        self.world.scene.add_default_ground_plane()

        self.setup_scene()
        
    def setup_scene(self):
        """Adds the UR10 robot and a reference cube to the scene."""
        print("Setting up the scene...")
        # Add UR10 Robot
        self.ur10 = self.world.scene.add(
            self.UR10(
                prim_path="/World/UR10",
                name="my_ur10",
                position=np.array([0, 0, 0])
            )
        )

        # Add a reference Cube
        self.cube = self.world.scene.add(
            self.DynamicCuboid(
                prim_path="/World/Cube",
                name="reference_cube",
                position=np.array([0.6, 0.0, 0.05]),
                scale=np.array([0.05, 0.05, 0.05]),
                color=np.array([0.0, 0.0, 1.0]), # Blue cube
                mass=0.1
            )
        )
        
        # Reset the world to prepare physics
        self.world.reset()

    def run(self):
        """Runs the main simulation loop."""
        from isaacsim.core.utils.types import ArticulationAction
        
        print("\n" + "🚀" * 10)
        print("ISAAC SIM 4.5.0 ACTIVE - UR10 EXAMPLE")
        print("Robot loaded. Simulation running with custom joint movement...")
        print("🚀" * 10 + "\n")

        time_elapsed = 0.0

        while self.simulation_app.is_running():
            self.world.step(render=True)
            
            if self.world.is_playing():
                if self.world.current_time_step_index == 0:
                    self.world.reset()
                    time_elapsed = 0.0
                
                # Calculate time elapsed
                dt = self.world.get_physics_dt()
                time_elapsed += dt

                # Create a smooth sine wave movement for all 6 joints of UR10
                target_positions = np.zeros(self.ur10.num_dof)
                
                # Base rotation (Shoulder Pan)
                target_positions[0] = np.sin(time_elapsed * 0.5) * 1.5 
                # Shoulder Lift
                target_positions[1] = -1.5 + np.sin(time_elapsed * 0.8) * 0.5
                # Elbow
                target_positions[2] = 1.0 + np.sin(time_elapsed * 0.7) * 0.8
                # Wrist 1
                target_positions[3] = -1.0 + np.sin(time_elapsed * 1.2) * 0.5
                # Wrist 2
                target_positions[4] = np.sin(time_elapsed * 1.5) * 1.0
                # Wrist 3
                target_positions[5] = np.sin(time_elapsed * 2.0) * 1.0

                # Apply the joint positions using the Articulation Controller
                action = ArticulationAction(joint_positions=target_positions)
                self.ur10.get_articulation_controller().apply_action(action)

        self.cleanup()
        
    def cleanup(self):
        """Closes the simulation cleanly."""
        print("Shutting down the simulation...")
        self.simulation_app.close()

if __name__ == "__main__":
    # Create the simulation instance and run it
    sim = UR10Sim(headless=False)
    sim.run()