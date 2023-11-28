
import pandas as pd
import json
import math
import numpy as np
from rustworkx import connected_components as connectedComponents
from potts import GraphPercolation, GraphLattice, Chain
from potts.stats import randomizedToConstant
from potts.utils import Metadata

# Set the order of our coefficient field and the size of the lattice.
q = 2
corners = [32,32]
steps = 1000

# Create an integer lattice to experiment on.
lattice = GraphLattice(corners=corners, field=q)
model = GraphPercolation(
    temperatureFunction=randomizedToConstant(
        -math.log(1/2), steps, distribution=np.random.uniform
    )
)
initial = model.initial(lattice)

# Create a function that finds the largest connected component of the graph and
# reports its vertices and edges.
def largestComponent(lattice, state):
    G = lattice.graph

    # Find the edges that have spin 1, and find the largest connected component.
    include = []
    for edge in G.edges():
        u, v = edge.at
        if edge.spin == 1: include.append((u.index, v.index))

    subgraph = G.edge_subgraph(include)
    components = connectedComponents(subgraph)

    # Report the vertices in the *largest* connected component.
    return list(max(components, key=len))

# Create a chain and iterate, stashing information as we go.
chain = Chain(
    lattice, model, initial=initial, sampleInterval=10,
    steps=steps
)

components = []

# Step through the chain.
with Metadata(chain) as metadata:
    for step in chain.progress():
        components.append(largestComponent(chain.lattice, chain.state))

# Write statistics to file.
pd.DataFrame.from_dict(chain.statistics).to_csv("./output/statistics/energy.csv", index=False)
with open("./output/statistics/components.json", "w") as w: json.dump(components, w)
with open("./output/statistics/assignments.json", "w") as w: json.dump(chain.assignments, w)