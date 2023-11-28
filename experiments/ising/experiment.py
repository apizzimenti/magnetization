
import pandas as pd
import math
import numpy as np
import json
from potts import GraphLattice, GraphIsing, Chain
from potts.stats import linear, metropolis, randomizedToConstant, constant
from potts.utils import Metadata

# Set the order of our coefficient field and the size of the lattice.
q = 2
corners = [32,32]
steps = 1000

# Create an integer lattice to experiment on.
lattice = GraphLattice(corners=corners, field=q)
model = GraphIsing(
    temperatureFunction=constant(-math.log(math.sqrt(2)/(1+math.sqrt(2))))
    # temperatureFunction=randomizedToConstant(
    #     -math.log(math.sqrt(2)/(1+math.sqrt(2))), steps, hold=3/4, distribution=np.random.uniform
    # )
)
model = GraphIsing()
initial = model.initial(lattice)

# Create a chain and iterate, stashing information as we go.
chain = Chain(
    lattice, model, initial=initial, sampleInterval=5,
    steps=steps, accept=metropolis
)

# Step through the chain.
with Metadata(chain) as metadata:
    for step in chain.progress(): pass

# Write statistics to file.
pd.DataFrame.from_dict(chain.statistics).to_csv("./output/statistics/energy.csv", index=False)
with open("./output/statistics/assignments.json", "w") as w: json.dump(chain.assignments, w)