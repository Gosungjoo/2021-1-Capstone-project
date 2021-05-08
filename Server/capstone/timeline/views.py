from django.shortcuts import render
from django.views import View
from googleapiclient.discovery import build
from django.http import JsonResponse, HttpResponse
from datetime import datetime
import json
import re
# Create your views here.


class TimelineView(View):
    def post(self, request):

        api_key = 'AIzaSyC4poxuFWcR4mChE66JBgKDjbGUFjmRas4'
        youtube = build('youtube', 'v3', developerKey=api_key)
        data = json.loads(request.body)
        url = data['comments']
        print(url)
        videoId = url[24:]

        # 오류제어 : 시청기록 사용 케이스
        videoId = url[24:]
        if '&t=' in videoId:
            idx = videoId.index('&t=')
            videoId = videoId[:idx]

        # 영상 길이 확인
        v_length_res = youtube.videos().list(
            id = videoId,
            part='contentDetails',
        ).execute()
        length = v_length_res['items'][0]['contentDetails']['duration']
        length = length.replace('PT','').replace('H',':').replace('M',':').replace('S','')
        print(length)

        results = youtube.commentThreads().list(
            videoId=videoId,
            order='relevance',
            part='snippet',
            textFormat='plainText',
            maxResults=100,
        ).execute()

        comments = []

        # 상위 500개 댓글의 타임라인 가져오기
        cnt = 0
        while results:
            # 댓글 사용자 채널명 + 댓글 + 좋아요(like)
            for item in results['items']:
                comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
                channel_name = item['snippet']['topLevelComment']['snippet']['authorDisplayName']
                like_count = item['snippet']['topLevelComment']['snippet']['likeCount']
                comment_list = [channel_name,comment,like_count]
                # 좋아요 5개 미만 출력 X
                if like_count >= 5:
                    comments.append(comment_list)


            if 'nextPageToken' in results:
                cnt += 1
                if cnt < 5:
                    results = youtube.commentThreads().list(
                        videoId=videoId,
                        order='relevance',
                        part='snippet',
                        textFormat='plainText',
                        maxResults=100,
                    ).execute()
                else:
                    break
            else:
                break

        timeline_dict = {}

        # hh:mm:ss 양식 찾기 (timeline 양식 찾기)
        for c_list in comments:
            comment = c_list[1]
            # 영상길이가 mm:ss 일 때
            if len(length) < 7:
                # 00:00 확인
                state = bool(re.search('[0-9]+:[0-9]+', comment))
                if state:
                    if len(comment) < 7:
                        continue
                    cmd = re.compile('[0-9]+:[0-9]+').findall(comment)
                    if len(cmd) == 1:
                        t_length = datetime.strptime(length, '%M:%S')
                        t_cmd = datetime.strptime(cmd[0], '%M:%S')
                        diff = t_length - t_cmd
                        if diff.days > -1:
                            if cmd[0] not in timeline_dict:
                                timeline_dict[cmd[0]] = []
                            timeline_dict[cmd[0]].append(c_list)
                    '''
                    else:
                        if cmd[0] not in timeline_dict:
                            timeline_dict[cmd[0]] = []
                        timeline_dict[cmd[0]].append(c_list)
                    '''
            # 영상 길이가 hh:mm:ss 일 때
            elif len(length) >= 7:
                # 00:00:00 확인
                state = bool(re.search('[0-9]+:[0-9]+:[0-9]+',comment))
                if state:
                    if len(comment) < 9:
                        continue
                    cmd = re.compile('[0-9]+:[0-9]+:[0-9]+').findall(comment)
                    if len(cmd)==1:
                        t_length = datetime.strptime(length,'%H:%M:%S')
                        t_cmd = datetime.strptime(cmd[0],'%H:%M:%S')
                        diff = t_length - t_cmd
                        if diff.days > -1:
                            if cmd[0] not in timeline_dict:
                                timeline_dict[cmd[0]] = []
                            timeline_dict[cmd[0]].append(c_list)
                    '''
                    else:
                        if cmd[0] not in timeline_dict:
                            timeline_dict[cmd[0]] = []
                        timeline_dict[cmd[0]].append(c_list)
                    '''

                else:
                    # 00:00 확인
                    state = bool(re.search('[0-9]+:[0-9]+',comment))
                    if state:
                        if len(comment) < 7:
                            continue
                        cmd = re.compile('[0-9]+:[0-9]+:[0-9]+').findall(comment)
                        if cmd[0] not in timeline_dict:
                            timeline_dict[cmd[0]] = []
                        timeline_dict[cmd[0]].append(c_list)

        for key in timeline_dict.keys():
            most_like = sorted(timeline_dict[key],key=lambda x:x[-1],reverse=True)
            timeline_dict[key] = most_like[0]

        timeline_comments = list(timeline_dict.values())
        for x in timeline_comments:
            print(x)
            print('-----------------------------------------')

        return JsonResponse({'datas': '', 'skip':length})