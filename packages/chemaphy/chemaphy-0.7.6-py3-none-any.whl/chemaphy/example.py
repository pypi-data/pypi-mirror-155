from chemaphy import ProjectileMotion as pm
from chemaphy import LogicGates as lg
import pandas_datareader as pdr

print(pm.HorizontalRange(100,pm.g_earth.value,45))
print(lg.OR(1,0))
