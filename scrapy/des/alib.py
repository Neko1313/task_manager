import scrapy
import sqlite3
from scrapy.crawler import CrawlerProcess

import requests as req
import sys
import subprocess
import json

class Alib(scrapy.Spider):
    name = "alib_spider"
    allowed_domains = ['www.alib.ru']
    start_urls = ["https://www.alib.ru/"]
    custom_settings = {
        "LOG_LEVEL" : "INFO",
        "LOG_ENABLED" : True,
        "LOG_FILE" : "./log/alib_des.log",
        "LOG_STDOUT" : False
        }
    def __init__(self, isbn_list, argument):
        super().__init__()
        self.isbn_list = isbn_list
        self.argument = argument
        self.page_count = 0
    
    def start_requests(self):
        yield scrapy.Request(
            url='https://www.alib.ru/find3.php4?tfind={}'.format(self.isbn_list[self.page_count][1]),
            callback=self.parse,
            cb_kwargs={'isnb': self.page_count}
        )
    
    def parse(self, response, isnb):
        item = {}
        item[self.isbn_list[isnb][1]] = response.css('h3+ p').get()
        cursor.execute("DELETE FROM task WHERE id=?", (self.isbn_list[isnb][0],))
        conn.commit()
        req.post("http://localhost:5000/api/working_data/photo_des", json=item)
        
        self.page_count += 1
        if self.page_count < len(self.isbn_list):
            yield scrapy.Request(
                url=' https://www.alib.ru/find3.php4?tfind={}'.format(self.isbn_list[self.page_count][1]),
                dont_filter=True, 
                callback=self.parse,
                cb_kwargs={'isnb': self.page_count}
            )
    
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
        process.crawl(Alib, isbn_list=isbn_list, argument=argument)
        process.start()