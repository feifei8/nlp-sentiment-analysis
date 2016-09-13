# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy import signals
from scrapy.exporters import XmlItemExporter
import json
import codecs
import os
import sys

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)


class DoubanPipeline(object):
    # def __init__(self):
    #     self.files = {}
    #
    # @classmethod
    # def from_crawler(cls, crawler):
    #      pipeline = cls()
    #      crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
    #      crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
    #      return pipeline
    #
    # def spider_opened(self, spider):
    #     file = open('%s_products.xml' % spider.name, 'w+b')
    #     self.files[spider] = file
    #     self.exporter = XmlItemExporter(file)
    #     self.exporter.start_exporting()
    #
    # def spider_closed(self, spider):
    #     self.exporter.finish_exporting()
    #     file = self.files.pop(spider)
    #     file.close()
    #
    # def process_item(self, item, spider):
    #     self.exporter.export_item(item)
    #     return item
    def __init__(self):
        # self.file = codecs.open('data.dat',mode='wb',encoding='utf-8')
        path = os.getcwd() + 'output.txt'
        self.file = codecs.open(path, mode='wb', encoding='utf-8')

    def process_item(self, item, spider):
        comment_content = item['comment_content']
        comment_grade = item['comment_grade']
        for i in range(len(comment_grade)):
            line = comment_grade[i] + ' ' + ''.join(comment_content[i].split()).replace('\n', ';') + '\n'
            # print line
            self.file.write(line)
        return item
