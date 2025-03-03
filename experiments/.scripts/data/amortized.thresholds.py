
from ateams.structures import Lattice
from pathlib import Path
import numpy as np
import math
import json


root = Path("../../")
output = root/"output"
with open(root/"stamps.txt", "r") as f: stamps = [s.strip() for s in f]

L = Lattice()
L.fromFile("../../lattice.json")
homology = 2
length = len(L.boundary[homology])
rank = math.comb(len(L.corners), homology)

guesses = []

for stamp in stamps:
	statistics = output/"statistics"/stamp

	with open(statistics/"metadata.json", "r") as r: metadata = json.load(r)
	occupied = np.loadtxt(statistics/"occupied.gz").astype(int)
	satisfied = np.loadtxt(statistics/"satisfied.gz").astype(int)

	assignments = np.array([
		np.array(occupied[:,(t-1)*length:t*length]) for t in range(1, rank+1)
	])

	ratios = []

	for data in assignments:
		# Compute ratios and plot them over time.
		burn = int(metadata["iterations"]/25)
		times = np.arange(1, metadata["iterations"]+1)
		ratios.append(data.sum(axis=1)/satisfied.sum(axis=1))

	guesses.append(np.array(ratios))

guesses = np.array(guesses)
amortized = np.mean(guesses, axis=0)
np.savetxt(output/"statistics"/"amortized.thresholds.gz", amortized)
