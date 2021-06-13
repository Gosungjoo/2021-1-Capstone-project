import numpy as np
import pandas as pd
import urllib.request
import pickle
from sklearn.externals import joblib


import os

from sklearn.utils import shuffle


os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

data = pd.read_csv('traindata2.csv',encoding='ANSI')
data = data.sample(frac=1).reset_index(drop=True)


del data['Unnamed: 0']
del data['사용자명']

data = data.sample(frac=1).reset_index(drop=True)


data.info()

print(data.groupby('스팸').size().reset_index(name='count'))

#컬럼 분리
X_data = data['댓글'].astype(str)
Y_data = data['스팸'].astype(int)

from nltk.stem import PorterStemmer

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

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score


X_train, X_test, y_train, y_test = train_test_split(X_vec, Y_data, test_size = 0.3, shuffle=False)

calsifer = RandomForestClassifier(n_estimators=100)
calsifer.fit(X_train,y_train)

print("train score : {0}".format(round(calsifer.score(X_train,y_train)*100 ,2)))

scores = cross_val_score(calsifer, X_train, y_train, cv=10, scoring='accuracy')
print(scores)



print("test score : {0}".format(round(calsifer.score(X_test,y_test)*100 ,2)))

file_name = 'model.pkl'
joblib.dump(calsifer, file_name)

prediction = calsifer.predict(X_vec[250:270])

print(prediction)
print(data[250:270])

