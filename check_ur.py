import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
from isaacsim import SimulationApp
simulation_app = SimulationApp({"headless": True, "anti_aliasing": 0})

import isaacsim.robot.manipulators.examples.universal_robots as ur
print("UR EXPORTS: ", dir(ur))

simulation_app.close()