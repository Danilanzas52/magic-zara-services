
import time
from inditex_item_scrapper import InditexScrapper
from sitemap_scrapper import get_item_urls, ZARA_SPAIN_SITEMAP
import numpy as np
from database import MongoDB_Handler

from utils import display_images
RANDOMS=[2,5,7,9,13,17,20]


PULL_AND_BEAR_SITEMAP="https://www.pullandbear.com/2/info/sitemaps/sitemap-products-pb-es-0.xml.gz"
BERSHKA_SITEMAP="https://www.bershka.com/4/info/sitemaps/sitemap-products-bk-es-0.xml.gz"
DISPLAY = False
if __name__ == '__main__':
    zara_scrapper = InditexScrapper(find_proxies=False, use_proxy=False)
    count = 0


    with MongoDB_Handler() as db:
            item_urls = get_item_urls(PULL_AND_BEAR_SITEMAP)
            good_proxies=[]
            while len(item_urls) > 0:
                item_url = item_urls.pop()

                if not any([comunity in item_url for comunity in ["/es/mujer","/es/hombre"]]):
                    print("SKIPPING COMMUNITY")

                    continue



                inserted=db["zara"].find_one({"url":item_url})
                if inserted:
                    print("SKIPPING ALREADY INSERTED")
                    continue


                count += 1
                print(item_url)
                proxy_tries_threshold = 1
                while True:
                    time.sleep(np.random.choice(RANDOMS))
                    if proxy_tries_threshold == 0:
                        count-=1
                        break
                    proxy_tries_threshold -= 1
                    try:

                        url,category, price,price_currency,description, image_urls = zara_scrapper.extract_pull_and_bear(item_url)

                        if category is not None:
                            good_proxies.append(zara_scrapper.get_proxy())
                            print("Inserting {}".format(category))
                            db["zara"].insert_one({
                                "url": url,
                                "category":category,
                                "price":price,
                                "price_currency":price_currency,
                                "description": description,
                                "images": image_urls
                            })
                            break
                        if DISPLAY:
                            display_images(image_urls, description)
                    #Continue in something happends
                    except Exception as ex:
                        print(ex)
