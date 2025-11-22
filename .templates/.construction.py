
from ateams.complexes import Cubical
from pathlib import Path
import sys

# Create the lattice (if it hasn't already been created).
def buildcomplex(dimension, scale, _root="."):
	root = Path(_root)
	fname = root/Path(f"cubical.{dimension}.{scale}.json")

	if not fname.exists():
		fname.parent.mkdir(exist_ok=True)
		C = Cubical().fromCorners([scale]*dimension)
		C.toFile(fname)
	else:
		C = Cubical().fromFile(fname)

	return C


if __name__ == "__main__":
	DIM, SCALE = int(sys.argv[-2]), int(sys.argv[-1])
	buildcomplex(DIM, SCALE, _root="./../_shared/")
