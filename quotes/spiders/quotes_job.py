# -*- coding: utf-8 -*-
import scrapy
from quotes.items import QuotesItem
from scrapy.http import Request
from urllib.parse import urljoin


class QuotesJobSpider(scrapy.Spider):
    name = 'quotes_job'
    allowed_domains = ['brainyquote.com']
    start_urls = ['https://www.brainyquote.com']

    def parse(self, response):
        products = response.xpath('//div[contains(@class,"bqLn")]/a/@href').extract()
        for p in products:
            url = urljoin(response.url, p)
            yield scrapy.Request(url, callback=self.parse_product)

    def parse_product(self, response):
        for info in response.xpath('//div[contains(@id, "quotesList")]').extract():
            for t in info:
                hrefs = response.xpath('//div[contains(@class, "qti-listm")]/a/@href').extract()
                #lines = response.xpath("//div[@class='qti-listm']//a/img/@alt").extract().split(',')[0]
                lines = [line.split(",") for line in response.xpath("//div[@class='qti-listm']//a/img/@alt").extract()]
                lines = [line[0] for line in lines]
                for item in zip(hrefs,lines):
                    new_item = QuotesItem()
                    new_item['hrefs'] = item[0]
                    new_item['lines'] = item[1]
                    yield new_item








