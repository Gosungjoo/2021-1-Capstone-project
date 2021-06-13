import numpy as np
import pandas as pd
import urllib.request


from nltk.stem import PorterStemmer
from sklearn.externals import joblib


data = pd.read_csv('traindata2.csv',encoding='ANSI')

X_data = data['댓글'].astype(str)
extemp = X_data
Y_data = data['스팸'].astype(int)

def Featurize(dt):
    porter = PorterStemmer()
    word_map = {}

    cnt = 0
    for i in range(len(dt.values)):
        temp = dt.values[i].split(' ')
        
        for j in range(len(temp)):
            temp[j] = porter.stem(temp[j])

            if temp[j] in word_map:
                continue
            else:
                word_map[temp[j]] = cnt
                cnt = cnt + 1

        dt.values[i] = np.array(temp)
    
    return dt, word_map



def Vectorize(dt):
    length = len(dt.values)
    map_length = len(word_map.keys())
    blank = []

    for i in range(len(dt.values)):
        temp = np.zeros(map_length)

        for j in range(len(dt.values[i])):
            idx = word_map.get(dt.values[i][j])
            temp[idx] = 1
        
        blank.append(temp)
    
    return np.array(blank)

X_data, word_map = Featurize(X_data)
X_vec = Vectorize(X_data)

file_name = 'model.pkl' 
model = joblib.load(file_name) 


print(X_data[50:60])
print(model.predict(X_vec[50:60]))
