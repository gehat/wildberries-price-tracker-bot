import selenium
from selenium import webdriver
from selenium.common import ElementNotInteractableException
from selenium.webdriver.common.by import By
import pickle
from random import randint
from pay_and_scrapping.wb import Browsr
from async_property import async_property
import asyncio


class Reload_cooks(Browsr):
    def __init__(self):
        self.options = self.options_selenium
        self.__driver = None
        self.__second_driver = None

    async def main_log(self):
        self.__driver = webdriver.Chrome(options=self.options,
                                         executable_path=r"C:\Users\Leonid\PycharmProjects\tele_bot\chromedriver.exe")
        self.__driver.get('https://www.wildberries.ru/security/login?returnUrl=https%3A%2F%2Fwww.wildberries.ru%2F')
        await asyncio.sleep(randint(4, 7))
        telephone = self.__driver.find_element(By.CLASS_NAME, 'input-item')
        telephone.send_keys('')  # telephon number
        await asyncio.sleep(randint(2, 5))
        check = self.__driver.find_elements(By.CLASS_NAME, 'checkbox-with-text__decor')[1]
        check.click()
        await asyncio.sleep(randint(1, 2))
        button = self.__driver.find_element(By.ID, 'requestCode')
        button.click()
        await asyncio.sleep(15)

    @async_property
    async def automatic_update_cookies(self):
        self.__second_driver = webdriver.Chrome(options=self.options)
        self.__second_driver.get('https://www.wildberries.ru/lk/newsfeed/events')
        await asyncio.sleep(3)
        for cookie in pickle.load(open('cookies.pkl', 'rb')):
            self.__second_driver.add_cookie(cookie)
        self.__second_driver.refresh()
        await asyncio.sleep(3)
        code = self.__second_driver.find_element(By.CLASS_NAME, 'additional-info').text
        print(code[19:23])
        self.__second_driver.quit()
        return code[19:23]



    async def logining_function(self):
        await self.main_log()
        number = await self.automatic_update_cookies
        numb = self.__driver.find_element(By.CLASS_NAME, 'j-input-confirm-code')
        numb.send_keys(number)
        await asyncio.sleep(randint(2, 3))
        pickle.dump(self.__driver.get_cookies(), open('cookies.pkl', 'wb'))
        self.__driver.quit()

    async def send_code(self):
        while True:
            await asyncio.sleep(randint(43200, 54000))
            try:
                await self.logining_function()

            except ElementNotInteractableException:
                try:
                    self.__driver.quit()
                finally:
                    pass
                try:
                    self.__second_driver.quit()
                finally:
                    pass
                await asyncio.sleep(randint(60, 600))
                await self.logining_function()

            except selenium.common.exceptions.NoSuchElementException:
                try:
                    self.__driver.quit()
                finally:
                    pass
                try:
                    self.__second_driver.quit()
                finally:
                    pass
                await asyncio.sleep(randint(60, 600))
                await self.logining_function()

