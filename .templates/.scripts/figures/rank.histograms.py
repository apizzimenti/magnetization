
import numpy as np
import json
from pathlib import Path
import matplotlib.pyplot as plt

from config import KDE

# Turn on latex.
plt.rcParams.update(**KDE.layered.rcParams)

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
	RANK = METADATA["rank"]
	DIM = METADATA["dimension"]
	L = METADATA["scale"][0]

	# Load betti curve data. Get histogram data for each rank.
	giants = np.load(STATS/STAMP/"percentages.npy")
	histograms = KDE.layered.histograms(giants, RANK)
	X = np.linspace(0, 1, num=2048)
	Ys = KDE.layered.pdfs(histograms, X)

	rev = list(range(RANK))

	# Create a layered plot with all the histograms on top of each other.
	fig, ax = plt.subplots(figsize=KDE.layered.figsize)
	colors = KDE.layered.colors(RANK)
	
	for i in rev:
		Y = Ys[i]
		ax.plot(X, Y, lw=1/2, alpha=1/2, color=colors[i])
		ax.fill_between(X, Y, alpha=1/2, color=colors[i], lw=0)

		# Find the x-coordinate of the max value of Y?
		ax.text(1/2, Y[Y.shape[0]//2], rf"${i+1}$", fontsize=4, alpha=3/4, ha="right", va="top")
	
	ax.set_xlim(*KDE.layered.xlim)
	plt.savefig(OUT/KDE.layered.name(L), **KDE.layered.savefig)


	for i in rev:
		fig, ax = plt.subplots(figsize=KDE.single.figsize)
		ax.plot(X, Ys[i], lw=1/2, alpha=1/2, color=colors[-1])
		ax.fill_between(X, Ys[i], alpha=1/2, color=colors[-1], lw=0)
		# ax.set_xlim(*KDE.single.xlim)

		plt.savefig(OUT/KDE.single.name(i+1,L), **KDE.single.savefig)
		plt.close()
		plt.clf()
