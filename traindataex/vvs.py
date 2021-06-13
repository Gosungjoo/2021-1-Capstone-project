import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import urllib.request
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import os


os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

data = pd.read_csv('traindata2.csv',encoding='ANSI')
data = data[5570:5590]

print('총 샘플의 수 :',len(data))


del data['Unnamed: 0']
del data['사용자명']
del data['좋아요']

#컬럼 분리
X_data = data['댓글']
X_temp = X_data

tokenizer = Tokenizer()
tokenizer.fit_on_texts(X_data)
sequences = tokenizer.texts_to_sequences(X_data) #토크나이징 >> i love lemon => 1 , 2 , 3
X_data = sequences

def vectorize_sequences(sequences, dimension=20000):
    # 크기가 (len(sequences), dimension)이고 모든 원소가 0인 행렬을 생성
    results = np.zeros((len(sequences), dimension))
    for i, sequence in enumerate(sequences):
        results[i, sequence] = 1. # results[i]에서 특정 인덱스의 위치를 1로 지정
    return results

X_data_vec = vectorize_sequences(X_data) # 데이터를 벡터로 변환


from tensorflow.keras.models import load_model #모델 소환

model = load_model('spam_model.h5')
model.summary()
'''
prediction = model.predict(X_data_vec) #모델 예측값
prediction = np.round(prediction,2) #반올림

data['스팸'] = prediction.tolist() #합치기
print(data)
'''