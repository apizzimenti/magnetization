
import dateutil.relativedelta, time, datetime, json
from potts import Lattice, SwendsenWang, Chain, constant, Tape

# Construct lattice object.
L = Lattice()
L.fromFile("lattice.json")

# Set up Model and Chain.
SW = SwendsenWang(L, temperatureFunction=constant(-0.441))
N = 1000
M = Chain(SW, steps=N)

# Metadata.
start = time.time()

r = Tape.Recorder()
fp = f"{int(start)}.jsonl.gz"
compressed = True

with r.record(M, fp, compressed=compressed) as r:
    for state in M.progress(): r.store(state)

end = time.time()
ttc = end-start

# Write metadata to file.
with open(".metadata.json", "r") as r: metadata = json.load(r)
with open(f"metadata-{int(start)}.json", "w") as w:
    # Dates and times and stuff.
    dtstart = datetime.datetime.fromtimestamp(start)
    dtend = datetime.datetime.fromtimestamp(end)
    dtttc = dateutil.relativedelta.relativedelta(dtend, dtstart)

    metadata["start"] = datetime.datetime.fromtimestamp(start).strftime("%Y-%m-%d %H:%M:%S")
    metadata["end"] = datetime.datetime.fromtimestamp(end).strftime("%Y-%m-%d %H:%M:%S")
    metadata["ttc"] = "%dY-%dM-%dD %dh:%dm:%ds" % (dtttc.years, dtttc.months, dtttc.days, dtttc.hours, dtttc.minutes, dtttc.seconds)
    metadata["tape"] = fp
    metadata["compressed"] = compressed

    # Computational things.
    metadata["iterations"] = N

    C = list(sum([f.encoding for f in L.faces], ()))[-1]
    metadata["lattice"] = [c+1 for c in C]
    metadata["dimension"] = M.model.lattice.dimension
    metadata["field"] = M.model.lattice.field.order
    metadata["periodicBoundaryConditions"] = int(M.model.lattice.periodicBoundaryConditions)
    metadata["model"] = M.model.name

    # Write to file.
    json.dump(metadata, w, indent=2)