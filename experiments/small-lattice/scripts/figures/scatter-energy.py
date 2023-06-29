
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


def energyScatter(directory):
    """
    Creates a shaded scatterplot of the Hamiltonian of the given lattice over
    time.
    """
    # Read in data; normalize.
    out = Path(directory)/"output"
    energyPath = out/"statistics/energy.csv"
    data = pd.read_csv(str(energyPath))
    normalized = (data-data.min())/(data.max()-data.min())

    plt.rcParams.update({
        "text.usetex": True,
        "font.family": "serif",
        "text.latex.preamble": r"\usepackage{amsfonts}"
    })

    # Color map.
    plasma = plt.get_cmap("plasma")

    # Higher energy is better(?).
    plt.scatter(
        x=normalized.index, y=normalized["energy"], c=plasma(normalized["energy"]),
        s=2
    )

    # Set titles and save.
    plt.ylabel(r"$H(f_t)$ (normalized)")
    plt.xlabel(r"$t$")
    plt.savefig(out/"figures/energy.pdf", bbox_inches="tight")


if __name__ == "__main__":
    import sys
    energyScatter(sys.argv[-1])
