
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

OCCUPIED = np.empty(N, dtype=np.float64)
GIANTS = np.empty(N, dtype=int)
PERCENTAGES = np.zeros((N, RANK), dtype=np.float64)

with Player().playback(ROOT/"tape.lz", steps=N, dtypes=(np.uint8, int)) as play:
	t = 0

	for (occupied, giants) in play.progress():
		OCCUPIED[t] = occupied.sum()/occupied.shape[0]
		GIANTS[t] = (giants[giants > 0]).shape[0]
		PERCENTAGES[t,:GIANTS[t]] = ((giants-TRANCHES[DIM,0])/occupied.shape[0])[:GIANTS[t]]
		t += 1
	
	np.save(STATS/"occupation", OCCUPIED)
	np.save(STATS/"giants", GIANTS)
	np.save(STATS/"percentages", PERCENTAGES)


with open(STATS/"metadata.json", "w") as w: json.dump(METADATA, w, indent=2)
