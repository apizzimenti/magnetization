
from ateams.arithmetic import autocorrelation
from pathlib import Path

import numpy as np
import json
import matplotlib as mpl
import matplotlib.pyplot as plt

with open("../../temps.assignment.txt", "r") as f: stamps = [t.strip() for t in f]
with open("../../temps.distribution.txt", "r") as f: temps = [float(t.strip()) for t in f]

plt.rcParams["text.usetex"] = True
plt.rc("text.latex", preamble=r"\usepackage{nicefrac}")
fig, ax = plt.subplots(figsize=(3,1))
ax.spines[['right', 'top', "left"]].set_visible(False)
ax.spines['left'].set_position('zero')
ax.spines['bottom'].set_position('zero')

colors = mpl.colormaps["coolwarm"]
norm = mpl.colors.Normalize(0, 1)
# cbar = fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=colors), cax=bar, orientation="vertical")

for stamp in stamps:
	# Load data.
	output = Path("../../output")
	statistics = output/"statistics"/stamp
	tape = output/"tape"/stamp

	with open(tape/"metadata.json", "r") as r: metadata = json.load(r)
	temp = metadata["temperature"]

	autos = np.loadtxt(statistics/"autocorrelation.gz")
	ax.plot(autos, color=colors(1-temp/min(temps)), zorder=10000)


# Plot Glauber dynamics autocorrelation as well.
glauber = Path("../../../4torus-glauber-2/")
with open(glauber/"temps.assignment.txt", "r") as f: stamps = [t.strip() for t in f]

for stamp in stamps:
	# Load data.
	statistics = glauber/"output/statistics"/stamp
	tape = glauber/"output/tape"/stamp

	with open(tape/"metadata.json", "r") as r: metadata = json.load(r)
	temp = metadata["temperature"]

	autos = np.loadtxt(statistics/"autocorrelation.gz")
	ax.plot(autos, color=colors(1-temp/min(temps)), lw=1.5, alpha=1/4)


# Plot invaded-cluster results as well!
invaded = Path("../../../4torus-homological-2/output/statistics/amortized.gz")
autos = np.loadtxt(invaded)
ax.plot(autos, color="k", ls="--", zorder=10001)

for t in range(5, 26, 5):
	ax.set_xlim(0, t)
	ax.set_xticks([])

	ax.set_ylim(-0.15, 1.05)
	ax.set_yticks([])

	figures = Path("../../output/figures")
	plt.savefig(figures/f"sw-glauber-invaded-comparison-{metadata['field']}-{t}.jpeg", dpi=600, bbox_inches="tight", pad_inches=0)

temps = np.array(temps)

fig, bar = plt.subplots(figsize=(6, 1/4))
cbar = fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=colors), cax=bar, orientation="horizontal")
cbar.ax.invert_xaxis()
T = 1-temps/temps.min()
cbar.ax.set_xticks([])
cbar.set_ticklabels([])
plt.savefig(figures/"colorbar-horizontal.jpeg", bbox_inches="tight", dpi=600, pad_inches=0)

fig, bar = plt.subplots(figsize=(1/8,2))
cbar = fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=colors), cax=bar, orientation="vertical")
cbar.ax.invert_xaxis()
T = 1-temps/temps.min()
cbar.ax.set_xticks([])
cbar.set_ticklabels([])
plt.savefig(figures/"colorbar-vertical.jpeg", bbox_inches="tight", dpi=600, pad_inches=0)

