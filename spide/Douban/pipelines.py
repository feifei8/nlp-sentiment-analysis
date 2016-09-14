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
        self.path = os.getcwd() + '/output'
        if not os.path.isdir(self.path):
            os.mkdir(self.path)

    def process_item(self, item, spider):
        file = self.path + '/' + ''.join(item['movie_name']) + '.txt'
        f = codecs.open(file, mode='a', encoding='utf-8')
        comment_content = item['comment_content']
        comment_grade = item['comment_grade']
        for i in range(len(comment_grade)):
            if comment_grade[i] == '力荐':
                grade = '5'
            elif comment_grade[i] == '推荐':
                grade = '4'
            elif comment_grade[i] == '还行':
                grade = '3'
            elif comment_grade[i] == '较差':
                grade = '2'
            else:
                grade = '1'
            content = ''.join(comment_content[i].split()).replace('\n', ';')
            if content.strip() != '':
                line = grade + '\t' + content + '\n'
                # print line
                f.write(line)
        f.close()
        return item
