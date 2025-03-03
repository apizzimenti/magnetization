
from ateams.structures import Lattice
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import json
import math

# Load data.
output = Path("../../output")
statistics = output/"statistics"

with open("../../stamps.txt", "r") as f: stamps = [s.strip() for s in f]
with open(statistics/stamps[-1]/"metadata.json", "r") as f: metadata = json.load(f)

amortized = np.loadtxt(statistics/"amortized.thresholds.gz")
iterations = len(amortized[0])

L = Lattice()
L.fromFile("../../lattice.json")
homology = 2
length = len(L.boundary[homology])
rank = math.comb(len(L.corners), homology)

plt.rcParams['text.usetex'] = True
fig, ax = plt.subplots(figsize=(3,1.5))
ax.spines[["right", "top"]].set_visible(False)
j = 0

cumulatives = []

for data in amortized:
	# Compute ratios and plot them over time.
	burn = int(iterations/25)
	times = np.arange(1, iterations+1)
	rolling = data.cumsum()/times

	# if j == 0: ax.plot(times, rolling, alpha=1/4, color="k", lw=1.5)
	ax.plot(times[burn:], rolling[burn:], color="k", lw=1.5, alpha=1/4 if j != 2 else 1)
	ax.text(
		iterations*0.65, rolling[-1]+0.002,
		s=rf"$\mathbf{{b}}_{{k-1}}(X_{{t-1}}) = {j+1}$", fontsize="xx-small",
		alpha=1/2 if j != 2 else 1
	)
	j += 1

# Critical temperature.
q = np.sqrt(metadata["field"])/(1+np.sqrt(metadata["field"]))
ax.hlines(
	y=q,
	xmin=0, xmax=metadata["iterations"],
	ls=":", lw=3/4, color="k"
)

# Set and adjust ticks.
adj = 0.01
ax.set_xticklabels([rf"${int(t)}$" for t in ax.get_xticks() if t > -1], fontsize=6)

yticks = ax.get_yticks()
ax.set_xlim(0, 1.01*iterations)
ax.set_ylim(0.55, 0.63)
ax.set_yticks(np.arange(0.55, 0.64, 0.02))
ax.set_yticklabels([rf"${round(t, 2)}$" for t in ax.get_yticks()], fontsize=6)

plt.savefig(output/"figures"/f"expectations-split-{metadata['dimension']}-{metadata['field']}-amortized.jpeg", bbox_inches="tight", dpi=600, pad_inches=0)

