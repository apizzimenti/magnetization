
import numpy as np
import math
import dateutil.relativedelta, time, datetime, json, pathlib, sys, platform
from ateam.structures import Lattice
from ateam.models import InvadedCluster
from ateam import Chain, Tape, _version
import sys

# Construct lattice object.
L = Lattice()
L.fromFile("lattice.json")

T = float(sys.argv[-1])
D = L.dimension

# Set up Model and Chain.
homology=1
rank = math.comb(len(L.corners), homology)
SW = InvadedCluster(L, homology=homology, stop=rank/2)
N = 10000
M = Chain(SW, steps=N)

# Metadata.
start = time.time()

# Create the appropriate directory and write to file.
output = pathlib.Path(f"./output/tape/{start}")
if not output.exists(): output.mkdir()

# Create the recorder.
r = Tape.Recorder()
fp = str(output/"tape.jsonl.gz")
compressed = True
outputs = {
    0: np.array([-1]*len(L.boundary[homology-1])),
    1: np.array([-1]*rank*len(L.boundary[homology])),
    2: np.array([-1]*len(L.boundary[homology]))
}

with r.record(M, fp, outputs, compressed=compressed) as r:
    for (spins, essentials, satisfied) in M.progress():
        r.store((spins, essentials.flatten(), satisfied))

end = time.time()
ttc = end-start

# Write metadata to file.
with open(".metadata.json", "r") as r: metadata = json.load(r)
with open(str(output/"metadata.json"), "w") as w:
    # Versioning?
    metadata["platform"] = platform.platform()
    metadata["pythonversion"] = sys.version
    metadata["packageversion"] = _version

    # Dates and times and stuff.
    dtstart = datetime.datetime.fromtimestamp(start)
    dtend = datetime.datetime.fromtimestamp(end)
    dtttc = dateutil.relativedelta.relativedelta(dtend, dtstart)

    metadata["start"] = datetime.datetime.fromtimestamp(start).strftime("%Y-%m-%d %H:%M:%S")
    metadata["end"] = datetime.datetime.fromtimestamp(end).strftime("%Y-%m-%d %H:%M:%S")
    metadata["ttc"] = "%dY-%dM-%dD %dh:%dm:%ds" % (dtttc.years, dtttc.months, dtttc.days, dtttc.hours, dtttc.minutes, dtttc.seconds)
    metadata["compressed"] = int(compressed)

    # Computational things.
    metadata["iterations"] = N
    metadata["lattice"] = M.model.lattice.corners
    metadata["dimension"] = M.model.lattice.dimension
    metadata["field"] = M.model.lattice.field.order
    metadata["periodicBoundaryConditions"] = int(M.model.lattice.periodicBoundaryConditions)
    metadata["model"] = M.model.name

    if M.model.name == "InvadedCluster": metadata["homology"] = homology
    if M.model.name in {"SwendsenWang", "Glauber"}: metadata["temperature"] = T

    json.dump(metadata, w, indent=2)