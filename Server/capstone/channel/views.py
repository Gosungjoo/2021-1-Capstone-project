from django.shortcuts import render
import json
from .models import ChannelList
from django.views import View
from django.http import HttpResponse, JsonResponse
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver as wd
from selenium.webdriver.common.keys import Keys
import chromedriver_autoinstaller

# Create your views here.


class ChannelListView(View):
    def post(self,request):
        driver_path = chromedriver_autoinstaller.install()
        ChannelList.objects.all().delete()

        options = wd.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('lang=ko_KR')
        options.add_argument('disable-gpu')
        options.add_argument('window-size=1920,1080')
        #options.add_argument(
        #    "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")

        driver = wd.Chrome(executable_path=driver_path, options=options)

        data = json.loads(request.body)
        url = f'https://www.youtube.com/{data["channel"]}'
        #req = requests.get(
        #    f'https://www.youtube.com/watch?v={data["channel"]}'
        #)
        driver.implicitly_wait(3)
        driver.get(url)
        print(driver.current_url)
        channel_infos = []
        imgs = []
        titles = []
        subscribers = []
        cnt = 1
        try:

            channel_info = driver.find_elements_by_xpath('//*[@id="channel-info"]')
            for ci in channel_info:
                print(ci.get_attribute('href'))
                channel_infos.append(ci.get_attribute('href'))
                ig = ci.find_element_by_id('img').get_attribute('src')
                print(ig)
                imgs.append(ig)
                tt = ci.find_element_by_id('title').text
                print(tt)
                titles.append(tt)
                sc = ci.find_element_by_id('thumbnail-attribution').text
                print(sc)
                subscribers.append(sc)
                cnt += 1
                if cnt == 20:
                    break
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