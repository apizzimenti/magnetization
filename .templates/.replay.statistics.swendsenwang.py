
from ateams.statistics import Player, constant, totalEnergy, occupancy
from ateams.models import SwendsenWang
from construction import buildcomplex
from pathlib import Path
import numpy as np
import json, sys

# Read metadata from designated directory.
STAMP = sys.argv[-1] if len(sys.argv) > 1 else "TEST"
ROOT = Path("./output/tape")/STAMP
STATS = Path("./output/statistics")/STAMP
with open(ROOT/"metadata.json") as f: METADATA = json.load(f)

DIM = METADATA["dimension"]
SCALE = METADATA["scale"][0]
F = METADATA["field"]
N = METADATA["iterations"]

# Recreate all the variables for the experiment.
COMPLEX = buildcomplex(len(METADATA["scale"]), SCALE, _root="./../_shared")
MODEL = SwendsenWang(
	COMPLEX,
	dimension=DIM,
	field=F,
	temperature=constant(METADATA["temperature"])
)

statistics = [
	(occupancy, "occupancy"),
	(totalEnergy, "energy")
]

# Specify a burn-in.
BURN = int(0.25*N)
SAMPLE = N-BURN

# Compute stats, do whatever.
for statistic, name in statistics:
	res = np.empty(SAMPLE)
	t = 0

	with Player().playback(ROOT/"tape.lz", steps=N) as play:
		for state in play.progress():
			if t < BURN: t+=1; continue

			res[t-BURN] = statistic(state, MODEL)
			t += 1

	# Write the statistic to file.
	np.save(STATS/f"{name}", res)

METADATA["burn"] = BURN
with open(STATS/"metadata.json", "w") as w: json.dump(METADATA, w, indent=2)
