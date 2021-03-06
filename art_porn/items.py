# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ArtPornItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    link = scrapy.Field()
    category = scrapy.Field()
    cookie = scrapy.Field()


class HotItem(scrapy.Item):
    name = scrapy.Field()
    link = scrapy.Field()
    category = scrapy.Field()
