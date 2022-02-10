from dis import dis
import json
import re
import sys

class Search:
    def __init__(self, data_path, config_path):
        with open(data_path) as f:
            self.FEs=json.load(f)
        with open(config_path) as f:
            self.threshold=json.load(f)
    
    def clean_query(self, q):
        q=q.strip()
        q=re.sub(r'[ 　]{2,}', ' ', q)
        q=q.lower()
        return q

    def calc_similarity(self, fe1, fe2, max_similarity=1.0):
        words={}
        for w in fe1.split(' '):
            words[w]=1
        for w in fe2.split(' '):
            if w in words:
                words[w]=2
            else:
                words[w]=1
        intersection=[w for w in words if words[w]==2]
        if len(words)!=0:
            similarity=len(intersection)/len(words)
            if similarity>max_similarity:
                return 0
            return similarity
        return 0

    def search(self, discipline, q, topN=10):
        q=self.clean_query(q)
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
                topN_FEs=sorted(candidates, reverse=True, key=lambda x: candidates[x] if candidates[x]<=threshold else 0)[:topN]
                max_CF=(CF, max_sim, topN_FEs)
        return max_CF
        
