
from ateam.viz import points, shortestPath
from ateam.structures import Lattice
import matplotlib.pyplot as plt
import numpy as np
import json
from pathlib import Path

# Load data.
output = Path("../../output")
statistics = output/"statistics"
tape = output/"tape"/"1731431805.599992"

with open(tape/"metadata.json", "r") as r: metadata = json.load(r)

spins = np.loadtxt(statistics/"spins.gz").astype(int)
occupied = np.loadtxt(statistics/"occupied.gz").astype(int)
satisfied = np.loadtxt(statistics/"satisfied.gz").astype(int)

# Create Lattice and points.
L = Lattice().fromCorners(metadata["lattice"])
V, (internal, external) = points(L, 1)

def lattice2D(N):
	(shortestEdges, shortestVertices) = shortestPath(L, occupied[N])

	# Set up plot; set options.
	fig, ax = plt.subplots()
	ax.set_aspect("equal")
	ax.set_axis_off()

	# Line styles.
	thicklines = dict(lw=1.5, color="black")
	lines = dict(lw=0.75, color="black", alpha=1/2)

	for j, ((ux, uy), (vx, vy)) in enumerate(internal):
		if occupied[N][j]:
			if shortestEdges[j]: style = thicklines
			else: style = lines
			
			if external[j]:
				for ((ux, uy), (vx, vy)) in external[j]:
					ax.plot([ux, vx], [uy, vy], **style)
			else:
				ax.plot([ux, vx], [uy, vy], **style)

	# Vertex styles.
	vertex = dict(s=4, marker="s", linewidths=0.5, alpha=1)
	
	colors = ["w", "k"]
	vertices = {
		j: dict(**vertex, color=color, edgecolors="k", facecolors=color)
		for j, color in enumerate(colors)
	}

	X, Y = V
	
	for spin, style in vertices.items():
		spun = np.where(spins[N] == spin)[0]
		ax.scatter(X[spun], Y[spun], zorder=10000, **style)

	plt.savefig(output/"figures/lattices"/f"lattice-{N}.jpeg", bbox_inches="tight", dpi=400)
	plt.close()
	plt.clf()


for N in range(metadata["iterations"]):
	try: lattice2D(N)
	except Exception as E:
		continue
	plt.close()
	plt.clf()

