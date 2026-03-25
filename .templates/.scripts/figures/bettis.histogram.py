
import numpy as np
import json
from pathlib import Path
import matplotlib.pyplot as plt

from config import plot

ROOT = Path("./../../")
STATS = ROOT/"output/statistics"
OUT = ROOT/"output/figures/bettis"
TEST = False

if not OUT.exists(): OUT.mkdir()

try:
	with open(ROOT/"completed.txt") as f: STAMPS = [s.strip() for s in f.readlines()]
	assert len(STAMPS) > 0
	assert not TEST
except:
	STAMPS = ["TEST"]

for STAMP in STAMPS:
	with open(ROOT/"output/statistics"/STAMP/"metadata.json") as f: METADATA = json.load(f)

	N = METADATA["iterations"]
	RANK = METADATA["rank"]

	# Load histogram data.
	giants = np.load(STATS/STAMP/"giants.npy")
	values, bars = np.unique(giants, return_counts=True)

	# Give all bar heights.
	X = np.arange(0, RANK+1)
	Y = np.zeros(RANK+1, dtype=int)
	for t in range(values.shape[0]): Y[values[t]] = bars[t]
	
	# Create the plot.
	plt.rcParams.update(**plot.rcParams)
	fig, ax = plt.subplots(figsize=plot.figsize)
	histogram = ax.bar(X, Y, width=0.77)

	ax.set_xticks(X)
	ax.set_xticklabels(X)
	ax.set_xlim(-1, RANK+1)

	plt.show()

