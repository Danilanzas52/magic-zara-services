from bs4 import BeautifulSoup
import os
import numpy as np

ZARA_SPAIN_SITEMAP= "https://www.zara.com/sitemaps/sitemap-es-es.xml.gz"
from categories import find_category

def get_item_urls(sitemap_url):
    """ Retrieves the urls of the articles that zara has in it's web page """
    item_urls=[]
    sitemap_path="../data/"+sitemap_url.split("/")[-1][:-3]
    if not os.path.isfile(sitemap_path):
        os.system("wget " + sitemap_url + " -q -O " + sitemap_path)
        os.system("gunzip " + sitemap_path)
    with open(sitemap_path) as file:
        lines=file.readlines()
        file_str="".join(lines)
        soup = BeautifulSoup(file_str, features="lxml")
        locs=soup.find_all("loc")
        for loc in locs:
            url=str(loc.contents[0])
            # if not any([word in url for word in ["edited","help","z-","sostenibilidad","calcetines","ninos","gorro","kids","underwear"]]):


            if any(word in url for word in["/es/mujer","/es/hombre"]):
                if find_category(url):

                    item_urls.append(loc.contents[0])

    # os.remove(sitemap_url.split("/")[-1][:-3])
    np.random.shuffle(item_urls)
    return item_urls
