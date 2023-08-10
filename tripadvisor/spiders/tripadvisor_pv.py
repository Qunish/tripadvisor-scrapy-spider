import scrapy
from selenium.webdriver.common.by import By
import random
import pymongo

DRIVER_FILE_PATH = "/Users/qunishdash/Documents/chromedriver_mac64/chromedriver"
USER_AGENT_LIST = ['Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
                    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0',
                    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:72.0) Gecko/20100101 Firefox/72.0',
                    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36',
                    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'
                    ]

class TripadvisorPvSpider(scrapy.Spider):
    name = "tripadvisor_pv"
    handle_httpstatus_list = [403]

    def __init__(self):
        self.conn = pymongo.MongoClient(
            "localhost",
            27017
        )
        db = self.conn["tripadvisor_scrapy_db"]
        self.collection = db["tokyo_lv"]
        self.pvcollection = db["tokyo_pv"]
        self.start_urls = [document['url'] for document in self.collection.find()]
    
    def get_chrome_driver(self, headless_flag):
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        if headless_flag:
            # in case you want headless browser
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--start-maximized")
            # chrome_options.add_experimental_option('prefs', {'headers': headers}) # if you want to add custom header
            chrome_options.add_argument("user-agent={}".format(random.choice(USER_AGENT_LIST)))
            driver = webdriver.Chrome(options=chrome_options) 
        else:
            # in case  you want to open browser
            chrome_options = Options()
            # chrome_options.add_experimental_option('prefs', {'headers': headers}) # if you want to add custom header
            chrome_options.add_argument("--start-maximized")
            chrome_options.add_argument("user-agent={}".format(random.choice(USER_AGENT_LIST)))
            chrome_options.headless = False
            driver = webdriver.Chrome(options=chrome_options)
        return driver
    
    def get_place_data(self, url):
        driver = self.get_chrome_driver(headless_flag=False)
        driver.get(url)

        try:
            try:
                place_overview = driver.find_element(By.CSS_SELECTOR, '#vr-detail-page-overview').text
            except Exception as e:
                place_overview = ''
            try:
                amenities = driver.find_element(By.CSS_SELECTOR, '#vr-detail-page-things-to-know').text
            except Exception as e:
                amenities = ''
            try:
                things_to_know = driver.find_element(By.CSS_SELECTOR, '#vr-detail-page-things-to-know').text
            except Exception as e:
                things_to_know = ''


            data = {
                "place_overview": place_overview,
                "amenities": amenities,
                "things_to_know": things_to_know
            }
            return data
        except Exception as e:
            print("Error while extracting activity data:", e)
            return None
        finally:
            driver.quit()

    def parse(self, response):
        if response.status == 403:
            self.logger.warning("Status 403 - but chill we are handling using selenium driver.")
        url = response.url

        activity_data = self.get_place_data(url)
        if activity_data:
            self.pvcollection.update_one({"url": url}, {"$set": activity_data}, upsert=True)