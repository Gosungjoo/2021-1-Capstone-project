import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import urllib.request
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.layers import SimpleRNN, Embedding, Dense
from tensorflow.keras.models import Sequential
import os


os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

data = pd.read_csv('traindata.csv',encoding='UTF-8')
print('총 샘플의 수 :',len(data))


del data['Unnamed: 0']
del data['Unnamed: 0.1']
del data['사용자명']


data.info()

print(data.groupby('한국인').size().reset_index(name='count'))

#컬럼 분리
X_data = data['댓글']
Y_data = data['한국인']

tokenizer = Tokenizer()
tokenizer.fit_on_texts(X_data)
sequences = tokenizer.texts_to_sequences(X_data)
X_data = sequences

word_to_index = tokenizer.word_index

threshold = 2
total_cnt = len(word_to_index) # 단어의 수
rare_cnt = 0 # 등장 빈도수가 threshold보다 작은 단어의 개수를 카운트
total_freq = 0 # 훈련 데이터의 전체 단어 빈도수 총 합
rare_freq = 0 # 등장 빈도수가 threshold보다 작은 단어의 등장 빈도수의 총 합


for key, value in tokenizer.word_counts.items():
    total_freq = total_freq + value

    # 단어의 등장 빈도수가 threshold보다 작으면
    if(value < threshold):
        rare_cnt = rare_cnt + 1
        rare_freq = rare_freq + value

print('등장 빈도가 %s번 이하인 희귀 단어의 수: %s'%(threshold - 1, rare_cnt))
print("단어 집합(vocabulary)에서 희귀 단어의 비율:", (rare_cnt / total_cnt)*100)
print("전체 등장 빈도에서 희귀 단어 등장 빈도 비율:", (rare_freq / total_freq)*100)


vocab_size = len(word_to_index) + 1
print('단어 집합의 크기: {}'.format((vocab_size)))


print('댓글의 최대 길이 : %d' % max(len(l) for l in X_data))
print('댓글의 평균 길이 : %f' % (sum(map(len, X_data))/len(X_data)))
plt.hist([len(s) for s in X_data], bins=100)
plt.xlabel('length of samples')
plt.ylabel('number of samples')
plt.show()
max_len = max(len(l) for l in X_data)

#댓글 최대 길이에 맞춰 짧은 댓글들 빈칸 제로패딩

data = pad_sequences(X_data, maxlen = max_len)
print("훈련 데이터의 크기(shape): ", data.shape)

#8:2 비율로 트레이닝 데이터, 테스트 데이터 분리

X_test = data[round(len(X_data)*0.8):]
Y_test = np.array(Y_data[round(len(X_data)*0.8):])
X_train = data[:round(len(X_data)*0.8)]
Y_train = np.array(Y_data[:round(len(X_data)*0.8)])



#test 정확도

model = Sequential()
model.add(Embedding(vocab_size, 32)) # 임베딩 벡터의 차원은 32
model.add(SimpleRNN(32)) # RNN 셀의 hidden_size는 32
model.add(Dense(1, activation='sigmoid'))

model.compile(optimizer='rmsprop', loss='binary_crossentropy', metrics=['acc'])
history = model.fit(X_train, Y_train, epochs=10, batch_size=64, validation_split=0.2)




print("\n 테스트 정확도: %.4f" % (model.evaluate(X_test, Y_test)[1]))


epochs = range(1, len(history.history['acc']) + 1)
plt.plot(epochs, history.history['loss'])
plt.plot(epochs, history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'val'], loc='upper left')
plt.show()

