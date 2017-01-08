# -*- coding: utf-8 -*-
import scrapy


class ExampleSpider(scrapy.Spider):
    """Some text.
    Hi!

    ; Note

    Some note.

    ; output

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
