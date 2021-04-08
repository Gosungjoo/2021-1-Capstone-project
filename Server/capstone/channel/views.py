from django.shortcuts import render
import json
from .models import ChannelList
from django.views import View
from django.http import HttpResponse, JsonResponse

import requests
from bs4 import BeautifulSoup
from selenium import webdriver as wd
# Create your views here.


class ChannelListView(View):
    def post(self,request):
        ChannelList.objects.all().delete()

        options = wd.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('lang=ko_KR')
        options.add_argument('disable-gpu')
        options.add_argument(
            "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")

        driver = wd.Chrome(executable_path='C:/Program Files (x86)/Google/Chrome/Application/ch', options=options)

        data = json.loads(request.body)
        url = f'https://www.youtube.com/watch?v={data["channel"]}'
        #req = requests.get(
        #    f'https://www.youtube.com/watch?v={data["channel"]}'
        #)
        driver.implicitly_wait(3)
        driver.get(url)
        print(driver)
        '''
        html = req.text
        #print(html)
        soup = BeautifulSoup(html, 'html.parser')
        post_link = soup.find_all(class_='style-scope ytd-watch-flexy')
        print(post_link)
        for item in post_link:
            ChannelList(
                channelLink=item,
            ).save()
            print(item)
        return HttpResponse(status=200)
        '''
    def get(self, request):
        return JsonResponse({'channel_link':list(ChannelList.objects.values())},status=200)