import os
import numpy as np
import logging

# Windows fix
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

from isaacsim import SimulationApp

class UR10TrackingSim:
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
        from isaacsim.robot.manipulators.examples.universal_robots.kinematics_solver import KinematicsSolver
        from isaacsim.core.utils.rotations import euler_angles_to_quat

        self.World = World
        self.UR10 = UR10
        self.DynamicCuboid = DynamicCuboid
        self.KinematicsSolver = KinematicsSolver
        self.euler_angles_to_quat = euler_angles_to_quat

        # Initialize the world
        self.world = self.World(stage_units_in_meters=1.0)
        self.world.scene.add_default_ground_plane()

        self.setup_scene()
        
    def setup_scene(self):
        """Adds the UR10 robot and a physical target to the scene."""
        print("Setting up the scene...")
        # Add UR10 Robot
        self.ur10 = self.world.scene.add(
            self.UR10(
                prim_path="/World/UR10",
                name="my_ur10",
                position=np.array([0, 0, 0]),
                attach_gripper=True
            )
        )

        # Add a physical Cube with gravity so it drops to the floor
        self.target = self.world.scene.add(
            self.DynamicCuboid(
                prim_path="/World/TargetCube",
                name="target_cube",
                position=np.array([0.6, 0.0, 0.5]), # Drop from 50cm
                scale=np.array([0.04, 0.04, 0.04]),
                color=np.array([1.0, 0.5, 0.0]), # Orange cube
                mass=0.1
            )
        )
        
        # Reset the world to prepare physics
        self.world.reset()

        # Initialize Inverse Kinematics Solver for UR10
        self.ik_solver = self.KinematicsSolver(
            robot_articulation=self.ur10,
            attach_gripper=True
        )

    def run(self):
        """Runs the main simulation state machine loop."""
        
        print("\n" + "🌟" * 10)
        print("ISAAC SIM 4.5.0 ACTIVE - UR10 DYNAMIC PICK & THROW")
        print("Robot uses S-Curve trajectory smoothing and realistically waits for the cube to drop.")
        print("🌟" * 10 + "\n")

        self.state = "SPAWN"
        self.wait_frames = 0
        self.total_frames = 1
        
        # Gripper orientation pointing straight down
        self.down_orientation = self.euler_angles_to_quat(np.array([0, np.pi, 0]))
        
        # We will interpolate the end effector target
        self.current_target_pos = np.array([0.3, 0.0, 0.5])
        self.start_pos = self.current_target_pos.copy()
        self.end_pos = self.current_target_pos.copy()
        
        def set_target(target, frames):
            self.start_pos = self.current_target_pos.copy()
            self.end_pos = target
            self.wait_frames = frames
            self.total_frames = frames

        while self.simulation_app.is_running():
            self.world.step(render=True)
            
            if self.world.is_playing():
                if self.world.current_time_step_index == 0:
                    self.world.reset()
                    self.state = "SPAWN"
                    self.current_target_pos = np.array([0.3, 0.0, 0.5])
                    self.wait_frames = 0
                    
                cube_pos, _ = self.target.get_world_pose()

                # Smooth interpolation (S-curve)
                if self.wait_frames > 0:
                    self.wait_frames -= 1
                    alpha = 1.0 - (self.wait_frames / self.total_frames)
                    alpha = alpha * alpha * (3 - 2 * alpha) # Smoothstep easing
                    self.current_target_pos = self.start_pos + (self.end_pos - self.start_pos) * alpha

                # Always apply IK for current target with fixed downward orientation
                action, success = self.ik_solver.compute_inverse_kinematics(
                    target_position=self.current_target_pos,
                    target_orientation=self.down_orientation
                )
                if success:
                    self.ur10.get_articulation_controller().apply_action(action)
                
                # Check if arm has reached target position (within 2cm) to wait correctly
                ee_pos, _ = self.ik_solver.compute_end_effector_pose()
                dist_to_target = np.linalg.norm(self.current_target_pos - ee_pos)
                is_at_target = dist_to_target < 0.02

                # STATE MACHINE TRANSITIONS
                if self.wait_frames <= 0 and (is_at_target or self.state in ["WAIT_FALL", "SPAWN", "GRASP", "RELEASE"]):
                    if self.state == "SPAWN":
                        drop_x = np.random.uniform(0.4, 0.6)
                        drop_y = np.random.uniform(-0.3, 0.3)
                        
                        # Set cube and wake physics
                        self.target.set_world_pose(position=np.array([drop_x, drop_y, 1.0]))
                        self.target.set_linear_velocity(np.zeros(3))
                        self.target.set_angular_velocity(np.zeros(3))
                        
                        self.ur10.gripper.open()
                        
                        self.state = "WAIT_FALL"
                        set_target(np.array([0.4, 0.0, 0.5]), 180) # Go to observation pose, wait 3s
                        print(f"\n[1] Nova kocka pada na lokaciju ({drop_x:.2f}, {drop_y:.2f})...")

                    elif self.state == "WAIT_FALL":
                        self.state = "APPROACH"
                        # Hover 30cm above the cube to avoid any collisions during sweep
                        hover_pos = cube_pos + np.array([0.0, 0.0, 0.30])
                        set_target(hover_pos, 150) # Smooth slower move
                        print(f"[2] Približavam se iznad kocke...")

                    elif self.state == "APPROACH":
                        self.state = "GO_DOWN"
                        # Move precisely down to the cube, offset by 0.145m to account for UR10 gripper physical length
                        grab_pos = cube_pos + np.array([0.0, 0.0, 0.145])
                        set_target(grab_pos, 100) # Slower precision landing
                        print("[3] Precizno spuštanje na kocku...")

                    elif self.state == "GO_DOWN":
                        self.state = "GRASP"
                        set_target(self.current_target_pos, 60) # Wait 1s
                        self.ur10.gripper.close()
                        print("[4] Hvatanje aktivirano (Surface Gripper)...")

                    elif self.state == "GRASP":
                        self.state = "LIFT_AND_THROW"
                        throw_position = np.array([0.0, 0.5, 0.4])
                        set_target(throw_position, 150) 
                        print("[5] Podižem i pomičem kocku na stranu...")

                    elif self.state == "LIFT_AND_THROW":
                        self.state = "RELEASE"
                        set_target(self.current_target_pos, 60) # Wait 1s before opening
                        self.ur10.gripper.open()
                        print("[6] Otpuštanje. Reset...")

                    elif self.state == "RELEASE":
                        self.state = "SPAWN"

        self.cleanup()
        
    def cleanup(self):
        """Closes the simulation cleanly."""
        print("Shutting down the simulation...")
        self.simulation_app.close()

if __name__ == "__main__":
    sim = UR10TrackingSim(headless=False)
    sim.run()