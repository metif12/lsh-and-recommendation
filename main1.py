import glob
import re
import random

NUM_OF_PERMUTES = 50

names = glob.glob('files/*')
files = []

for name in names:
    file = open(name)
    files.append(file.read().lower())
    file.close()
    
n_grams= []
file_n_grmas= []

for f in files:
    text = re.sub(r'[^\w\s]', '', f)
    words = list(set(text.split()))
    
    for w in words:
      if w not in n_grams:
        n_grams.append(w)
    
    file_n_grmas.append(words) 
    
matrix = [[] for x in range(len(n_grams))] # each row one n_gram

for i,ng in enumerate(n_grams):
    for fng in file_n_grmas:
        if ng in fng:
            matrix[i].append(1)
        else:
            matrix[i].append(0)
            
signature = []

for y in range(NUM_OF_PERMUTES):
    
    permute = [ p for p in range(len(n_grams))]
    random.shuffle(permute)
    
    signed = []
    for j in range(len(files)):
        for p in permute:
            if matrix[p][j] == 1:
                signed.append(p)
                break
    
    signature.append(signed)
    
from itertools import combinations
combinations = combinations([x for x in range(len(files))],2)
#combinations = []
#for x in range(len(files)):
    #for y in range(x+1, len(files)):
        #combinations.append((x,y))
        
similarities = []

for c in combinations:
    x = c[0]
    y = c[1]
    sum = 0
    for i in range(len(signature)):
        if signature[i][x] == signature[i][y]:
            sum += 1

    sim = 0.0

    if sum != 0:
        sim = float(sum) / NUM_OF_PERMUTES
        
    similarities.append((sim,c))
    
for s in similarities:
    if s[0] >= 0.35:
        print(s)
        
import matplotlib.pyplot as plt
import numpy as np

height = list()
bars = set()

for s in similarities:
    height.append(s[0])
    bars.add(s[1])

x_pos = np.arange(len(bars))

# Create bars and choose color
plt.bar(x_pos, height, color=(0.5, 0.1, 0.5, 0.6))

# Add title and axis names
plt.title('Similarity')
plt.xlabel('Files')
plt.ylabel('Files')

# Create names on the x axis
plt.xticks(x_pos, bars)

# Show graph
plt.show()