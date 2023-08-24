import scrapy
import sqlite3
from scrapy.crawler import CrawlerProcess

import requests as req
import sys
import subprocess
import json

class Book24(scrapy.Spider):
    name = "book_24"
    allowed_domains = ['book24.ru']
    start_urls = ["https://book24.ru/"]
    
    custom_settings = {
        "LOG_LEVEL" : "INFO",
        "LOG_ENABLED" : True,
        "LOG_FILE" : "./log/book24_des.log",
        "LOG_STDOUT" : False
        }
    
    def __init__(self, isbn_list, argument):
        super().__init__()
        self.argument = argument
        self.isbn_list = isbn_list
        self.page_count = 0
        self.cookie_dict = {
            "BITRIX_SM_book24_visitor_id": "7a8c2f45-90dd-438b-9e9c-22b2083e0d41",
            "BITRIX_SM_location_name": "%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0",
            "BITRIX_SM_location_code": "0c5b2444-70a0-4932-980c-b4dc0d3f02b5",
            "BITRIX_SM_location_country": "RU",
            "BITRIX_SM_location_region_code": "",
            "BITRIX_SM_location_coords": "%5B%2255.75396%22%2C%2237.620393%22%5D",
            "ssaid": "087e6ec0-f763-11ed-a693-1594a46296a0",
            "_ym_uid": "1684624024509985445",
            "_ym_d": "1684624024",
            "tmr_lvid": "37fc0c99d8d7a40f2916e266941022c3",
            "tmr_lvidTS": "1684624024279",
            "_tt_enable_cookie": "1",
            "_ttp": "v0fiQNgXCRXp3Qik70872S7KvE4",
            "flocktory-uuid": "d99d230e-1b68-403f-9158-5a06c1f2339b-2",
            "popmechanic_sbjs_migrations": "popmechanic_1418474375998%3D1%7C%7C%7C1471519752600%3D1%7C%7C%7C1471519752605%3D1",
            "_ym_isad": "1",
            "_gid": "GA1.2.1777046696.1688348076",
            "g4c_x": "1",
            "PHPSESSID": "kJBydjBo267E7q6eCNV20HU7pKNSD2d2",
            "mindboxDeviceUUID": "d728ee12-f421-4d14-84e4-128bde7a92b0",
            "directCrm-session": "%7B%22deviceGuid%22%3A%22d728ee12-f421-4d14-84e4-128bde7a92b0%22%7D",
            "COOKIES_ACCEPTED": "Y",
            "BITRIX_SM_SOUND_LOGIN_PLAYED": "Y",
            "user_id": "6363099",
            "_ga_L57STKDPVC": "GS1.1.1688367209.4.0.1688367209.60.0.0",
            "tmr_detect": "1%7C1688367209383",
            "_ym_visorc": "b",
            "_ga": "GA1.2.362329161.1684624019",
            "_gat_ddl": "1",
            "__tld__": "null"
        }

        self.user_agent_dict = {
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 YaBrowser/23.1.1.1114 Yowser/2.5 Safari/537.36"
        }
        
        self.headers = {
            "authority": "book24.ru",
            "method": "GET",
            "path": "/search/?q=9785444818213",
            "scheme": "https",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "ru,en;q=0.9",
            "cache-control": "max-age=0",
            "if-modified-since": "Monday, 03-Jul-2023 06:53:31 GMT",
            "referer": "https://www.yandex.ru/",
            "sec-ch-ua": "\"Not?A_Brand\";v=\"8\", \"Chromium\";v=\"108\", \"Yandex\";v=\"23\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Linux\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 YaBrowser/23.1.1.1114 Yowser/2.5 Safari/537.36"
        }
        
    def start_requests(self):
        yield scrapy.Request(
            url="https://book24.ru/search/?q={}".format(self.isbn_list[self.page_count][1]),
            dont_filter=True, 
            callback=self.parse, 
            headers=self.headers, 
            cookies=self.cookie_dict
        )
        
    def parse(self, response):
        product_card = response.css('div.product-card__image-holder').extract_first()
        if product_card:
            href = response.css('a.product-card__name::attr(href)').extract_first()
            if href:
                yield scrapy.Request(
                    url="https://book24.ru" + href,
                    dont_filter=True, 
                    callback=self.parse_book_des, 
                    headers=self.headers, 
                    cookies=self.cookie_dict,
                    cb_kwargs={'isnb': self.page_count}
                )
        
        self.page_count += 1
        if self.page_count < len(self.isbn_list):
            yield scrapy.Request(
                url="https://book24.ru/search/?q={}".format(self.isbn_list[self.page_count][1]),
                dont_filter=True, 
                callback=self.parse, 
                headers=self.headers, 
                cookies=self.cookie_dict
                
            )

    def parse_book_des(self, response,isnb):
        item = {}
        item[self.isbn_list[isnb][1]] = "\n".join(response.css("div#product-about p::text").getall())
        cursor.execute("DELETE FROM task WHERE id=?", (self.isbn_list[isnb][0],))
        conn.commit()
        req.post("http://localhost:5000/api/working_data/photo_des", json=item)
        
    def closed(self, reason):
        if reason == 'finished':
            self.logger.info("Паук завершил работу успешно")
            conn.close()
            self.argument += 1
            
            with open("./des/queue.json", "r") as file:
                queue = json.load(file)
            
            if len(queue) > self.argument:
                subprocess.Popen(["python", f"./des/{queue[self.argument]}.py", f"{self.argument}"], shell=False)
            else:
                pass
            
        else:
            self.logger.warning("Паук завершил работу с ошибкой: %s", reason)
            conn.close()
            
            # """
            #     Оправить на управляющию ноду сообщение о сбои
            # """
            
if __name__ == '__main__':
    conn = sqlite3.connect('task/task_isbn_des.db')
    cursor = conn.cursor()
    query = "SELECT * FROM task"
    cursor.execute(query)
    isbn_list = cursor.fetchall()
    if len(sys.argv) > 1:
        argument = int(sys.argv[1])
        process = CrawlerProcess()
        process.crawl(Book24, isbn_list=isbn_list, argument=argument)
        process.start()