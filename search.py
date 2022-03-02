import json
import re

class Search:
    def __init__(self, data_path, config_path, sentences_path):
        with open(data_path) as f:
            self.FEs=json.load(f)
        with open(config_path) as f:
            self.threshold=json.load(f)
        with open(sentences_path) as f:
            self.sentences=json.load(f)
    
    def clean_query(self, q):
        q=q.strip()
        q=re.sub(r'[ 　]{2,}', ' ', q)
        q=re.sub(r'[^ a-zA-Z0-9\-_]', '', q)
        q=q.lower()
        return q

    def calc_similarity(self, fe1, fe2, max_similarity=1.0):
        words={}
        for w in fe1.split(' '):
            if w!='*':
                words[w]=1
        for w in fe2.split(' '):
            if w in words:
                words[w]=2
            else:
                if w!='*':
                    words[w]=1
        intersection=[w for w in words if words[w]==2]
        if len(words)!=0:
            similarity=len(intersection)/len(words)
            if similarity>max_similarity:
                return 0
            return similarity
        return 0

    def make_pairs(self, FEs, discipline):
        pairs=[]
        for FE in FEs:
            if FE in self.sentences[discipline]:
                pairs.append({
                    'FE': FE,
                    'sentences': [{'sentence': s['sentence'], 'uri': s['uri']} for s in self.sentences[discipline][FE]][:5]
                })
        return pairs

    def search(self, discipline, q, topN=10):
        q=self.clean_query(q)
        if q=='':
            return ('', 0.0, [])
        max_CF=(None, 0.0, []) # CF, similarity
        for CF in self.FEs[discipline]:
            if len(self.FEs[discipline][CF])==0:
                continue
            threshold=self.threshold[discipline][CF]
            candidates={}
            max_sim=0.0
            for FE in self.FEs[discipline][CF]:
                candidates[FE]=self.calc_similarity(q, FE)
                if candidates[FE]>max_sim:
                    max_sim=candidates[FE]
            if max_sim>max_CF[1]:
                if max_sim!=1.0:
                    threshold=1.0
                topN_FEs=sorted(candidates, reverse=True, key=lambda x: candidates[x] if candidates[x]<=threshold else 0)[:topN]
                max_CF=(CF, max_sim, self.make_pairs(topN_FEs, discipline))
        return max_CF
        
