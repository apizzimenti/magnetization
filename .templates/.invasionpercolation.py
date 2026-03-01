
import dateutil.relativedelta, time, datetime, json, pathlib, sys, platform
from construction import buildcomplex
from ateams.models import InvasionPercolation
from ateams import Chain, Recorder, _version
from math import comb

# Construct lattice object, model, and chain.
SCALE = int(sys.argv[-3]) if len(sys.argv) > 1 else 3
DIMENSION = int(sys.argv[-2]) if len(sys.argv) > 1 else 2
COMPLEX = buildcomplex(DIMENSION, SCALE, "./../_shared")

FULL = True
RANK = comb(COMPLEX.dimension, COMPLEX.dimension//2)

MODEL = InvasionPercolation(
	COMPLEX,
	dimension=COMPLEX.dimension//2,
	full=FULL
)

# N = int(min(-(SCALE-128)**3+1000, 1e5)) if len(sys.argv) > 1 else 1000
N = 10
M = Chain(MODEL, steps=N)

# Metadata.
start = time.time()

# Create the appropriate directory and write to file.
_ROOT = sys.argv[-1] if len(sys.argv) > 1 else "TEST"
output = pathlib.Path(f"./output/tape/{_ROOT}")
if not output.exists(): output.mkdir()

# Create the recorder.
with Recorder().record(output/"tape.lz", blocksize=50) as rec:
	for (occupied, essential, total, pairs) in M.progress():
		rec.store((occupied, essential, total, pairs))

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
	metadata["compressed"] = 1

	# Computational things.
	metadata["iterations"] = N
	metadata["complex"] = COMPLEX._name
	metadata["scale"] = COMPLEX.corners
	metadata["dimension"] = COMPLEX.dimension//2
	metadata["periodic"] = int(COMPLEX.periodic)
	metadata["model"] = MODEL._name
	metadata["full"] = FULL
	metadata["rank"] = RANK
	metadata["cells"] = MODEL.cellCount
	metadata["tranches"] = COMPLEX.tranches.tolist()
	
	json.dump(metadata, w, indent=2)