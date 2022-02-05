import glob
import json
import os
import re
import sys

def clean_FE(raw_FE):
    FE=re.sub(r'( cite-)+ ', ' [CITATION] ', ' '+raw_FE+' ')
    FE=re.sub(r'( math-)+ ', ' [MATH] ', ' '+FE+' ')
    FE=re.sub(r'\d+', '[N]', FE.strip())
    return FE  

def main(dir_path, out_path, minimum_frequency=3):
    FEs={} # FEs[discipline][CF][FE]=sum_freq
    for path in glob.glob(dir_path+'*'):
        discipline, section=os.path.basename(path).split('.')
        if discipline not in FEs:
            FEs[discipline]={}
        with open(path, mode='r') as f:
            for l in f:
                CF, FE, frequency=l.split("\t")
                frequency=int(frequency)
                if CF not in FEs[discipline]:
                    FEs[discipline][CF]={}
                FE=clean_FE(FE)
                if FE not in FEs[discipline][CF]:
                    FEs[discipline][CF][FE]=0
                FEs[discipline][CF][FE]+=frequency
        for discipline in FEs:
            for CF in FEs[discipline]:
                FEs[discipline][CF]={k:v for k, v in FEs[discipline][CF].items() if v >= minimum_frequency}
    with open(out_path, mode='w') as f:
        json.dump(FEs, f, ensure_ascii=False, indent="\t")

if __name__=='__main__':
    if len(sys.argv)!=4:
        sys.exit('usage: python preproc.py FE-Database/ out.json min_freq')
    main(sys.argv[1], sys.argv[2], minimum_frequency=int(sys.argv[3]))



