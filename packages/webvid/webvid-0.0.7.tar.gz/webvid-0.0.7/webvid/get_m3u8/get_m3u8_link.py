from selenium.webdriver import DesiredCapabilities
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import json


class m3u8_link:

    name_and_url = []

    def __init__(self, url):
        self.url = url

    def m3u8url_get(self):  # take the video url and fetch the m3u8 url from it
        caps = DesiredCapabilities.CHROME
        caps['goog:loggingPrefs'] = {'performance': 'ALL'}
        # caps = {"page_load_strategy": "none"}
        options = webdriver.ChromeOptions()
        # options.add_argument("--headless")
        # options.add_argument("--no-startup-window")
        options.add_experimental_option('perfLoggingPrefs', {
            'enableNetwork': True,
            'enablePage': False,
        })

        driver = webdriver.Chrome(desired_capabilities=caps)
        driver.minimize_window()
        driver.get(self.url)
        WebDriverWait(driver, timeout=20)
        # WebDriverWait(driver, timeout=20).until()
        # driver.implicitly_wait(20)
        # time.sleep(20)
        # print(driver.title)
        name = driver.title
        name = name.replace(':', '')
        name = name.replace(' ', '_')
        self.name_and_url.append(name)
        logs = driver.get_log('performance')
        # driver.implicitly_wait(20)

        for row in logs:
            data = row['message']
            json_data = json.loads(data)
            json_data1 = json_data['message']
            json_data2 = json_data1['params']
            if 'request' in json_data2.keys():
                m3u8 = json_data2['request']['url']
                if "/master.m3u8" in m3u8:
                    # print(m3u8)
                    self.name_and_url.append(m3u8)
                    return self.name_and_url
        driver.close()
