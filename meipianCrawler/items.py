# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import Join, MapCompose, TakeFirst


def trim_space(value: str):
    return value.strip()


def exist(value: str):
    return value != ""


class ArticleItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    caption = scrapy.Field()
    time = scrapy.Field(input_processor=MapCompose(trim_space))
    read_cnt = scrapy.Field()
    content = scrapy.Field()
    like_cnt = scrapy.Field(input_processor=MapCompose(trim_space))
    images = scrapy.Field()
    jiajing = scrapy.Field(input_processor=MapCompose(exist))
