import argparse
import json
import os
import random
import re
import sys

import tqdm

def convert_sentence(list_sentences, max_words=20): # [{'sentence', 'normalised', 'paper_id'}]
    for dict_sentence in list_sentences:
        sentence=dict_sentence['sentence']
        sentence=sentence.replace('CITE', ' --citation-- ')
        sentence=sentence.lower()
        sentence=re.sub(r'[\n\t]', ' ', sentence)
        sentence=re.sub(r'[^a-z0-9\-_ ]', '', sentence)
        sentence=re.sub(r'\d+', '[N]', sentence)
        sentence=re.sub(r'(--citation-- +)+', '[CITATION]', sentence)
        sentence=re.sub(r'  +', ' ', sentence)
        sentence=re.sub(r'^ +| +$', '', sentence)
        if len(sentence.split(' '))<=max_words:
            dict_sentence['normalised']=sentence
    return None

def search_FE(FE, list_sentences, max_sentences=5):
    sentences=[]
    FE=' '+FE+' '
    FE=FE.replace('*', '.+?')
    for sentence in random.sample(list_sentences, len(list_sentences)):
        if 'normalised' not in sentence:
            continue
        if re.search(FE, ' '+sentence['normalised']+' '):
            sentences.append(sentence)
        if len(sentences)==max_sentences:
            break
    return sentences

def PMC_select_journal(paper_dir, journal_list_path, journal_title): # FEsはFEのlist
    sentences=[]
    with open(journal_list_path) as f:
        journal_list=json.load(f)
    if journal_title in journal_list:
        for paper_path in journal_list[journal_title]:
            with open(os.path.join(paper_dir, paper_path+'.json')) as f:
                paper=json.load(f)
            sentences.extend([{'sentence': sentence, 'paper_id': paper_path} for section in paper['data'] for sentence in paper['data'][section]])
    return sentences

def load_FEs(path, discipline):
    with open(path) as f:
        j=json.load(f)
    FEs=[fe for cf in j[discipline] for fe in j[discipline][cf]]
    return FEs
    
def make_pairs(FEs, sentences, max_sentences=5):
    results={}
    for FE in tqdm.tqdm(FEs):
        result=search_FE(FE, sentences, max_sentences=max_sentences)
        results[FE]=result
    return results

def PMC_main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--paper-dir')
    parser.add_argument('--journal-list')
    parser.add_argument('--title')
    parser.add_argument('--fe')
    parser.add_argument('--discipline')
    parser.add_argument('--output')
    args=parser.parse_args()
    sentences=PMC_select_journal(args.paper_dir, args.journal_list, args.title)
    convert_sentence(sentences)
    FEs=load_FEs(args.fe, args.discipline)
    results=make_pairs(FEs, sentences)
    with open(args.output, mode='w') as f:
        json.dump(results, f, ensure_ascii=False, indent="\t")

def main(N, M=8):
    directory=sys.argv[1]
    disciplines=['CL', 'Chem', 'Onc', 'Psy']
    disciplines=['Onc', 'Psy']
    sections=['introduction', 'methods', 'results', 'discussion']
    for disc in disciplines:
        sentences=[]
        for sec in sections:
            with open(os.path.join(directory, disc+'.'+sec)) as f:
                for n, l in enumerate(f):
                    if n%M!=N:
                        continue
                    sent_id, c, conf, sentence=l.split("\t")
                    if 'PMC' in sent_id:
                        paper_id=re.search(r'PMC\d+', sent_id).group()
                    else:
                        paper_id=sent_id.split('_')[0]
                    sentence=sentence.replace('cite-', 'CITE')
                    sentence=re.sub(r'CITE-p-\d+-\d+-\d+', 'CITE', sentence)
                    sentences.append({
                        'sentence': sentence.strip(),
                        'paper_id': paper_id
                    })
        convert_sentence(sentences)
        FEs=load_FEs(sys.argv[2], disc)
        results=make_pairs(FEs, sentences, 1)
        with open(os.path.join(sys.argv[3], disc+str(N)+'.json'), mode='w') as f:
            json.dump(results, f, ensure_ascii=False, indent="\t")





if __name__=='__main__':
    main(int(sys.argv[4]))
    # PMC_main()


