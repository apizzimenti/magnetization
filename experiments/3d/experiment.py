
import pandas as pd
import json
from potts import GraphLattice, GraphSwendsonWang, Chain
from potts.stats import linear
from potts.utils import Metadata

# Set the order of our coefficient field and the size of the lattice.
q = 3
corners = [4,4,4]
steps = 10

# Create an integer lattice to experiment on.
lattice = GraphLattice(corners=corners, field=q)
model = GraphSwendsonWang(temperatureFunction=linear(steps, low=0, high=-3))
initial = model.initial(lattice)

# Create a chain and iterate, stashing information as we go.
chain = Chain(
    lattice, model, initial=initial, sampleInterval=1,
    steps=steps
)

# Step through the chain.
with Metadata(chain) as metadata:
    for step in chain.progress(): pass

# Write statistics to file.
pd.DataFrame.from_dict(chain.statistics).to_csv("./output/statistics/energy.csv", index=False)
with open("./output/statistics/assignments.json", "w") as w: json.dump(chain.assignments, w)