# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup as bs
import logging
from DouTuLa_Scraper.items import GifItem


class DoutulaSpider(scrapy.Spider):
    name = "doutula"
    allowed_domains = ["www.doutula.com"]
    list_url = "https://www.doutula.com/photo/list";
    page_url = "https://www.doutula.com/photo/list/?page="
    last_page = 1
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8",
        "Connection": "keep-alive",
        "Host": "www.doutula.com",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36"
    }

    def parse(self, response):
        pass

    def start_requests(self):
        yield scrapy.Request(
                url = self.list_url,
                headers = self.headers,
                callback = self.parse_pages
                )

    def parse_pages(self, response):

        soup = bs(response.body, 'lxml')
        for li in soup.find('ul', class_='pagination').find_all('li'):
            if li.text.isdigit():
                self.last_page = max(self.last_page, int(li.text))
        logging.info("************************************************")
        logging.info("Last page found: {}".format(self.last_page))
        logging.info("************************************************")

        for page in range(1, self.last_page+1):
            yield scrapy.Request(
                    url = self.page_url + str(page),
                    headers = self.headers,
                    callback = self.parse_one_page
                    )

    def parse_one_page(self, response):
        soup = bs(response.body, 'html.parser')
        logging.info("************************************************")
        logging.info("Page {} scraped!".format(response.url.split('page=')[-1]))
        logging.info("************************************************")
        for a in soup.find('div', class_='page-content').div.find_all('a'):
            yield scrapy.Request(
                    url = a['href'],
                    headers = self.headers,
                    callback = self.parse_gif_page
                    )

    def parse_gif_page(self, response):
        item = GifItem()
        soup = bs(response.body, 'html.parser')

        item['_id'] = response.url.split('/')[-1]
        item['title'] = soup.find('h1').text
        item['url'] = response.url
        item['tags'] = []
        for a in soup.find('div', class_='pic-tips').find_all('a'):
            item['tags'].append(a.text)
        item['file_urls'] = [soup.find('div', class_='swiper-wrapper').find('img')['src']]

        yield item

