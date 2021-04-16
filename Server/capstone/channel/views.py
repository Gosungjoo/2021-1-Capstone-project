
import json
from .models import ChannelList
from django.views import View
from django.http import JsonResponse
import time
import requests
from datetime import datetime
from selenium import webdriver as wd
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


class ChannelListView(View):
    def post(self,request):
        driver = setting_chrome()

        data = json.loads(request.body)
        url = f'https://www.youtube.com/{data["channel"]}'

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




