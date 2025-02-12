
from ateam.viz import points, shortestPath
from ateam.structures import Lattice
import matplotlib.pyplot as plt
import numpy as np
import json
from pathlib import Path

# Load data.
output = Path("../../output")
statistics = output/"statistics"
tape = output/"tape"/"1731442953.256813"

with open(tape/"metadata.json", "r") as r: metadata = json.load(r)

occupied = np.loadtxt(statistics/"occupied.gz").astype(int)
satisfied = np.loadtxt(statistics/"satisfied.gz").astype(int)

first = occupied[:,:800]
second = occupied[:,800:]

plt.rcParams['text.usetex'] = True
fig, ax = plt.subplots()

for data in [first, second]:
	# Compute ratios and plot them over time.
	burn = int(metadata["iterations"]/10)
	times = np.arange(1, metadata["iterations"]+1)
	ratios = data.sum(axis=1)/satisfied.sum(axis=1)
	rolling = ratios.cumsum()/times
	burned = (ratios[burn:].cumsum())/times[:metadata["iterations"]-burn]

	ax.plot(times, rolling, alpha=1/4, color="k", lw=1.5)
	ax.plot(times[burn:], burned, color="k", lw=1.5)

q = np.sqrt(metadata["field"])/(1+np.sqrt(metadata["field"]))
ax.hlines(
	y=q,
	xmin=0, xmax=metadata["iterations"],
	ls=":", lw=1, color="k"
)
adj = 0.005
ax.set_ylim(0.55-adj, 0.61+adj)
ax.set_xlim(0, 1.01*metadata["iterations"])

ax.set_yticks([0.55, q, 0.61])
ax.set_yticklabels([r"$0.55$", r"$\frac{\sqrt{q}}{1 + \sqrt{q}}$", r"$0.61$"])

xticks = list(range(0, metadata["iterations"]+1, int(metadata["iterations"]/5)))
ax.set_xticks(xticks)
ax.set_xticklabels([fr"${t}$" for t in xticks])

plt.savefig(output/"figures"/"expectations-split.jpeg", bbox_inches="tight", dpi=300)

