import os
from pathlib import Path
import ross as rs
import numpy as np

# MATERIAL
#
# E       - Módulo de young
# G_s     - Módulo de cisalhamento (shear)
# Poisson - Coeficiente de Poisson
# rho     - Densidade do material
ABNT1020  = rs.Material(name="ABNT1020", rho=7850, E=2.05e11, Poisson=0.29)
ASTMA36   = rs.Material(name="ASTMA36", rho=7850, E=2e11, G_s=7.93e10)

# ========================================================================
# EIXO
#
L       = [0.3, 0.3, 0.052]   # length
i_d     = 0                                     # inner diameter
o_d     = 0.0127                                # outer diameter
N_shaft = 3                                     # number of elements

shaft_elements = [
  rs.ShaftElement(
    n=i,
    L=L[i],
    idl=i_d,
    odl=o_d,
    material=ABNT1020,
    shear_effects=True,
    rotary_inertia=True,
    gyroscopic=True,
    tag=(f"Shaft el. {i}")
  )
  for i in range(N_shaft)
]

# ========================================================================
# DISCO
#
# Utilizando as propriedades geométricas:
disk_geo = rs.DiskElement.from_geometry(
  n=1,
  material=ASTMA36,
  width=0.01,
  i_d=0.0127,
  o_d=0.1807,
  tag="Geometry disk"
)

# ========================================================================
# ROLAMENTOS E VEDAÇÕES
#
N_bearing = 2

n_balls   = 7
d_balls   = 0.006
fs        = 500.0
alpha     = (np.pi * 8) / (6 * n_balls)
bearings  = [
  rs.BallBearingElement(
    n=i*2,
    n_balls=n_balls,
    d_balls=d_balls,
    fs=fs,
    alpha=alpha,
    tag=(f"Ball Bearing {i}")
  )
  for i in range(N_bearing)
]

# ========================================================================
# ROTOR
#
rotor = rs.Rotor(shaft_elements, [disk_geo], bearings)
print("Rotor total mass = ", np.round(rotor.m, 2))
print("Rotor center of gravity =", np.round(rotor.CG, 2))
rotor.plot_rotor()

# CAMPBELL
samples     = 50
speed_range = np.linspace(200, 2000, samples)
campbell    = rotor.run_campbell(speed_range)
campbell.plot()