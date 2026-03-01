
from ateams.statistics import Player, bettis
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
RANK = METADATA["rank"]
N = METADATA["iterations"]
CELLS = METADATA["cells"]
TRANCHES = np.array(METADATA["tranches"])

OCCUPIED = np.empty((N, RANK))
ESSENTIAL = np.zeros(sum([comb(2*DIM,k) for k in range(2*DIM+1)]))
CURVES = np.zeros((2*DIM+1, CELLS))

with Player().playback(ROOT/"tape.lz", steps=N, dtypes=(int,int,int,int)) as play:
	t = 0

	for (occupied, essential, total, pairs) in play.progress():
		occupieds = occupied.reshape((RANK, -1))
		summed = occupieds.sum(axis=1)/occupieds.shape[1]
		OCCUPIED[t] = summed

		# Compute betti curves; add to the average.
		pairs = pairs.reshape((2,-1))
		curves = bettis(pairs, total, TRANCHES)
		
		for dimension in range(curves.shape[0]):
			CURVES[dimension] = CURVES[dimension]*(t/(t+1)) + curves[dimension]/(t+1)

		# Get the expected time our giant cycles show up.
		ESSENTIAL = ESSENTIAL*(t/(t+1)) + total/(t+1)

		t += 1
	
	OCCUPIED = OCCUPIED.T
	OCCUPIED = OCCUPIED.cumsum(axis=1)/np.arange(1, N+1)
	OCCUPIED = OCCUPIED.flatten()
	np.save(STATS/"occupation", OCCUPIED)

	np.save(STATS/"curves", CURVES)
	np.save(STATS/"giants", ESSENTIAL)


with open(STATS/"metadata.json", "w") as w: json.dump(METADATA, w, indent=2)
