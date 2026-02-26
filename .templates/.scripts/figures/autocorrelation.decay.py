
import numpy as np
import json
from pathlib import Path
import matplotlib.pyplot as plt
from ateams.statistics import cutoffs

ROOT = Path("./../../")
STATS = ROOT/"output/statistics"
with open(ROOT/"timestamps.txt") as f: STAMPS = [s.strip() for s in f.readlines()]

statistics = ["energy", "occupancy"]

STOP = 100

for STAMP in STAMPS:
	with open(STATS/STAMP/"metadata.json") as f: METADATA = json.load(f)
	for statistic in statistics:
		normalized = np.load(STATS/STAMP/f"{statistic}.autocorrelation.normalized.npy")
		integrated = np.load(STATS/STAMP/f"{statistic}.autocorrelation.integrated.npy")
		M = cutoffs.rectangular(integrated, c=7)

		plt.plot(range(M), normalized[:M])
		plt.yscale("log")
		plt.show()
