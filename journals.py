import glob
import json
import os
import sys

journals={}
for path in glob.glob(sys.argv[1]+'*'):
    with open(path) as f:
        j=json.load(f)
        journal=j['journal']
        if journal not in journals:
            journals[journal]=[]
        journals[journal].append(os.path.splitext(os.path.basename(path))[0])
with open(sys.argv[2], mode='w') as f:
    json.dump(journals, f, indent="\t")
