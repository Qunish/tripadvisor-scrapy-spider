# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TripadvisorItem_LV(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    type = scrapy.Field()
    type_of_property = scrapy.Field()
    number_of_bedrooms = scrapy.Field()
    number_of_bathrooms = scrapy.Field()
    number_of_guests_allowed = scrapy.Field()
    number_of_reviews = scrapy.Field()
    url = scrapy.Field()
    image_url = scrapy.Field()
    pass
