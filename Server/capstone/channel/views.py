
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


class ChannelListView(View):
    def post(self,request):
        start_time = datetime.now()
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

        driver.implicitly_wait(3)
        driver.get(url)
        print(driver.current_url)
        channel_infos = []
        imgs = []
        titles = []
        subscribers = []
        try:
            nodata = driver.find_element_by_xpath('//*[@id="message"]').text
            if nodata == '이 채널에는 다른 채널이 표시되지 않습니다.':
                driver.quit()
                end_time = datetime.now()
                print((end_time-start_time).seconds)
                return JsonResponse({'channel_info': 'no', 'img': 'no', 'title': 'no',
                          'subscribers': 'no'})

        except:
            pass


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
            end_time = datetime.now()
            print((end_time - start_time).seconds)
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
