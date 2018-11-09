# -*- coding: utf-8 -*-
import scrapy


class ShopbopCrawlerSpider(scrapy.Spider):
    name = 'shopbop_crawler'
    allowed_domains = ['shopbop.com']
    start_urls = ['https://www.shopbop.com/']

    def parse(self, response):
        categories = response.xpath(
            '//li[@class="top-nav-list-item"]')
        for category in categories:
            category_name = category.xpath(
                './/a/span/text()').extract_first().strip()
            if category_name in ['Clothing', 'Shoes', 'Bags']:
                link = category.xpath('.//a/@href').extract_first()
                yield scrapy.Request(response.urljoin(link), callback=self.parse_category)

    def parse_category(self, response):
        items = response.xpath('//li[@class="hproduct product "]')
        for item in items:
            link = item.xpath('.//a[@class=" photo"]/@href').extract_first()

            yield scrapy.Request(response.urljoin(link), callback=self.parse_item)

        next_page_url = response.xpath(
            '//a[@class="next "]/@data-next-link').extract_first()
        if next_page_url:
            yield scrapy.Request(response.urljoin(next_page_url), callback=self.parse_category)

    def parse_item(self, response):
        brand_name = response.xpath(
            '//span[@class="brand-name"]/text()').extract_first()
        product_title = response.xpath(
            '//div[@id="product-title"]/text()').extract_first()
        details = response.xpath(
            '//ul[@class="bulleted-attributes"]/li/text()').extract()
        details = list(map(lambda x: x.strip(), details))
        id = response.xpath(
            '//div[@class="product-code"]/span/text()').extract_first()
        images = response.xpath(
            '//ul[@id="display-list"]/li/img/@src').extract()
        images = list(map(lambda x: x.strip(), images))
        price = response.xpath(
            '//span[@class="pdp-price"]/text()').extract_first()[3:]

        yield {
            'brand_name': brand_name,
            'product_title': product_title,
            'details': details,
            'id': id,
            'images': images,
            'price': price
        }
