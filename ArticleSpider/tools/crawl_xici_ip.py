# _*_ coding: utf-8 _*_
import requests
from scrapy.selector import Selector

def crawl_ips():
    # 爬取西刺高匿代理IP
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"}
    re = requests.get("http://www.xicidaili.com/nn/", headers=headers)

    selector = Selector(text=re.text)
    all_trs = selector.css("#ip_list tr")

    print(re.text)
