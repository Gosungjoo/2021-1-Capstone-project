from django.shortcuts import render
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import urllib.request
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

from django.views import View
from googleapiclient.discovery import build
from django.http import JsonResponse, HttpResponse
from datetime import datetime
import json
# Create your views here.


class KoreanView(View):
    def labelingKorean(self, data):
        # 컬럼 분리
        X_data = data['3']
        X_temp = X_data

        tokenizer = Tokenizer()
        tokenizer.fit_on_texts(X_data)
        sequences = tokenizer.texts_to_sequences(X_data)  # 토크나이징 >> i love lemon => 1 , 2 , 3
        X_data = sequences

        def vectorize_sequences(sequences, dimension=10000):
            # 크기가 (len(sequences), dimension)이고 모든 원소가 0인 행렬을 생성
            results = np.zeros((len(sequences), dimension))
            for i, sequence in enumerate(sequences):
                results[i, sequence] = 1.  # results[i]에서 특정 인덱스의 위치를 1로 지정
            return results

        X_data_vec = vectorize_sequences(X_data)  # 데이터를 벡터로 변환

        from tensorflow.keras.models import load_model  # 모델 소환

        model = load_model('nlp_model.h5')

        prediction = model.predict(X_data_vec)  # 모델 예측값
        prediction = np.round(prediction)  # 반올림

        data['한국인'] = prediction.tolist()  # 합치기

        data = data.values.tolist()
        #print(data)
        return data

    def post(self, request):

        return JsonResponse({'data':'hi'})