
from ateams.structures import Lattice
from ateams.models import InvadedCluster
from ateams.stats import autocorrelation
from ateams import Chain, Tape, _version
from pathlib import Path
import numpy as np
import math
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
# temp = metadata["temperature"]

homology = 2
rank = math.comb(len(L.corners), homology)
SW = InvadedCluster(L, homology=homology, stop=rank/2)
outputs = {
    0: np.array([-1]*len(L.boundary[homology-1])),
    1: np.array([-1]*rank*len(L.boundary[homology])),
    2: np.array([-1]*len(L.boundary[homology]))
}

# Tape player.
compressed = True
p = Tape.Player()

spins = np.zeros((metadata["iterations"], len(L.boundary[homology-1]))).astype(int)
percolates = np.zeros((metadata["iterations"], rank*len(L.boundary[homology]))).astype(int)
completes = np.zeros((metadata["iterations"], len(L.boundary[homology]))).astype(int)

with p.playback(SW, fp/"tape.jsonl.gz", outputs=outputs, compressed=compressed) as chain:
    t = 0

    for (s, p, c) in chain.progress():
        spins[t] = s
        percolates[t] = p
        completes[t] = c
        t += 1

    out = Path(f"output/statistics/{stamp}")
    if not out.exists(): out.mkdir()
    
    for name, x in zip(["spins", "occupied", "satisfied"], [spins, percolates, completes]):
        np.savetxt(out/f"{name}.gz", x)

    # also compute autocorrelation data for the run.
    occupied = completes.sum(axis=1)
    autos = autocorrelation(occupied)
    np.savetxt(out/"autocorrelation.gz", autos)

    with open(out/"metadata.json", "w") as w: json.dump(metadata, w)