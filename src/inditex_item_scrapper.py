"""Module containing zara scrapper"""
from itertools import cycle
from time import sleep

from bs4 import BeautifulSoup
import requests
from categories import find_category
import utils
from selenium import webdriver
import numpy as np

class InditexScrapper:
    def __init__(self, ua_file="../data/user_agents.txt", find_proxies=False, use_proxy=True):
        self.ua_index = 0
        self.user_agents = utils.load_user_agents(ua_file)
        self.good_proxies = set()
        self.proxies = None
        self.use_proxy = use_proxy
        # Proxies that already worked for zara scrapping
        self.read_proxies()
        if find_proxies:
            self.proxies = utils.get_proxies()
        self.proxy = None

        self.driver = webdriver.Chrome("/home/smooth/.programs/drivers/chromedriver")

    def write_proxies(self, file_name="../data/good_proxies.txt"):
        """ Writes the good_proxies in the file 'file_name'  """
        with open(file_name, 'w') as file:
            for proxy in self.good_proxies:
                file.write('%s\n' % proxy)

    def read_proxies(self, file_name="../data/good_proxies.txt"):
        """ Reads the proxies in the file 'file_name'  """
        proxies = []
        with open(file_name, 'r') as file:
            lines = file.readlines()
            for line in lines:
                proxies.append(line.replace("\n", ""))
        self.proxies = cycle(proxies)

    def __add_good_proxy(self):
        """ Adds good_proxy and rewrites file with new good_proxies"""
        self.good_proxies.add(self.proxy)
        if len(self.good_proxies) > 20:
            self.write_proxies()

    def __get_zara_imgs(self, soup):
        image_urls = []
        images = soup.find('div', {"id": "main-images"})
        if images is not None:
            for img in images:
                image_urls.append("https:" + img.contents[0]["href"])
        return image_urls

    def __get_zara_description(self, soup):
        description = str(soup.find('p', {"class": "description"}))
        description = description[description.index("class=\"description\">") + 20:description.index("<br/>")]
        return description

    def __get_zara_price(self, soup):
        price = soup.text[soup.text.index("\"price\"") + 10:]
        price = price[:price.index("\"")]

        price_currency = soup.text[soup.text.index("\"priceCurrency\"") + 18:]
        price_currency = price_currency[:price_currency.index("\"")]

        return float(price), price_currency

    def extract_bershka(self, url):
        self.driver.get(url)
        sleeps=[5,10,20,15]
        sleep(np.random.choice(sleeps))
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        a = soup.findAll("div", {"class": "bsk-carousel-slides disable-select bsk-carousel-transition"})
        image_urls = []
        for image in a[0]:
            try:
                image_urls.append(image['href'])
            except:
                pass
        price = soup.find("span", {"class": "productPrice"})
        price, price_currency = price.string.split()
        description = str(soup.find("h1", {"class": "product-description-name"}).string)

        category=find_category(description)
        return url, category, float(price.replace(",",".")), "EUR", description, image_urls

    def extract_pull_and_bear(self, url):
        self.driver.get(url)
        sleeps=[5,10,20,15]
        sleep(np.random.choice(sleeps))
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        a = soup.findAll("img", {"class": "image-responsive"})
        image_urls = []
        for image in a:
            try:
                image_urls.append(image['src'])
            except:
                pass
        price, price_currency = soup.find("span", {"class": "number hansolo"}).text.replace("\n","").replace(" ","").split()
        description =str(soup.find("div", {"class": "c-product-info--description-description"}).text).replace("\n"," ")

        category=find_category(description)
        return url, category, float(price.replace(",",".")), "EUR", description, image_urls

    def extract_zara_data(self, url):
        image_urls = None
        description = None
        price = None
        price_currency = None
        category = None
        if not "\"favicon\"" in url:
            user_agent = str(self.user_agents[self.ua_index])
            self.proxy = next(self.proxies)
            try:
                if self.use_proxy:
                    result = requests.get(str(url), allow_redirects=False, headers={
                        "user-agent": user_agent,
                        "referer": "https://www.google.es/"
                    }, proxies={"http": self.proxy, "https": self.proxy}, timeout=3)
                else:
                    result = requests.get(str(url), allow_redirects=False, headers={
                        "user-agent": user_agent,
                        "referer": "https://www.google.es/"
                    })

                self.ua_index = (self.ua_index + 1) % len(self.user_agents)
                if result.status_code == 200:
                    self.__add_good_proxy()
                    soup = BeautifulSoup(result.content, features="html.parser")
                    image_urls = self.__get_zara_imgs(soup)
                    description = self.__get_zara_description(soup)
                    price, price_currency = self.__get_zara_price(soup)
                    category = find_category(description)

            except requests.exceptions.ConnectTimeout as _:
                print("Timeout {}".format(self.proxy))
            except requests.exceptions.ProxyError as _:
                print("Proxy error {}".format(self.proxy))
            except Exception as ex:
                print(ex)
        return url, category, price, price_currency, description, image_urls

    def get_proxy(self):
        return self.proxy

if __name__ == '__main__':
    zara = InditexScrapper(use_proxy=False)

    url, category, price, price_currency, description, image_urls = zara.extract_pull_and_bear(
        "https://www.pullandbear.com/es/mujer/ropa/jeans-mom-b%C3%A1sicos-c1030207046p501830542.html?cS=427")



