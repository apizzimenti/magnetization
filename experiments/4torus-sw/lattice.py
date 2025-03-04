
from ateams.structures import Lattice

# Create the lattice we're operating on.
L = Lattice()
L.fromCorners([6,6,6,6], field=3, dimension=2)
L.toFile("lattice.json")
