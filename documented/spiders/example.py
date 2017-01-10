# -*- coding: utf-8 -*-
import scrapy


class ExampleSpider(scrapy.Spider):
    """Some text.
    Hi!

    ; Note

    Some note.

    ; Output

    {
        "1": 1
    }
    """

    name = 'example'
    allowed_domains = ('example.com',)
    start_urls = ('http://example.com/',)

    def parse(self, response):
        yield {
            'body_length': len(response.body)
        }


class ExampleSpider2(scrapy.Spider):
    """Some text.
    Hi!

    ; Info

    Some info.
    """

    name = 'example2'
    allowed_domains = ('example.com',)
    start_urls = ('http://example.com/',)

    def parse(self, response):
        yield {'success': True}
