import numpy as np
import pandas as pd
import re
from datasketch import MinHash, MinHashLSHForest

def preprocess(text):
    return re.sub(r'[^\w\s]','',text.lower()).split()

def get_forest(docs, perms):
    matrix = []
    
    for d in docs:
        tokens = preprocess(d)
        m = MinHash(num_perm=perms)
        for s in tokens:
            m.update(s.encode('utf8'))
        matrix.append(m)
        
    forest = MinHashLSHForest(num_perm=perms)
    
    for i,m in enumerate(matrix):
        forest.add(i,m)
        
    forest.index()
        
    return forest

def predict(text, docs, perms, num_results, forest):    
    tokens = preprocess(text)
    m = MinHash(num_perm=perms)
    for s in tokens:
        m.update(s.encode('utf8'))
        
    idx_array = np.array(forest.query(m, num_results))
    if len(idx_array) == 0:
        return None # if your query is empty, return none
    
    result = docs[idx_array]
        
    return result

if __name__ == '__main__':
    #Number of Permutations
    permutations = 128

    #Number of Recommendations to return
    num_recommendations = 1
    
    db = pd.read_csv('bts_2021_1.csv', dtype=str)
    docs = db['comment_text'].unique()
    query = 'some one looking like one small childe'
    forest = get_forest(docs, permutations)
    
    result = predict(query, docs, permutations, num_recommendations, forest)
    print(f'query:\n{query}\n')
    print(f'recomendation\n{result}')