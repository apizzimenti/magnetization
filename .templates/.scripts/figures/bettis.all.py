
import numpy as np
import json
from pathlib import Path
import matplotlib.pyplot as plt

# Turn on latex.
plt.rcParams.update({"text.usetex": True})

ROOT = Path("./../../")
STATS = ROOT/"output/statistics"
OUT = ROOT/"output/figures/bettis"
TEST = False

if not OUT.exists(): OUT.mkdir()

try:
	with open(ROOT/"timestamps.txt") as f: STAMPS = [s.strip() for s in f.readlines()]
	assert len(STAMPS) > 0
	assert not TEST
except:
	STAMPS = ["TEST"]

for STAMP in STAMPS:
	with open(ROOT/"output/statistics"/STAMP/"metadata.json") as f: METADATA = json.load(f)

	N = METADATA["iterations"]
	RANK = METADATA["rank"]//2
	TRANCHES = np.array(METADATA["tranches"])
	z = 1/2

	# Load betti curve data.
	curves = np.load(STATS/STAMP/"curves.npy")
	giants = np.load(STATS/STAMP/"giants.npy")

	# Create blank plots, set aspect ratio, limits, etc.
	fig, ax = plt.subplots(figsize=(5,3))
	m = -1
	# ax.spines[["right", "top"]].set_visible(False)

	for dimension in range(curves.shape[0]):
		lo, hi = TRANCHES[dimension]
		X = np.arange(curves.shape[1])/METADATA["cells"]
		# Y = curves[dimension]
		Y = curves[dimension]/METADATA["cells"]

		curve = ax.plot(X,Y, label=f"$H_{dimension}(Q_t)$")[0]
		subgiants = giants[(lo <= giants) & (giants < hi)]
		print(dimension, subgiants)
		ax.scatter(subgiants/METADATA["cells"], [0]*len(subgiants), s=8, color=curve.get_color(), marker="x", zorder=1000)
	
	ax.set_xlabel(r"$t/N$", fontsize=8)
	ax.set_ylabel(r"$H_k(Q_t)/N$", fontsize=8)
	ax.legend(fontsize=6)
	plt.savefig(OUT/f"{METADATA['scale'][0]}.jpeg", bbox_inches="tight", dpi=1200)

