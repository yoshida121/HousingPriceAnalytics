# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class HousingItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    
    name = scrapy.Field()
    age = scrapy.Field()
    rent = scrapy.Field()
    area = scrapy.Field()
    floor = scrapy.Field()
    floor_plan = scrapy.Field()
    address = scrapy.Field()
    building = scrapy.Field()