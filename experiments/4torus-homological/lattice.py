
from ateams.structures import Lattice

# Create the lattice we're operating on.
L = Lattice()
L.fromCorners([6,6,6,6], dimension=3, field=3)
L.toFile("lattice.json")
