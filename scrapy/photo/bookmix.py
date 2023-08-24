import scrapy
import sqlite3
from scrapy.crawler import CrawlerProcess

import sys
import requests as req
import subprocess
import json

class Bookmix(scrapy.Spider):
    name = "bookmix"
    allowed_domains = ['bookmix.ru']
    start_urls = ["https://bookmix.ru/"]
    custom_settings = {
        "LOG_LEVEL" : "INFO",
        "LOG_ENABLED" : True,
        "LOG_FILE" : "./log/bookmix.log",
        "LOG_STDOUT" : False
        }
    
    def __init__(self, isbn_list, argument):
        super().__init__()
        self.isbn_list = isbn_list
        self.argument = argument
        self.page_count = 0
        
    def start_requests(self):
        yield scrapy.Request(
            url="https://bookmix.ru/booksearch/?keyword={}".format(self.isbn_list[self.page_count][1]),
            dont_filter=True, 
            callback=self.parse,
            cb_kwargs={'isnb': self.page_count}
        )
        
    def parse(self, response, isnb):
        book_div = response.css('div.item-book').extract_first()
        if book_div:
            item = {}
            item[self.isbn_list[isnb][1]] = response.css('img::attr(src)').getall()[1]
            cursor.execute("DELETE FROM task WHERE id=?", (self.isbn_list[isnb][0],))
            conn.commit()
            req.post("http://api_gateway:5000/parse", json=item)
            
        else:
            pass
            
        self.page_count += 1
        if self.page_count < len(self.isbn_list):
            yield scrapy.Request(
                url="https://bookmix.ru/booksearch/?keyword={}".format(self.isbn_list[self.page_count][1]),
                dont_filter=True, 
                callback=self.parse,
                cb_kwargs={'isnb': self.page_count}
            )
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
        process.crawl(Bookmix, isbn_list=isbn_list, argument=argument)
        process.start()
