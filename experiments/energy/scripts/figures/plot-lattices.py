
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

    with open(experimentRoot/"metadata.json", "r") as r: metadata = json.load(r)
    with open(statistics/"assignments.json", "r") as r: assignments = json.load(r)

    # Create the lattice.
    lattice = Lattice(metadata["lattice"], field=metadata["field"])

    # Create a color map.
    colors = districtr(lattice.field.order)

    # For each assignment, make a nice lil plot.
    return
    for index, assignment in enumerate(assignments):
        lattice.assign(assignment)
        ax = lattice.plot(
            vertexStyle=dict(marker="o", ms=2, markeredgewidth=0),
            edgeStyle=dict(lw=1, alpha=1/4),
            vertexAssignment=[colors[c] for c in assignment]
        )

        plt.savefig(f"lattice-{index}.pdf", bbox_inches="tight", dpi=300)
        plt.clf()



if __name__ == "__main__":
    import sys
    plotLattices(sys.argv[-1])

