import os
import sys

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

from ur10_tracking import UR10TrackingSim

try:
    print("=== STARTING QUICK TEST FOR IK TRACKING IN HEADLESS MODE ===")
    sim = UR10TrackingSim(headless=True)
    
    print("Testing the simulation loop with 150 steps...")
    for i in range(150):
        sim.world.step(render=False)
        if sim.world.current_time_step_index == 0:
            sim.world.reset()
            sim.time_elapsed = 0.0
            
        import numpy as np
        dt = sim.world.get_physics_dt()
        
        target_x = 0.6
        target_y = np.sin(i * dt * 1.5) * 0.4
        target_z = 0.4 + np.sin(i * dt * 3.0) * 0.2
        new_position = np.array([target_x, target_y, target_z])
        sim.target.set_world_pose(position=new_position)
        
        action, success = sim.ik_solver.compute_inverse_kinematics(target_position=new_position)
        if success:
            sim.ur10.get_articulation_controller().apply_action(action)
        
    print("Closing the simulation...")
    sim.cleanup()
    print("=== TEST COMPLETED SUCCESSFULLY WITH NO ERRORS! ===")
    sys.exit(0)
except Exception as e:
    print(f"=== ERROR ENCOUNTERED ===\n{e}")
    sys.exit(1)