import time
import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import pickle
from random import randint
from async_property import async_property
import asyncio
from selenium.webdriver.support import expected_conditions as ES
from selenium.webdriver.support.wait import WebDriverWait


class Browsr():
    def __init__(self, url: str, usr_id: int = None):
        self.options = self.options_selenium
        self.__driver = None
        self.url = url
        self.__usr_id = usr_id
        self.__name = None
        self.__price = None

    @property
    def options_selenium(self):
        options = webdriver.ChromeOptions()
        options.add_argument("start-min")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("--disable-blink-features=AutomationControlled") # disable WebDriver
        options.add_argument("--blink-settings=imagesEnabled=false")
        options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.5414.75 Safari/537.36')
        return options

    @async_property
    async def get_elements(self):  # Getting data from a page
        self.__driver = webdriver.Chrome(options=self.options,
                                         executable_path=r"C:\Users\Gehat\YandexDisk\Компьютер HOME-PC\PycharmProjects\tele_bot\chromedriver.exe")
        self.__driver.get(self.url)
        await asyncio.sleep(randint(1, 3))
        for cookie in pickle.load(open('cookies.pkl', 'rb')):
            self.__driver.add_cookie(cookie)
        self.__driver.refresh()
        block = WebDriverWait(self.__driver, 10).until(ES.visibility_of_element_located((By.TAG_NAME, 'main')))
        try:
            self.__name = WebDriverWait(block, 10).until(
                ES.visibility_of_element_located((By.CLASS_NAME, 'product-page__grid'))).find_element(By.TAG_NAME,
                                                                                                      'h1').text
        except selenium.common.exceptions.NoSuchElementException:
            pass
        try:
            price_all = WebDriverWait(block, 10).until(
                ES.visibility_of_element_located((By.CLASS_NAME, 'price-block'))).text.split('\n')
            self.__price = int(''.join(map(str, [int(i) for i in price_all[0].strip() if i.isdigit()])))
        finally:
            pickle.dump(self.__driver.get_cookies(), open('cookies.pkl', 'wb'))
            self.__driver.quit()
            return self.__usr_id, self.__name, self.url, self.__price
