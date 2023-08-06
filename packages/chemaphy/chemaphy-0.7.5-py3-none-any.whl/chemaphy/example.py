import chemaphy
from chemaphy import ProjectileMotion as pm
from chemaphy import LogicGates as lg

print(pm.HorizontalRange(100,chemaphy.g_earth.value,45))
print(lg.OR(1,0))
