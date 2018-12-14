# -*- coding: utf-8 -*-
import scrapy


class AuthorSpider(scrapy.Spider):
    name = 'Author'
    allowed_domains = ['toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        urls = response.css('div.quote > span > a::attr(href)').extrcat()
        for url in urls:
            url = response.urljoin(url)
            yield scrapy.Request(url=url, callback=self.parse_author_details)

        # follow the next page url
        next_page_url = response.css('li.next > a::attr(href)').extract_first()
        if next_page_url:
            next_page_url = response.urljoin(next_page_url)
            yield scrapy.Request(url=next_page_url, callback=self.parse)

    def parse_author_details(self, response):
        yield {
            'author_name': response.css('h3.author-title::text').extract_first(),
            'author_birth_date': response.css('span.author-born-date::text').extract_first(),
        }
