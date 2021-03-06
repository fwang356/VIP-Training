from sparc.sparc_core import SPARC
from ase.build import molecule
from pandas import DataFrame
import warnings

warnings.filterwarnings("ignore")

water = molecule('H2O')
water.cell = [[6,0,0], [0,6,0], [0,0,6]]
water.center()
hyd = molecule('H2')
hyd.cell = [[6,0,0],[0,6,0],[0,0,6]]
hyd.center()
oxy = molecule('O2')
oxy.cell = [[6,0,0],[0,6,0],[0,0,6]]
oxy.center()

grid_spacings = [0.2, 0.16, 0.14, 0.12]
water_energy = []
water_total = []
hyd_energy = []
hyd_total = []
oxy_energy = []
oxy_total = []
reaction_energy = []

for x in grid_spacings:
  calc = SPARC(
               KPOINT_GRID = [1,1,1],
               h = x,
               EXCHANGE_CORRELATION = 'GGA_PBE',
               TOL_SCF = 1e-5,
               RELAX_FLAG = 1,
               PRINT_FORCES = 1,
               PRINT_RELAXOUT = 1)
  water.set_calculator(calc)
  hyd.set_calculator(calc)
  oxy.set_calculator(calc)

  Ew = water.get_potential_energy()
  Eh = hyd.get_potential_energy()
  Eo = oxy.get_potential_energy()
  water_energy.append(Ew)
  hyd_energy.append(Eh)
  oxy_energy.append(Eo)

  water_total.append(water.get_total_energy())
  hyd_total.append(hyd.get_total_energy())
  oxy_total.append(oxy.get_total_energy())

  Renergy = (Eh + 0.5 * Eo - Ew)
  reaction_energy.append(Renergy)


energy = [reaction_energy, water_energy, hyd_energy, oxy_energy]
df = DataFrame (energy).transpose()
df.columns = ["Reaction Energy", "H2O Total", "H2 Total", "O2 Total"]
df.index = grid_spacings
print(df)
df.to_csv(r'/storage/home/hpaceice1/fwang356/sparc_run/training_mid/energy.csv')
