import re
import scrapy
import logging
from datetime import datetime

class NewsSpider(scrapy.Spider):


    name = "news"

    def start_requests(self):
        urls = [
            'https://ikon.mn',
            'http://www.mminfo.mn'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        hrefs = response.css('a::attr(href)')
        for href in hrefs:
            next_url = href.get() if 'http' in href.get() else f'{response.url}{href.get()}'
            logging.info('GOING TO URL ' + next_url)
            yield response.follow(next_url, self.parse_page)
    
    def parse_page(self, response):

        # бүх paragraph доторх текстийг авах
        paragraphs = response.xpath('//p//text()').getall()

        # хоосон paragraph -уудыг хасах
        paragraphs = list(filter(lambda p: len(p) != 0, paragraphs))
        
        # paragraph байхгүй үед юу ч хийхгүй байх
        if len(paragraphs) == 0:
            return

        # html tag дотор байгаа paragraph -уудыг log folder -д хийх
        with open(f'./log/{datetime.now()}.txt', 'w+', encoding='utf-8') as f:
            for p in paragraphs:
                f.write(str(p.strip()) + '\n')