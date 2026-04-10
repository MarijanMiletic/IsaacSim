import os
# Obavezan popravak za Windows okruženje koji smo ranije otkrili
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

from isaacsim import SimulationApp
# Pokrećemo Isaac Sim u vidljivom (ne-headless) načinu rada s prozorom
simulation_app = SimulationApp({"headless": False})

import numpy as np
# Uvozimo osnovni 'World' za fiziku i scenu iz novog Isaac Sim API-ja
from isaacsim.core.api import World
# Uvozimo gotovog robota 'Franka' iz biblioteke primjera manipulatora
from isaacsim.robot.manipulators.examples.franka import Franka

print("Inicijaliziram scenu i preuzimam model robota (ovo može potrajati par sekundi)...")

# 1. Kreiramo svijet s podlogom i svjetlom
world = World()
world.scene.add_default_ground_plane()

# 2. Dodajemo Franka robota u scenu
# Robota instanciramo zadavanjem putanje u USD stablu i početne pozicije
franka_robot = world.scene.add(
    Franka(
        prim_path="/World/Moja_Franka",
        name="franka_robot",
        position=np.array([0.0, 0.0, 0.0]) # Smještamo ga u sami centar svijeta [X, Y, Z]
    )
)

# 3. OBAVEZNO: Resetiramo svijet prije početka simulacijske petlje
# Ovo prisiljava robota da se instancira i pripremi fiziku
world.reset()

print("\n" + "="*50)
print("Robot je uspješno učitan i simulacija se izvršava!")
print("Možete rotirati kameru držeći lijevu tipku miša + ALT.")
print("Pomičite se tipkama W, A, S, D (kao u videoigri) dok držite desnu tipku miša.")
print("Za izlazak i prekid skripte, jednostavno zatvorite prozor Isaac Sima.")
print("="*50 + "\n")

# 4. Glavna simulacijska petlja
# Vrti se beskonačno, sve dok vi ne kliknete 'X' na prozoru Isaac Sima
while simulation_app.is_running():
    # U ovoj petlji izračunavamo jedan korak fizike (step) i osvježavamo sliku na ekranu (render)
    # Tu biste inače ubacili logiku za slanje komandi robotu
    world.step(render=True)

# 5. Uredno gašenje aplikacije po izlasku iz petlje
simulation_app.close()
