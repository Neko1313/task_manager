import scrapy
import sqlite3
from scrapy.crawler import CrawlerProcess
from scrapy.http import Request

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
        "LOG_FILE" : "./log/book24_photo.log",
        "LOG_STDOUT" : False
        }
    
    def __init__(self, isbn_list, argument):
        super().__init__()
        self.isbn_list = isbn_list
        self.argument = argument
        self.page_count = 0
        self.cookie_dict = {
            "ssaid": "087e6ec0-f763-11ed-a693-1594a46296a0",
            "_ym_uid": "1684624024509985445",
            "_ym_d": "1684624024"
        }
        
        self.headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
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
                yield Request(
                    url="https://book24.ru" + href,
                    dont_filter=True, 
                    callback=self.parse_book_url, 
                    headers=self.headers, 
                    cookies=self.cookie_dict,
                    cb_kwargs={'isnb': self.page_count}
                )
        else:
            pass
            
        self.page_count += 1
        if self.page_count < len(self.isbn_list):
            yield scrapy.Request(
                url="https://book24.ru/search/?q={}".format(self.isbn_list[self.page_count][1]),
                dont_filter=True, 
                callback=self.parse, 
                headers=self.headers, 
                cookies=self.cookie_dict
            )

    def parse_book_url(self, response, isnb):
        item = {}
        item[self.isbn_list[isnb][1]] = "https:" + response.css("img.product-poster__main-image::attr(src)").get()
        cursor.execute("DELETE FROM task WHERE id=?", (self.isbn_list[isnb][0],))
        conn.commit()
        req.post("http://api_gateway:5000/parse", json=item)
    
    def closed(self, reason):
        if reason == 'finished':
            self.logger.info("Паук завершил работу успешно")
            conn.close()
            self.argument += 1
            
            with open("./photo/queue.json", "r") as file:
                queue = json.load(file)
            
            if len(queue) > self.argument:
                subprocess.Popen(["python", f"./photo/{queue[self.argument]}.py", f"{self.argument}"], shell=False)
            else:
                req.get("http://api_gateway:5000/api/statistics/static_all")
            
        else:
            self.logger.warning("Паук завершил работу с ошибкой: %s", reason)
            conn.close()
            
            # """
            #     Оправить на управляющию ноду сообщение о сбои
            # """

if __name__ == '__main__':
    conn = sqlite3.connect('task/task_isbn_photo.db')
    cursor = conn.cursor()
    query = "SELECT * FROM task"
    cursor.execute(query)
    isbn_list = cursor.fetchall()
    if len(sys.argv) > 1:
        argument = int(sys.argv[1])
        process = CrawlerProcess()
        process.crawl(Book24, isbn_list=isbn_list, argument=argument)
        process.start()
