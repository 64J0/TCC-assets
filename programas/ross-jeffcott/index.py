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
steel = rs.Material(name="Steel", rho=7810, E=211e9, Poisson=0.3)
# print(steel)

# Salva em um arquivo .toml, que pode ser lido como .txt
# Este arquivo é salvo na pasta raiz com o nome available_materials.toml
steel.save_material()
# print(rs.Material.available_materials()) # ['Steel']

# ========================================================================
# EIXO
#
# Permite criar elementos de eixo cilíndricos e cônicos, ou seja, é
# possível definir diâmetros diferentes para o raio interno e externo
L       = 0.25 # length
i_d     = 0    # inner diameter
o_d     = 0.05 # outer diameter
N_shaft = 6    # number of elements

shaft_elements = [
  rs.ShaftElement(
    L=L,
    idl=i_d,
    odl=o_d,
    material=steel,
    shear_effects=True,
    rotary_inertia=True,
    gyroscopic=True,
    tag=(f"Shaft {i}")
  )
  for i in range(N_shaft)
]
# print(shaft_elements)

# ========================================================================
# DISCO
#
# Disco rígido, utilizado apenas para adicionar massa e inércia ao sistema,
# desconsiderando sua rigidez (idealmente infinita)
#
# ROSS permite criar o elemento de disco utilizando as propriedades de inércia:
disk = rs.DiskElement(
  n=3,
  m=32.58,
  Ip=0.178,
  Id=0.329,
  tag="Inertia disk"
)

# E também utilizando as propriedades geométricas
disk_geo = rs.DiskElement.from_geometry(
  n=4,
  material=steel,
  width=0.07,
  i_d=0.05,
  o_d=0.28,
  tag="Geometry disk"
)

# ========================================================================
# ROLAMENTOS E VEDAÇÕES
#
# São os elementos que adicionam rigidez e/ou amortecimento ao sistema.
# Podem ser criados de vários tipos, inclusive do tipo de esferas, como é o
# caso encontrado na bancada do meu TCC
N_bearing = 2

stfx = 1e6
stfy = 0.8e6
bearings = [
  rs.BearingElement(
    n=0,
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
rotor = rs.Rotor(shaft_elements, [disk], bearings)
print("Rotor total mass = ", np.round(rotor.m, 2))
print("Rotor center of gravity =", np.round(rotor.CG, 2))
rotor.plot_rotor()