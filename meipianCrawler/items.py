# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import Join, MapCompose, TakeFirst


def trim_space(value: str):
    return value.strip()

def trim_chinese(value: str):
    return value.replace("阅读","").strip()

def exist(value: str):
    return value != ""


class ArticleItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    caption = scrapy.Field(output_processor=TakeFirst())
    time = scrapy.Field(input_processor=MapCompose(trim_space), output_processor=TakeFirst())
    read_cnt = scrapy.Field(input_processor=MapCompose(trim_chinese),output_processor=TakeFirst())
    content = scrapy.Field(output_processor=Join('\n'))
    like_cnt = scrapy.Field(input_processor=MapCompose(trim_space), output_processor=TakeFirst())
    images = scrapy.Field()
    jiajing = scrapy.Field(input_processor=MapCompose(exist), output_processor=TakeFirst())
    share_url = scrapy.Field(output_processor=TakeFirst())
