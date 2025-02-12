
import numpy as np
import dateutil.relativedelta, time, datetime, json, pathlib, sys, platform
from ateam.structures import Lattice
from ateam.models import SwendsenWang
from ateam.stats import constant
from ateam import Chain, Tape, _version

# Construct lattice object.
L = Lattice()
L.fromFile("lattice.json")

# Set up Model and Chain.
T = -0.881
D = L.dimension
SW = SwendsenWang(L, temperatureFunction=constant(T))
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
    0: np.array([-1]*len(L.boundary[D-1])),
    1: np.array([-1]*len(L.boundary[D]))
}

with r.record(M, fp, outputs, compressed=compressed) as r:
    for (spins, occupied) in M.progress():
        r.store((spins, occupied))

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

    if M.model.name == "SwendsenWang": metadata["temperature"] = T

    json.dump(metadata, w, indent=2)