from django.shortcuts import render
from django.views import View
from googleapiclient.discovery import build
from django.http import JsonResponse, HttpResponse
from datetime import datetime
import json
import re
# Create your views here.

current_video = ''
current_token = ''

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

            replies = []
            # 총 reply 수 (덧글) 수 확인, 만약 덧글이 존재하면 데이터 가져오고 없으면 pass
            total_replies = item['snippet']['totalReplyCount']
            if total_replies > 0:
                rep_res = item['replies']['comments']
                for rep_item in rep_res:
                    rep_comment = rep_item['snippet']['textDisplay']
                    rep_channel_name = rep_item['snippet']['authorDisplayName']
                    rep_channel_url = rep_item['snippet']['authorChannelUrl']
                    rep_like_count = rep_item['snippet']['likeCount']
                    rep_thumbnail = rep_item['snippet']['authorProfileImageUrl']

                    # 언제 올렸는지 계산 및 수정 여부 파악
                    rep_upload_date = item['snippet']['topLevelComment']['snippet']['publishedAt']
                    rep_update_date = item['snippet']['topLevelComment']['snippet']['updatedAt']

                    rep_upload_date = datetime.strptime(rep_upload_date.replace('T', ' ').replace('Z', ''),
                                                        '%Y-%m-%d %H:%M:%S')
                    rep_update_date = datetime.strptime(rep_update_date.replace('T', ' ').replace('Z', ''),
                                                        '%Y-%m-%d %H:%M:%S')

                    rep_when_upload = self.change_upload(now_time, rep_upload_date, rep_update_date)

                    replies.append([rep_comment, rep_channel_name, rep_channel_url, rep_like_count, rep_thumbnail,
                                    rep_when_upload])

            comment_list = [thumbnail, channel_name, channel_url, comment, like_count, when_upload, replies]
            comments.append(comment_list)
        # 다음 요청에 대비해 next page token 저장
        if 'nextPageToken' in results:
            current_token = results['nextPageToken']
        else:
            current_token = 'no'

        return comments

    def post(self, request):
        global current_video, current_token
        api_key = 'AIzaSyC4poxuFWcR4mChE66JBgKDjbGUFjmRas4'
        youtube = build('youtube', 'v3', developerKey=api_key)
        data = json.loads(request.body)
        url = data['comments']

        now_time = datetime.now()

        print(url)
        videoId = url[24:]

        # 오류제어 : 시청기록 사용 케이스
        videoId = url[24:]
        if '&t=' in videoId:
            idx = videoId.index('&t=')
            videoId = videoId[:idx]

        # 최초 영상에 대한 요청
        if current_video != videoId:
            print("New")
            current_video = videoId

            results = youtube.commentThreads().list(
                videoId=videoId,
                order='relevance',
                part='snippet, replies',
                textFormat='plainText',
                maxResults=100,
            ).execute()
            comments = self.get_comments(results, now_time)
        else:
            if current_token != 'no':
                print("old")
                results = youtube.commentThreads().list(
                    videoId=videoId,
                    order='relevance',
                    part='snippet, replies',
                    pageToken=current_token,
                    textFormat='plainText',
                    maxResults=100,
                ).execute()
                comments = self.get_comments(results, now_time)
            else:
                return JsonResponse({'data': 'stop it'})

        print(comments)
        return JsonResponse({'data':comments})
