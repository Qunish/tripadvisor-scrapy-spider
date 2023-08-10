import scrapy
from selenium.webdriver.common.by import By
import pymongo
from ..items import TripadvisorItem_LV
import random

DRIVER_FILE_PATH = "/Users/qunishdash/Documents/chromedriver_mac64/chromedriver"
USER_AGENT_LIST = ['Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
                    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0',
                    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:72.0) Gecko/20100101 Firefox/72.0',
                    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36',
                    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'
                    ]

class TripadvisorLvSpider(scrapy.Spider):
    name = "tripadvisor_lv"
    handle_httpstatus_list = [403]
    page_number = 1
    start_urls = ["https://www.tripadvisor.in/VacationRentals-g298184-Reviews-Tokyo_Tokyo_Prefecture_Kanto-Vacation_Rentals.html"]

    def __init__(self):
        self.conn = pymongo.MongoClient(
            "localhost",
            27017
        )
        db = self.conn["tripadvisor_scrapy_db"]
        self.collection = db["tokyo_lv"]

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

    def parse(self, response):
        if response.status == 403:
            self.logger.warning("Status 403 - but chill we are handling using selenium driver.")

        driver = self.get_chrome_driver(headless_flag=False)
        driver.get(response.url)
        
        items = TripadvisorItem_LV()

        # Extract data using Selenium and yield items
        all_cards = driver.find_elements(By.XPATH, "/html/body/div[2]/div[2]/div/div/div[4]/div/div[1]/div/div[2]/div/div/div")

        for card in all_cards:
            try:
                name = card.find_element(By.CSS_SELECTOR, ".S7").text
            except Exception as e:
                name = ''
            try:
                type_of_property = card.find_element(By.CSS_SELECTOR, ".oXJmt").text
            except Exception as e:
                type_of_property = ''
            try:
                number_of_bedrooms = card.find_element(By.CSS_SELECTOR, ".kkHNg .qkjPI").text
            except Exception as e:
                number_of_bedrooms = ''
            try:
                number_of_bathrooms = card.find_element(By.CSS_SELECTOR, ".WIPQs .qkjPI").text
            except Exception as e:
                number_of_bathrooms = ''
            try:
                number_of_guests_allowed = card.find_element(By.CSS_SELECTOR, ".CnwBZ .qkjPI").text.replace("Sleeps ", "")
            except Exception as e:
                number_of_guests_allowed = ''
            try:
                number_of_reviews = card.find_element(By.CSS_SELECTOR, ".LGVtJ").text
            except Exception as e:
                number_of_reviews = ''
            try:
                url = card.find_element(By.CSS_SELECTOR, ".S7 a").get_attribute("href")
            except Exception as e:
                url = ''
            try:
                image_url = card.find_element(By.CSS_SELECTOR, "._C").get_attribute("src")
            except Exception as e:
                image_url = ''

            items["name"] = name
            items["type_of_property"] = type_of_property
            items["number_of_bedrooms"] = number_of_bedrooms
            items["number_of_bathrooms"] = number_of_bathrooms
            items["number_of_guests_allowed"] = number_of_guests_allowed
            items["number_of_reviews"] = number_of_reviews
            items["url"] = url
            items["image_url"] = image_url

            if any(items.values()):
                self.collection.insert_one(dict(items))

            yield items

        next_page_offset = self.page_number * 50
        # Generate the next page URL
        next_page_url = f'https://www.tripadvisor.in/VRACSearch-g298184-Reviews-Tokyo_Tokyo_Prefecture_Kanto-Vacation_Rentals.html?oa={next_page_offset}'
        if self.page_number < 4:
            self.page_number += 1
            yield scrapy.Request(next_page_url, callback=self.parse)

        driver.quit()