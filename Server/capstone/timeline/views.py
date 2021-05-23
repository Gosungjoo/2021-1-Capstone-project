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
            part='contentDetails, statistics,status',
        ).execute()
        length = v_length_res['items'][0]['contentDetails']['duration']

        # 영유아 영상 댓글 달기 불가 -> 기능 폐지
        if v_length_res['items'][0]['status']['madeForKids']:
            print('유아영상')
            return JsonResponse({'one': 'kids', 'multi': 'kids', 'skip': 'kids'})

        # 댓글 기능 막은경우
        if 'commentCount' not in v_length_res['items'][0]['statistics'].keys():
            print('댓글 막음')
            return JsonResponse({'one': 'no comment', 'multi': 'no comment', 'skip': 'no comment'})

        # 댓글 10개 미만
        if int(v_length_res['items'][0]['statistics']['commentCount']) < 10:
            print('댓글 10개 미만')
            return JsonResponse({'one': 'not enough', 'multi': 'not enough', 'skip': 'not enough'})

        length = length.replace('PT','').replace('H',':').replace('M',':').replace('S','')

        if len(length) == 2:
            length = '0:'+ length
        elif len(length) == 1:
            length = '0:0'+length
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
                thumnail = item['snippet']['topLevelComment']['snippet']['authorProfileImageUrl']
                comment_list = [thumnail,channel_name,comment,like_count]
                # 좋아요 5개 미만 출력 X
                if like_count >= 5:
                    comments.append(comment_list)

            if 'nextPageToken' in results:
                cnt += 1
                if cnt < 4:
                    results = youtube.commentThreads().list(
                        videoId=videoId,
                        order='relevance',
                        part='snippet',
                        pageToken=results['nextPageToken'],
                        textFormat='plainText',
                        maxResults=100,
                    ).execute()
                else:
                    break
            else:
                break

        timeline_dict = {}
        multi_timeline = []
        # hh:mm:ss 양식 찾기 (timeline 양식 찾기)
        for c_list in comments:
            comment = c_list[2]
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
                            c_list.append([cmd[0],t_cmd])

                            timeline_dict[cmd[0]].append(c_list)

                    else:
                        multi_timeline.append(c_list)

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
                            c_list.append([cmd[0],t_cmd])

                            timeline_dict[cmd[0]].append(c_list)
                    else:
                        multi_timeline.append(c_list)

                else:
                    # 00:00 확인
                    state = bool(re.search('[0-9]+:[0-9]+',comment))
                    if state:
                        if len(comment) < 7:
                            continue
                        cmd = re.compile('[0-9]+:[0-9]+:[0-9]+').findall(comment)
                        if cmd[0] not in timeline_dict:
                            timeline_dict[cmd[0]] = []
                        c_list.append([cmd[0],t_cmd])

                        timeline_dict[cmd[0]].append(c_list)

        # 타임라인이 안찍힌 영상
        if len(timeline_dict) < 1:
            print('안찍힘')
            return JsonResponse({'one': 'no timeline', 'multi': 'no timeline', 'skip': 'no timeline'})

        # 동일 시간대 타임라인 좋아요 순으로 자르기
        for key in timeline_dict.keys():
            most_like = sorted(timeline_dict[key],key=lambda x:x[-2],reverse=True)
            timeline_dict[key] = most_like[0]

        # timeline_comments
        # [0] : 채널 썸네일
        # [1] : 채널 명
        # [2] : 댓글내용
        # [3] : 좋아요
        # [4] : 타임라인 시간대

        timeline_comments = list(timeline_dict.values())

        # 유사 시간대 타임라인 좋아요 많은 순으로 자르기
        timeline_comments = sorted(timeline_comments, key=lambda x:(x[-1][-1]))
        index = 0
        while index < len(timeline_comments)-1:
            if (timeline_comments[index+1][4][1]-timeline_comments[index][4][1]).seconds <= 2:
                if timeline_comments[index][3] >= timeline_comments[index+1][3]:
                    del timeline_comments[index+1]
                elif timeline_comments[index][3] < timeline_comments[index+1][3]:
                    del timeline_comments[index]
                continue
            index += 1

        # timeline_comments 5번째 인자 (타임라인 시간) 정리
        for x in timeline_comments:
            x[4] = x[4][0]
            print(x)

        # 타임라인 여러개 찍힌 댓글 중 좋아요 많은 댓글 1개만 추출
        if len(multi_timeline) > 0:
            multi_timeline.sort(key=lambda x:[-1], reverse=True)
            multi_timeline = multi_timeline[0]

        return JsonResponse({'one': timeline_comments, 'multi': multi_timeline, 'skip': length})