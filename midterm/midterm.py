from sparc.sparc_core import SPARC
from ase.build import molecule
from pandas import DataFrame
from ase.units import kJ, mol

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
hyd_energy = []
oxy_energy = []
reaction_energy = []
error = []
true = 285.8261 * kJ / mol

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

  renergy = (Eh + 0.5 * Eo - Ew)
  reaction_energy.append(renergy)
  error.append(100 * (renergy - true) / true)


energy = [reaction_energy, water_energy, hyd_energy, oxy_energy, error]
df = DataFrame (energy).transpose()
df.columns = ["Reaction Energy (eV)", "H2O Energy (eV)", "H2 Energy (eV)", "O2 Energy (eV)", "Error (%)"]
df.index = grid_spacings
print(df)
df.to_csv(r'/storage/home/hpaceice1/fwang356/sparc_run/VIP-Training/energy.csv')
