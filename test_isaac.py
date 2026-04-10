import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

from isaacsim import SimulationApp

# Inicijalizacija aplikacije - headless: False znači da će se otvoriti prozor
simulation_app = SimulationApp({"headless": False})

from omni.isaac.core import World
import omni.isaac.core.utils.prims as prims_utils

print("Pripremam scenu...")
world = World()
world.scene.add_default_ground_plane()

# Dodajemo kocku u prostor
prims_utils.create_prim(
    prim_path="/World/Cube",
    prim_type="Cube",
    position=[0.0, 0.0, 5.0],  # Visoko u zraku da vidimo pad
)

world.reset()

print("Simulacija uspješno pokrenuta! Prikazuje se prozor s kockom. Zatvorit će se automatski nakon kratkog vremena.")

# Vrtimo simulaciju oko 20 sekundi (ovisno o brzini računala)
for _ in range(1500):
    world.step(render=True)

simulation_app.close()
