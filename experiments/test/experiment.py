
import pandas as pd
from potts import Lattice, SwendsonWang, Chain
from potts.stats import critical
from potts.utils import Metadata

# Set the order of our coefficient field and the size of the lattice.
q = 5
corners = [2, 2]

# Create a 100x100 integer lattice to experiment on.
lattice = Lattice(corners=corners, field=q)
model = SwendsonWang(temperature=critical(q))
initial = model.initial(lattice)

# Create a chain and iterate, stashing information as we go.
chain = Chain(lattice, model, initial=initial, steps=2)

# Step through the chain.
with Metadata(chain) as metadata:
    for step in chain.progress(): pass

# Write statistics to file.
pd.DataFrame.from_dict(chain.statistics).to_csv("./output/statistics/")