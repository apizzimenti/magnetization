
import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
from pathlib import Path
import matplotlib.pyplot as plt

from config import autocorrelation
CONFIG = autocorrelation.exponents

OUT = Path("./../../output/figures/")
ROOT = Path("./../data/")
auto = pd.read_csv(ROOT/"autocorrelation.tables.csv")

statistics = ["energy", "occupancy"]

# "power-law" fit.
def plaw(X, a, b): return a*np.power(X,b)

# Use tex.
plt.rcParams.update(CONFIG.rcParams)

for statistic in statistics:
	X = auto.L
	Y = auto[statistic]

	# Compute fit.
	popt, pcov = curve_fit(plaw, X, Y, maxfev=2000)
	perr = np.sqrt(np.diag(pcov))
	top = plaw(X, *popt)+plaw(X, *perr)
	bottom = plaw(X, *popt)-plaw(X, *perr)

	fig, ax = plt.subplots(figsize=CONFIG.figsize)

	# Scatter data points; plot fit; plot standard deviation.
	ax.plot(X, plaw(X, *popt), **CONFIG.plot)
	ax.fill_between(X, top, bottom, **CONFIG.fill_between)
	ax.scatter(X, Y, **CONFIG.scatter)

	# Re-scale.
	ax = CONFIG.xscale(ax)
	ax = CONFIG.xticks(ax, X)
	
	# Plot.
	plt.savefig(OUT/CONFIG.name(statistic), **CONFIG.savefig)

