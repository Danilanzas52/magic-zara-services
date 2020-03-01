import os

from cv2 import cv2
import requests
from skimage import io
import numpy as np
from itertools import cycle
from lxml.html import fromstring


def get_proxies():
    url = 'https://free-proxy-list.net/'
    response = requests.get(url)
    parser = fromstring(response.text)
    proxies = set()
    for i in parser.xpath('//tbody/tr')[:300]:
        if i.xpath('.//td[7][contains(text(),"yes")]'):
            proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            proxies.add(proxy)
    return cycle(proxies)


def load_user_agents(ua_file):
    """Read the file of user agents"""
    user_agents = []
    with open(ua_file) as f:
        lines = f.readlines()
        for line in lines:
            user_agents.append(line.replace("\n", ""))

        np.random.shuffle(user_agents)
    return user_agents


def display_images(image_urls, keywords):
    imgs = []
    for i in range(min(4, len(image_urls))):
        os.system("wget " + image_urls[i] + " -O image.png -q")
        image = io.imread("image.png")
        image = cv2.resize(image, (int(image.shape[1] * 0.5), int(image.shape[0] * 0.5)))
        imgs.append(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    image = np.hstack(imgs)
    cv2.putText(image, str(" ".join(keywords)), (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0))
    cv2.imshow("Correct", image)
    cv2.waitKey(50)
