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

# ===========================================
# EIXO
#

L       = [0.3, 0.3, 0.052]   # comprimento
i_d     = 0                   # diâmetro interno
o_d     = 0.0127              # diâmetro externo
N_shaft = 3                   # quantidade de elementos

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
    tag=(f"Elemento {i} do eixo")
  )
  for i in range(N_shaft)
]

# ===========================================
# DISCO
#
# Utilizando as propriedades geométricas:

disk_geo = rs.DiskElement.from_geometry(
  n=1,
  material=ASTMA36,
  width=0.01,
  i_d=0.0127,
  o_d=0.1807,
  tag="Geometria do disco"
)

# ===========================================
# ROLAMENTOS E VEDAÇÕES
#

N_bearing = 2

n_balls   = 7
d_balls   = 0.006
fs        = 10
alpha     = (np.pi / 18)
bearings  = [
  rs.BallBearingElement(
    n=i*2,
    n_balls=n_balls,
    d_balls=d_balls,
    fs=fs,
    alpha=alpha,
    tag=(f"Rolamento de esferas {i}")
  )
  for i in range(N_bearing)
]

# ===========================================
# ROTOR
#

rotor = rs.Rotor(shaft_elements, [disk_geo], bearings)
rotor.plot_rotor()

# ===========================================
# DIAGRAMA DE CAMPBELL
#

samples     = 50
speed_range = np.linspace(20, 1000, samples) # [rad/s]
campbell    = rotor.run_campbell(speed_range)
campbell.plot()