
import numpy as np
from ateam.structures import Lattice
from ateam.stats import critical

# Construct lattice object.
L = Lattice()
L.fromFile("lattice.json")

t = critical(L.field.order)(0)
X = np.linspace(0, t, 10)
Y = X**4
Y = -np.concatenate([t-Y, t+Y])
Y = Y[Y < 0]
Y.sort()

with open("temps.distribution.txt", "w") as w:
	for y in Y: w.write(f"{y}\n")
