
import dateutil.relativedelta, time, datetime, json, pathlib, sys, platform
import numpy as np
from construction import buildcomplex
from ateams.models import Bernoulli
from ateams import Chain, Recorder, _version
from math import comb

# Construct lattice object, model, and chain.
SCALE = int(sys.argv[-3]) if len(sys.argv) > 1 else 10
DIMENSION = int(sys.argv[-2]) if len(sys.argv) > 1 else 2
COMPLEX = buildcomplex(DIMENSION, SCALE, "./../_shared")

RANK = comb(COMPLEX.dimension, COMPLEX.dimension//2)

MODEL = Bernoulli(
	COMPLEX,
	dimension=COMPLEX.dimension//2
)

# N = int(min(-(SCALE-128)**3+1000, 1e5)) if len(sys.argv) > 1 else 1000
N = 1000
M = Chain(MODEL, steps=N)

# Metadata.
start = time.time()

# Create the appropriate directory and write to file.
_ROOT = sys.argv[-1] if len(sys.argv) > 1 else "TEST"
output = pathlib.Path(f"./output/tape/{_ROOT}")
if not output.exists(): output.mkdir()

# Create the recorder.
with Recorder().record(output/"tape.lz", blocksize=50) as rec:
	# The times that the giant cycles appear aren't important (since there's no
	# sense of a filtration), just their number. As such, we have to do a little
	# hack.
	L = np.zeros(shape=1)
	for (occupied, giants) in M.progress():
		L[0] = len(giants)

		# We could even ignore the "occupied" data?
		rec.store((occupied,L))

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
	metadata["rank"] = RANK
	metadata["cells"] = MODEL.cellCount
	metadata["tranches"] = COMPLEX.tranches.tolist()
	
	json.dump(metadata, w, indent=2)