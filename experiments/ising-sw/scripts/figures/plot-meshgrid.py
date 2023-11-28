
import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from gerrytools.plotting import districtr, latex
from pathlib import Path
from potts import GraphLattice
from tqdm import tqdm


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
    lattice = GraphLattice(metadata["lattice"], field=metadata["field"])

    # Create colors.
    colors = [
        latex["Amber"], latex["Cadmium Green"], latex["Amethyst"]
    ][:lattice.field.order]
    cmap = ListedColormap(colors)
    
    # For each assignment, make a nice lil plot.
    with tqdm(total=len(assignments)) as bar:
        for index, assignment in enumerate(assignments):
            lattice.assign(assignment)

            # Create the grid.
            r, c = metadata["lattice"] 
            grid = np.zeros([r+1,c+1])
            for v in lattice.graph.nodes(): grid[*v.at] = v.spin

            # Plot stuff.
            fig, ax = plt.subplots()
            ax.imshow(grid, cmap=cmap, vmin=0, vmax=len(colors))
            ax.set_axis_off()

            plt.savefig(
                output/f"lattice-{str(index).zfill(4)}.jpg", bbox_inches="tight", dpi=200
            )
            
            plt.close()
            plt.clf()
            bar.update()



if __name__ == "__main__":
    import sys
    plotLattices(sys.argv[-1])

