from django.shortcuts import render
from django.views import View
from googleapiclient.discovery import build
from django.http import JsonResponse, HttpResponse
from tensorflow.keras.preprocessing.text import Tokenizer
from datetime import datetime
import pandas as pd
import numpy as np
import json
import re
# Create your views here.

current_video = ''
current_token = ''
current_type = ''
current_korean = 0
current_spam = 0


def labeling(data, ml_model, kind_of):
    # 컬럼 분리
    X_data = data[3]
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(X_data)
    sequences = tokenizer.texts_to_sequences(X_data)  # 토크나이징 >> i love lemon => 1 , 2 , 3
    X_data = sequences

    def vectorize_sequences(sequences, dimension):
        # 크기가 (len(sequences), dimension)이고 모든 원소가  0인 행렬을 생성
        results = np.zeros((len(sequences), dimension))
        for i, sequence in enumerate(sequences):
            results[i, sequence] = 1.  # results[i]에서 특정 인덱스의 위치를 1로 지정
        return results
    if kind_of == 'kr':
        X_data_vec = vectorize_sequences(X_data,10000)  # 데이터를 벡터로 변환 (korean)
    else:
        X_data_vec = vectorize_sequences(X_data, 20000)  # 데이터를 벡터로 변환 (spam)

    from tensorflow.keras.models import load_model  # 모델 소환

    model = load_model(ml_model)
    prediction = model.predict(X_data_vec)  # 모델 예측값
    prediction = np.round(prediction)  # 반올림

    data[kind_of] = prediction.tolist()  # 합치기
    data = data.values.tolist()

    return data


def korean_discrimination(data):
    sdata = pd.DataFrame(data)
    ml_data = pd.DataFrame()
    re_idx = []
    sdata['kr'] = np.nan
    for i in range(len(sdata)):
        if ([] != re.findall(u'[\u3130-\u318F\uAC00-\uD7A3]+', str(sdata.loc[i][1]))) or \
                ([] != re.findall(u'[\u3130-\u318F\uAC00-\uD7A3]+', str(sdata.loc[i][3]))):
            sdata.loc[i, 'kr'] = list([1.0])
        else:
            ml_data = ml_data.append(sdata.loc[i], ignore_index=True)
            re_idx.append(i)

    sdata = sdata.values.tolist()
    # 전처리에서 모두 한국인으로 판별된 경우
    if len(ml_data) == 0:
        for i in range(len(sdata)):
            sdata[i] = sdata[i][:-1]
        return sdata

    # 전처리에서 한국인 판별이 필요한 댓글이 존재하는 경우
    end_ml = labeling(ml_data, 'nlp_model.h5', 'kr')
    cnt = 0
    for i in re_idx:
        del sdata[i]
        sdata.insert(i, end_ml[cnt])
        cnt += 1
    send_data = []
    for i in range(len(sdata)):

        if sdata[i][-1] != [0.0]:
            send_data.append(sdata[i][:-1])

    return send_data


def spam_discrimination(data, multi=0):
    sdata = pd.DataFrame(data)
    ml_data = pd.DataFrame()
    re_idx = []
    sdata['spam'] = np.nan

    for i in range(len(sdata)):
        if [] != re.findall(u'[\u3130-\u318F\uAC00-\uD7A3]+', str(sdata.loc[i][1])):
            sdata.loc[i, 'spam'] = list([1.0])
        else:
            ml_data = ml_data.append(sdata.loc[i], ignore_index=True)
            re_idx.append(i)

    sdata = sdata.values.tolist()

    # 전처리에서 모두 비 스팸 으로 판별된 경우
    if len(ml_data) == 0:
        for i in range(len(sdata)):
            sdata[i] = sdata[i][:-1]
        return sdata

    # 전처리에서 스팸 판별이 필요한 댓글이 존재하는 경우
    end_ml = labeling(ml_data, 'spam_model.h5', 'spam')

    cnt = 0
    for i in re_idx:
        del sdata[i]
        sdata.insert(i, end_ml[cnt])
        cnt += 1

    send_data = []
    for i in range(len(sdata)):
        if sdata[i][-1] != [0.0]:
            send_data.append(sdata[i][:-1])

    return send_data


class SeeDaetView(View):
    def change_upload(self, now_time, update_date, upload_date):
        when_upload = ''
        diff_time = now_time - update_date
        # 1년 이상 차이나는 경우 (xx 년 전)
        if diff_time.days > 365:
            years = diff_time.days // 365
            when_upload = str(years) + '년 전'
        # 1년 미만 (xx 개월 전)
        elif (now_time.month - update_date.month) > 0:
            months = now_time.month - update_date.month
            when_upload = str(months) + '개월 전'
        # 1개월 미만 (xx 일 전)
        elif (now_time.day - update_date.day) > 0:
            days = now_time.day - update_date.day
            when_upload = str(days) + '일 전'
        # 1일 미만 (xx 시간 전)
        elif (now_time.hour - update_date.hour) > 0:
            hours = now_time.hour - update_date.hour
            when_upload = str(hours) + '시간 전'
        # 1시간 미만 (xx 분 전)
        elif (now_time.minute - update_date.minute) > 0:
            minutes = now_time.minute - update_date.minute
            when_upload = str(minutes) + '분 전'
        # 1분 미만 (xx 초 전)
        elif (now_time.second - update_date.second) >= 0:
            seconds = now_time.second - update_date.second
            when_upload = str(seconds) + '분 전'

        # 수정 여부 파악
        if (upload_date - update_date).seconds != 0:
            when_upload = when_upload + '(수정됨)'
        return when_upload

    def get_comments(self,results, now_time):
        global current_token
        comments = []
        # 댓글 사용자 채널명 + 댓글 + 좋아요(like)
        for item in results['items']:
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            channel_name = item['snippet']['topLevelComment']['snippet']['authorDisplayName']
            channel_url = item['snippet']['topLevelComment']['snippet']['authorChannelUrl']
            like_count = item['snippet']['topLevelComment']['snippet']['likeCount']
            thumbnail = item['snippet']['topLevelComment']['snippet']['authorProfileImageUrl']

            # 언제 올렸는지 계산 및 수정 여부 파악
            upload_date = item['snippet']['topLevelComment']['snippet']['publishedAt']
            update_date = item['snippet']['topLevelComment']['snippet']['updatedAt']

            upload_date = datetime.strptime(upload_date.replace('T', ' ').replace('Z', ''), '%Y-%m-%d %H:%M:%S')
            update_date = datetime.strptime(update_date.replace('T', ' ').replace('Z', ''), '%Y-%m-%d %H:%M:%S')

            when_upload = self.change_upload(now_time, upload_date, update_date)

            # 전송을 위해 list 에 저장
            comment_list = [thumbnail, channel_name, channel_url, comment, like_count, when_upload]
            comments.append(comment_list)

        # 다음 요청에 대비해 next page token 저장
        if 'nextPageToken' in results:
            current_token = results['nextPageToken']
        else:
            current_token = 'no'

        return comments

    def post(self, request):
        global current_video, current_token, current_type, current_korean, current_spam
        api_key = 'AIzaSyC4poxuFWcR4mChE66JBgKDjbGUFjmRas4'
        youtube = build('youtube', 'v3', developerKey=api_key)
        data = json.loads(request.body)
        url = data['comments']
        order_type = data['type']

        # 한국인 필터 기능 사용 여부 파악
        korean = int(data['korean'])
        # 스팸 필터 기능 사용 여부 파악
        spam = int(data['spam'])

        now_time = datetime.now()

        # 오류제어 : 시청기록 사용 케이스
        videoId = url[24:]
        if '&t=' in videoId:
            idx = videoId.index('&t=')
            videoId = videoId[:idx]

        # 영상 길이 확인
        v_length_res = youtube.videos().list(
            id=videoId,
            part='contentDetails, statistics,status',
        ).execute()

        # 영유아 영상 댓글 달기 불가 -> 기능 폐지
        if v_length_res['items'][0]['status']['madeForKids']:
            print('유아영상')
            return JsonResponse({'data': 'kids'})

        # 댓글 기능 막은경우
        if 'commentCount' not in v_length_res['items'][0]['statistics'].keys():
            print('댓글 막음')
            return JsonResponse({'data': 'no comment'})

        # 최초 영상에 대한 요청
        if current_video != videoId:
            print("최초요청")
            current_video = videoId
            current_type = order_type
            current_korean = 0
            current_spam = 0
            results = youtube.commentThreads().list(
                videoId=videoId,
                order=order_type,
                part='snippet',
                textFormat='plainText',
                maxResults=100,
            ).execute()
            comments = self.get_comments(results, now_time)
        # 동일 영상에 대한 댓글 추가 100개 요청(korean 및 spam 타입 동일)
        elif current_video == videoId and current_type == order_type and current_token != 'no' and current_korean == \
                korean and current_spam == spam:
            print("이전 필터 동일 + 이어서")
            results = youtube.commentThreads().list(
                videoId=videoId,
                order=order_type,
                part='snippet',
                pageToken=current_token,
                textFormat='plainText',
                maxResults=100,
            ).execute()
            comments = self.get_comments(results, now_time)
        # 인기 <-> 최신 필터 변경
        elif current_video == videoId and current_type != order_type:
            print("인기 최신 변경")
            current_type = order_type
            current_korean = 0
            current_spam = 0
            results = youtube.commentThreads().list(
                videoId=videoId,
                order=order_type,
                part='snippet',
                textFormat='plainText',
                maxResults=100,
            ).execute()
            comments = self.get_comments(results, now_time)
        # 한국인 및 스팸 필터 변경 (인기 / 최신 상태는 동일)
        elif current_video == videoId and (current_korean != korean or current_spam != spam):
            print("스팸 한국인 변경")
            current_korean = korean
            current_spam = spam
            results = youtube.commentThreads().list(
                videoId=videoId,
                order=order_type,
                part='snippet',
                textFormat='plainText',
                maxResults=100,
            ).execute()
            comments = self.get_comments(results, now_time)
        # state 엔 변화가 없지만 더이상 가져올 댓글이 없는 경우
        elif current_video == videoId and current_type == order_type and current_token == 'no' and current_korean == \
                korean and current_spam == spam:
            return JsonResponse({"data": "stop it"})
        # filter 종류
        # 필터 적용 x
        if korean == 0 and spam == 0:
            print("무 필터")
            return JsonResponse({'data': comments})
        # 한국인 필터 적용
        elif korean == 1 and spam == 0:
            print("한국인 필터")
            return JsonResponse({'data': korean_discrimination(comments)})
        # 스팸 필터 적용
        elif korean == 0 and spam == 1:
            print("스팸 필터")
            return JsonResponse({'data': spam_discrimination(comments)})
        # 한국인 + 스팸 필터 적용 (선 한국인 후 스팸)
        elif korean == 1 and spam == 1:
            print("둘 다")
            return JsonResponse({'data': spam_discrimination(korean_discrimination(comments))})
        return JsonResponse({'data': 'error'})
