
import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
from pathlib import Path
import matplotlib.pyplot as plt

ROOT = Path("./../data/")
auto = pd.read_csv(ROOT/"autocorrelation.tables.csv")

statistics = ["energy", "occupancy"]

def plaw(X, a, b): return a*np.power(X,b)

for statistic in statistics:
	X = auto.L
	Y = auto[statistic]

	s = curve_fit(plaw, X, Y)
	print(s)
