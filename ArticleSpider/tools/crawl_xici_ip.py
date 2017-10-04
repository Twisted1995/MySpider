# _*_ coding: utf-8 _*_
import requests
from scrapy.selector import Selector
import MySQLdb

conn = MySQLdb.connect(host="", user="", passwd="", db="", charset="utf-8")
cursor = conn.cursor()


def crawl_ips():
    # 爬取西刺高匿代理IP
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"}
    for i in range(1568):
        re = requests.get("http://www.xicidaili.com/nn/{0}".format(i), headers=headers)

    selector = Selector(text=re.text)
    all_trs = selector.css("#ip_list tr")

    ip_list = []
    for tr in all_trs:
        speed_str = tr.css(".bar::attr(title)").extract()[0]
        if speed_str:
            speed = float(speed_str.split("秒")[0])
        all_texts = tr.css("td::text").extract()

        ip = all_texts[0]
        port = all_texts[1]
        proxy_type = all_texts[4]

        ip_list.append((ip.port, proxy_type, speed))
    for ip_info in ip_list:
        cursor.execute(
            "insert proxy_ip(ip, port, speed, proxy_type) VALUES('{0}', '{1}', {2}, 'HTTP')".format(
                ip_info[0], ip_info[1], ip_info[3]
            )
        )
        conn.commit()


class GetIP(object):
    def get_random_ip(self):
        # 从数据库中国随机获取一个ip
        random_sql = """
            SELECT ip, port FROM proxy_ip ORDER BY RAND() LIMIT 1
        """
        result = cursor.execute(random_sql)
