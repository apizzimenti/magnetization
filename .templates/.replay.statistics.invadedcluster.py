
from ateams.statistics import Player
from pathlib import Path
from math import comb
import numpy as np
import json, sys

# Read metadata from designated directory.
STAMP = sys.argv[-1] if len(sys.argv) > 1 else "TEST"
ROOT = Path("./output/tape")/STAMP
STATS = Path("./output/statistics")/STAMP
with open(ROOT/"metadata.json") as f: METADATA = json.load(f)

if not STATS.exists(): STATS.mkdir()

DIM = METADATA["dimension"]
SCALE = METADATA["scale"][0]
RANK = comb(DIM*2, DIM)
F = METADATA["field"]
N = METADATA["iterations"]

OCCUPIED = np.empty((N, RANK))

with Player().playback(ROOT/"tape.lz", steps=N) as play:
	t = 0

	for (occupied, satisfied) in play.progress():
		occupieds = occupied.reshape((RANK, -1))
		summed = occupieds.sum(axis=1)/satisfied.sum()
		OCCUPIED[t] = summed
		t += 1
	
	OCCUPIED = OCCUPIED.T
	OCCUPIED = OCCUPIED.cumsum(axis=1)/np.arange(1, N+1)
	OCCUPIED = OCCUPIED.flatten()
	np.save(STATS/"occupation", OCCUPIED)


with open(STATS/"metadata.json", "w") as w: json.dump(METADATA, w, indent=2)
