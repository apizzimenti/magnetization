
from potts import Lattice, SwendsenWang, constant, Tape

# Instantiate Lattice and Model.
L = Lattice()
L.fromFile("lattice.json")
SW = SwendsenWang(L, temperatureFunction=constant(-0.441))

# Tape player.
fp = ""
compressed = True
p = Tape.Player()

with p.playback(SW, fp, compressed=compressed) as chain:
    for state in chain:
        print(state)
