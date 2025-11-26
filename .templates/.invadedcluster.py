
import dateutil.relativedelta, time, datetime, json, pathlib, sys, platform
from construction import buildcomplex
from ateams.models import InvadedCluster
from ateams import Chain, Recorder, _version
from random import choice

# Construct lattice object, model, and chain.
SCALE = int(sys.argv[-2]) if len(sys.argv) > 1 else 16
COMPLEX = buildcomplex(3, SCALE, "./../_shared")

F = 2
FULL = False

MODEL = InvadedCluster(
	COMPLEX,
	dimension=COMPLEX.dimension//2,
	field=F,
	full=FULL,
	stop=lambda: choice([COMPLEX.dimension//2, COMPLEX.dimension//2+1])
)

N = int(min(-(SCALE-128)**3+1000, 1e5)) if len(sys.argv) > 1 else 1000
M = Chain(MODEL, steps=N)

# Metadata.
start = time.time()

# Create the appropriate directory and write to file.
_ROOT = sys.argv[-1] if len(sys.argv) > 1 else "TEST"
output = pathlib.Path(f"./output/tape/{_ROOT}")
if not output.exists(): output.mkdir()

# Create the recorder.
with Recorder().record(output/"tape.lz", blocksize=50) as rec:
	for (spins, occupied, satisfied) in M.progress():
		rec.store((spins, occupied, satisfied))

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
	metadata["field"] = MODEL.field
	metadata["periodic"] = int(COMPLEX.periodic)
	metadata["model"] = MODEL._name
	metadata["full"] = FULL
	
	json.dump(metadata, w, indent=2)