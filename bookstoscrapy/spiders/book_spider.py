import scrapy
from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
from scrapy.exceptions import CloseSpider

import requests
import csv
import os

from bookstoscrapy.items import BookItem
from bookstoscrapy import settings
from constants import (DESCRIPTION_XPATH,
                       BOOKS_LIST_XPATH,
                       URL_XPATH,
                       TITLE_XPATH,
                       NEXT_PAGE_XPATH)


class BookSpider(CrawlSpider):

    name = "books"
    allowed_domains = ["books.toscrape.com"]
    base_url = "http://books.toscrape.com/catalogue/{extension}"
    start_urls = ["http://books.toscrape.com/catalogue/page-1.html"]

    def start_requests(self):

        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse_item)

    @staticmethod
    def is_in_csv(string):
        if os.path.isfile(settings.csv_file_path):
            csv_reader = csv.reader(open(settings.csv_file_path, 'r'),
                                    delimiter=',')
            for row in csv_reader:
                if string in row:
                    return True
        else:
            csv_writer = csv.writer(open(settings.csv_file_path, 'w'),
                       lineterminator='\n')
            csv_writer.writerow(["URL", "TITLE", "DESCRIPTION"])
        return False

    def parse_description(self, item_url):
        response = Selector(
            requests.get(item_url)
        )
        return response.xpath(DESCRIPTION_XPATH).extract()[-1].strip()

    def parse_item(self, response):
        ordered_list = response.xpath(BOOKS_LIST_XPATH).getall()
        for li in ordered_list:
            li_selector = Selector(text=li, type="html")
            item_url = li_selector.xpath(URL_XPATH).get()
            item_url = self.base_url.format(extension=item_url)
            if not self.is_in_csv(item_url):
                item = BookItem()
                item['url'] = item_url
                item['title'] = li_selector.xpath(TITLE_XPATH).get()
                item['description'] = self.parse_description(item_url)
                yield item
        next_page = response.xpath(NEXT_PAGE_XPATH).get()
        if next_page:
            yield scrapy.Request(url=self.base_url.format(extension=next_page),
                                 callback=self.parse_item)
