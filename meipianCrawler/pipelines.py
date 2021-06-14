# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json

from itemadapter import ItemAdapter


class MeipiancrawlerPipeline:
    def process_item(self, item, spider):
        return item


class PrintJsonPipeline:

    def open_spider(self, spider):
        self.file = open('items.json', 'w', encoding="utf-8")

        self.file.write("[")
    def close_spider(self, spider):
        self.file.write("]")
        self.file.close()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        line = json.dumps(adapter.asdict(), indent=2, ensure_ascii=False)
        self.file.write(line)
        self.file.write(",")
        return item
