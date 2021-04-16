#-*-coding:utf-8-*-

import json
from .models import ChannelList
from django.views import View
from django.http import JsonResponse, HttpResponse
import asyncio
from googleapiclient.discovery import build
from concurrent.futures import ThreadPoolExecutor
from googleapiclient.errors import HttpError
import time
import requests
from datetime import datetime
from selenium import webdriver as wd
import threading
import chromedriver_autoinstaller

# Create your views here.


def setting_chrome():
    driver_path = chromedriver_autoinstaller.install()
    ChannelList.objects.all().delete()

    options = wd.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('lang=ko_KR')
    options.add_argument('disable-gpu')
    options.add_argument('window-size=1920,1080')

    # options.add_argument(
    #    "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")

    driver = wd.Chrome(executable_path=driver_path, options=options)
    return driver

'''
def DataSearch(link):

    driver = setting_chrome()
    print("IN DATASEARCH")
    # 127.0.0.1:8000/ch/subscribers

    url = link

    driver.implicitly_wait(3)
    driver.get(url)
    print(driver.current_url)
    driver.execute_script('window.scrollBy(0, 1080);')
    time.sleep(0.5)

    channel_info = driver.find_elements_by_xpath('//*[@id="channel-info"]')

    for ci in channel_info:
        ig = ci.find_element_by_id('img').get_attribute('src')
        if ig is None:
            break
        item_0 = ci.get_attribute('href')
        item_1 = ig
        tt = ci.find_element_by_id('title').text
        item_2 = tt
        sc = ci.find_element_by_id('thumbnail-attribution').text
        item_3 = sc
        ChannelList(
            channel_info=item_0,
            img=item_1,
            title=item_2,
            subscribers=item_3
        ).save()

    driver.quit()
    return


def DoRun(link):
    print("IN DORUN")
    with ThreadPoolExecutor(max_workers=10) as executor:
        for url in link:
            executor.submit(DataSearch, url)
'''


def RankingSubscribes(channelIds):
    api_key = 'AIzaSyC4poxuFWcR4mChE66JBgKDjbGUFjmRas4'
    youtube = build('youtube', 'v3', developerKey=api_key)

    idRank = {}
    for channelId in channelIds:
        try:

            results = youtube.subscriptions().list(
                part='snippet',
                channelId=channelId,
                maxResults=100,

            ).execute()
            for item in results['items']:
                channelID = item['snippet']['resourceId']['channelId']
                if channelID in idRank:
                    idRank[channelID][-1] += 1
                    continue
                title = item['snippet']['title']
                img = item['snippet']['thumbnails']['default']['url']
                idRank[channelID] = [channelID,title,img,0]

        except:
            pass
    print("this is REUSULT")
    final = list(idRank.values())
    print(final)
    return final

class CommentView(View):
    def post(self, request):
        api_key = 'AIzaSyC4poxuFWcR4mChE66JBgKDjbGUFjmRas4'
        youtube = build('youtube', 'v3', developerKey=api_key)
        data = json.loads(request.body)
        url = data['comments']
        videoId = url[24:]

        results = youtube.commentThreads().list(
            videoId=videoId,
            order='relevance',
            part='snippet',
            textFormat='plainText',
            maxResults=10,
        ).execute()
        channelIds = []

        for item in results['items']:
            #comment = item['snippet']['topLevelComment']['snippet']['authorChannelUrl']
            channelId = item['snippet']['topLevelComment']['snippet']['authorChannelId']['value']
            channelIds.append(channelId)
        sendout = RankingSubscribes(channelIds)
        return JsonResponse({'datas': sendout})


class ChannelListView(View):
    def post(self,request):
        api_key = 'AIzaSyC4poxuFWcR4mChE66JBgKDjbGUFjmRas4'
        youtube = build('youtube', 'v3', developerKey=api_key)
        data = json.loads(request.body)
        channelId = data['channelId']
        try:
            results = youtube.subscriptions().list(
                part='snippet',
                channelId=channelId,
                maxResults=100,

            ).execute()
            subscribesData=[]
            for item in results['items']:
                subdata = []
                channelID = item['snippet']['resourceId']['channelId']
                print(channelID)
                title = item['snippet']['title']
                print(title)
                img = item['snippet']['thumbnails']['default']['url']
                print(img)
                print('----------------------------')
                subdata = [channelID,img,title]
                subscribesData.append(subdata)
            return JsonResponse({'subscribesData':subscribesData})
        except:
            return JsonResponse({'subscribesData':''})
    '''
    def post(self,request):
        driver = setting_chrome()

        #127.0.0.1:8000/ch/subscribers

        data = json.loads(request.body)
        url = data['channel']

        driver.implicitly_wait(3)
        driver.get(url)
        print(driver.current_url)
        channel_infos = []
        imgs = []
        titles = []
        subscribers = []
        try:

            driver.execute_script('window.scrollBy(0, 1080);')
            time.sleep(0.5)

            channel_info = driver.find_elements_by_xpath('//*[@id="channel-info"]')

            for ci in channel_info:
                ig = ci.find_element_by_id('img').get_attribute('src')
                if ig is None:
                    break
                channel_infos.append(ci.get_attribute('href'))
                imgs.append(ig)
                tt = ci.find_element_by_id('title').text
                titles.append(tt)
                sc = ci.find_element_by_id('thumbnail-attribution').text
                subscribers.append(sc)
            print(len(channel_infos))
            driver.quit()
            return JsonResponse({'channel_info': channel_infos, 'img': imgs, 'title': titles,
                                 'subscribers': subscribers})
        except:
            driver.quit()
            print("No Subscribes data")
            if len(channel_infos) == 0:
                return JsonResponse({'channel_info': 'no', 'img': 'no', 'title': 'no',
                          'subscribers': 'no'})
            else:
                return JsonResponse({'channel_info': channel_infos, 'img': imgs, 'title': titles,
                                     'subscribers': subscribers})
    '''

'''
class HistoryView(View):
    def post(self,request): # //*[@id="progress"] //*[@id="overlays"]/ytd-thumbnail-overlay-resume-playback-renderer //*[@id="overlays"]/ytd-thumbnail-overlay-resume-playback-renderer
        driver = setting_chrome()
        data = json.loads(request.body)
        url = data["history"]

        if url[:45] == 'https://www.youtube.com/results?search_query=':
            state = 0
        elif url[:32] == 'https://www.youtube.com/watch?v=':
            state = 1
        else:
            return JsonResponse({'fail': 'fail'})
        driver.implicitly_wait(3)
        driver.get(url)
        print(driver.current_url)

        try:

            ss = 5
        except:
            asdf = 5

'''




