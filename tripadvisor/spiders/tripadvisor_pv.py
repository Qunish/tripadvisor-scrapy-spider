import scrapy


class TripadvisorPvSpider(scrapy.Spider):
    name = "tokyo_pv"
    allowed_domains = ["example.com"]
    start_urls = ["https://example.com"]

    def parse(self, response):
        pass
