
from ateam.structures import Lattice

# Create the lattice we're operating on.
L = Lattice()
L.fromCorners([6,6,6,6])
L.toFile("lattice.json")
