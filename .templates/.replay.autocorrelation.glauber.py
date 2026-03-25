
from ateams.statistics import unnormalized, integrated, totalEnergy, occupancy
from pathlib import Path
import numpy as np
import json, sys

# Read metadata from designated directory.
STAMP = sys.argv[-1] if len(sys.argv) > 1 else "TEST"
STATS = Path("./output/statistics")/STAMP
with open(STATS/"metadata.json") as f: METADATA = json.load(f)

if not STATS.exists(): STATS.mkdir()

statistics = [
	# (occupancy, "occupancy"),
	(totalEnergy, "energy")
]

# Compute stats, do whatever.
for statistic, name in statistics:
	X = np.load(STATS/f"{name}.npy")

	# Compute the normed autocorrelation, then use it to compute the integraged
	# autocorrelation.
	Y = unnormalized(X);
	Z = Y/Y[0];
	I = integrated(Z, isNormalized=True);

	np.save(STATS/f"{name}.autocorrelation", Y)
	np.save(STATS/f"{name}.autocorrelation.normalized", Z)
	np.save(STATS/f"{name}.autocorrelation.integrated", I)
