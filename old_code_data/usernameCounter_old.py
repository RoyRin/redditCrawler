import numpy as np
import os
import glob
import json

for filename in glob.glob("*.json"):
	with open(filename) as f:
		while True:
			line = f.readline()
			if(not line):
				break
			text = json.loads(line)


dict = 