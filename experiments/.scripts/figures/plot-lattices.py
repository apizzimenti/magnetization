
import matplotlib.pyplot as plt
import json
from gerrytools.plotting import districtr
from pathlib import Path
from potts import Lattice


def plotLattices(directory):
    """
    Plots the lattices and their assignments over time.
    """
    # Read in metadata and assignments.
    experimentRoot = Path(directory)
    statistics = experimentRoot/"output/statistics"
    output = Path(directory)/"output/figures/lattices/"

    with open(experimentRoot/"metadata.json", "r") as r: metadata = json.load(r)
    with open(statistics/"assignments.json", "r") as r: assignments = json.load(r)

    # Create the lattice.
    lattice = Lattice(metadata["lattice"], field=metadata["field"])

    # Create a color map.
    colors = districtr(lattice.field.order)

    # For each assignment, make a nice lil plot.
    for index, assignment in enumerate(assignments):
        lattice.assign(assignment)
        ax = lattice.plot(
            vertexStyle=dict(marker="o", ms=6, markeredgewidth=0),
            vertexAssignment=[colors[c] for c in assignment],
            edgeStyle=dict(alpha=1/2, lw=1/2)
        )

        # Enable LaTeX.
        plt.rcParams.update({
            "text.usetex": True,
            "font.family": "serif",
            "text.latex.preamble": r"\usepackage{amsfonts}"
        })

        # Create a string for the lattice.
        latticeDesignation = ("times".join([str(c) for c in lattice.corners])).replace("times", "\\times")
        latticeDesignation = "$" + latticeDesignation + "$"
        latticeDesignation += f" sublattice of $\\mathbb{{Z}}^{len(lattice.corners)}$"

        # Create a string for the temperature designation and the step.
        field = f", coefficients in $\\mathbb{{F}}_{lattice.field.order}$"
        step = f"iteration ${index*interval}$ of ${metadata['steps']}$"
        indicator = latticeDesignation + field + "\n" + step

        # Add a little text box in the bottom-left.
        plt.text(0, -1/2, indicator, ha="left", va="top", fontsize=6)

        plt.savefig(output/f"lattice-{index}.png", bbox_inches="tight", dpi=300)
        plt.close()
        plt.clf()



if __name__ == "__main__":
    import sys
    plotLattices(sys.argv[-1])

