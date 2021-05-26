import numpy as np
import pandas as pd
from tensorflow.keras.preprocessing.text import Tokenizer
import re
from django.views import View
from django.http import JsonResponse

# Create your views here.


class KoreanView(View):
    def labelingKorean(self, data):
        # 컬럼 분리
        X_data = data['3']
        #print(X_data)
        X_temp = X_data

        tokenizer = Tokenizer()
        tokenizer.fit_on_texts(X_data)
        sequences = tokenizer.texts_to_sequences(X_data)  # 토크나이징 >> i love lemon => 1 , 2 , 3
        X_data = sequences

        def vectorize_sequences(sequences, dimension=10000):
            # 크기가 (len(sequences), dimension)이고 모든 원소가  0인 행렬을 생성
            results = np.zeros((len(sequences), dimension))
            for i, sequence in enumerate(sequences):
                results[i, sequence] = 1.  # results[i]에서 특정 인덱스의 위치를 1로 지정
            return results

        X_data_vec = vectorize_sequences(X_data)  # 데이터를 벡터로 변환

        from tensorflow.keras.models import load_model  # 모델 소환

        model = load_model('nlp_model.h5')

        prediction = model.predict(X_data_vec)  # 모델 예측값
        prediction = np.round(prediction)  # 반올림

        data['kr'] = prediction.tolist()  # 합치기

        data = data.values.tolist()

        return data

    def post(self, request):
        #get_data = json.loads(request.body)
        #data = get_data['comments']
        #sdata = pd.DataFrame(data)
        sdata = pd.read_csv('youtube_crawling.csv',encoding='utf-8')
        #gdata = sdata.values.tolist()
        ml_data = pd.DataFrame()
        re_idx = []
        sdata['kr'] = np.nan

        for i in range(len(sdata)):
            if ([] != re.findall(u'[\u3130-\u318F\uAC00-\uD7A3]+', str(sdata.loc[i][2]))) or \
                    ([] != re.findall(u'[\u3130-\u318F\uAC00-\uD7A3]+', str(sdata.loc[i][4]))):
                sdata.loc[i, 'kr'] = list([1.0])
            else:

                ml_data = ml_data.append(sdata.loc[i], ignore_index=True)
                re_idx.append(i)



        #print(re_idx)
        del ml_data['Unnamed: 0']
        del sdata['Unnamed: 0']

        sdata = sdata.values.tolist()
        #print(sdata)

        if len(ml_data) == 0:
            return JsonResponse({'data': 'kr'})

        end_ml = self.labelingKorean(ml_data)
        for i in range(len(end_ml)):
            #print("{} => {}".format(end_ml[i][3],end_ml[i][-1][0]))
            end_ml[i][-1] = end_ml[i][-1][0]
        cnt = 0
        for i in re_idx:
            del sdata[i]
            sdata.insert(i,end_ml[cnt])
            cnt+=1

        for i in range(len(sdata)):

            print("{} => {}".format(sdata[i][3],sdata[i][-1]))

        return JsonResponse({'data': sdata})