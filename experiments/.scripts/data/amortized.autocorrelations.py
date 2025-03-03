
import numpy as np
from pathlib import Path

root = Path("../../")
statistics = root/"output/statistics"
with open(root/"stamps.txt", "r") as f: stamps = [s.strip() for s in f]

autos = np.array([np.loadtxt(statistics/stamp/"autocorrelation.gz") for stamp in stamps])
amortized = np.mean(autos, axis=0)
np.savetxt(statistics/"autocorrelations.amortized.gz", amortized)

