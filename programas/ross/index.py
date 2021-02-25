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
L       = [0.295, 0.005, 0.005, 0.295, 0.052]   # length
i_d     = 0                                     # inner diameter
o_d     = 0.0127                                # outer diameter
N_shaft = 4                                     # number of elements

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
  n=2,
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

stfx = 1e6
stfy = 0.8e6
bearings = [
  rs.BearingElement(
    n=i*4,
    kxx=stfx,
    kyy=stfy,
    cxx=1e3,
    tag=(f"Bearing {i}")
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