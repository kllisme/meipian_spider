# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json
from openpyxl import load_workbook, Workbook

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


class PrintXLSXPipeline:

    def open_spider(self, spider):
        self.workbook = Workbook()
        self.worksheet = self.workbook.active
        self.worksheet.append(
            ["caption", "time", "content", "images", "read_cnt", "like_cnt", "jiajing", "share_url"])

    def close_spider(self, spider):
        self.workbook.save('items.xlsx')

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        caption = adapter.get("caption")
        if caption is None:
            caption = "unknown"
        time = adapter.get("time")
        if time is None:
            time = "unknown"
        elif len(time) == 5:
            time = "2021-" + time
        content = adapter.get("content")
        if content is None:
            content = "unknown"
        images = json.dumps(adapter.get("images"))
        read_cnt = adapter.get("read_cnt")
        if read_cnt is None:
            read_cnt = "0"
        like_cnt = adapter.get("like_cnt")
        if like_cnt is None:
            like_cnt = "0"
        jiajing = adapter.get("jiajing")
        if jiajing is None:
            jiajing = False
        share_url = adapter.get("share_url")
        self.worksheet.append([caption, time, content, images, read_cnt, like_cnt, jiajing, share_url])
        return item
