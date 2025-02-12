
from ateam.structures import Lattice
from ateam.models import SwendsenWang
from ateam.stats import constant, autocorrelation
from ateam import Chain, Tape, _version
from pathlib import Path
import numpy as np
import json
import sys

stamp = str(sys.argv[-1])

# Instantiate Lattice and Model.
L = Lattice()
L.fromFile("lattice.json")

# Get some metadata to configure the replay.
fp = Path("output/tape/")/stamp
with open(fp/"metadata.json", "r") as r: metadata = json.load(r)

dimension = metadata["dimension"]
temp = metadata["temperature"]

SW = SwendsenWang(L, temperatureFunction=constant(float(temp)))
outputs = {
    0: np.array([-1]*len(L.boundary[dimension-1])),
    1: np.array([-1]*len(L.boundary[dimension]))
}

# Tape player.
compressed = True
p = Tape.Player()

spins = np.zeros((metadata["iterations"], len(L.boundary[dimension-1]))).astype(int)
completes = np.zeros((metadata["iterations"], len(L.boundary[dimension]))).astype(int)

with p.playback(SW, fp/"tape.jsonl.gz", outputs=outputs, compressed=compressed) as chain:
    t = 0

    for (s, c) in chain:
        spins[t] = s
        completes[t] = c
        t += 1

    out = Path(f"output/statistics/{stamp}")
    if not out.exists(): out.mkdir()

    for name, x in zip(["spins", "satisfied"], [spins, completes]):
        np.savetxt(out/f"{name}.gz", x)

    # also compute autocorrelation data for the run.
    occupied = completes.sum(axis=1)
    autos = autocorrelation(occupied)
    np.savetxt(out/"autocorrelation.gz", autos)
