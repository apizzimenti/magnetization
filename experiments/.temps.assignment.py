
from pathlib import Path
import json

tape = Path("./output/tape")
temps = ""

for child in tape.iterdir():
	try:
		with open(child/"metadata.json", "r") as f: metadata = json.load(f)
		if metadata["field"] <= 2: continue
		temps += f"{str(child.name)}\n"
	except:
		continue

with open("temps.assignment.txt", "w") as w: w.write(temps)
