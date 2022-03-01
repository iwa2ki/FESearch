import json
import re
import sys

def get_uri(paper_id):
    if 'PMC' in paper_id:
        pmc_id=re.search(r'PMC\d+', paper_id).group()
        URI='https://www.ncbi.nlm.nih.gov/pmc/articles/'+pmc_id+'/'
    else:
        acl_id=re.search(r'[A-Z]\d\d-\d\d\d\d', paper_id).group()
        URI='https://aclanthology.org/'+acl_id+'/'
    return URI


def main(config_path, output):
    with open(config_path) as f:
        config=json.load(f)
    FEs={}
    for discipline in config:
        FEs[discipline]={}
        for src in config[discipline]:
            with open(src) as f:
                source=json.load(f)
            for FE in source:
                if FE not in FEs[discipline]:
                    FEs[discipline][FE]=[]
                for i in source[FE]:
                    FEs[discipline][FE].append({
                        'sentence': i['sentence'],
                        'uri': get_uri(i['paper_id']),
                        'normalised': i['normalised']
                    })
    with open(output, mode='w') as f:
        json.dump(FEs, f, ensure_ascii=False, indent="\t")

if __name__=='__main__':
    main(sys.argv[1], sys.argv[2])