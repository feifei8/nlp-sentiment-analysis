#!/usr/bin/env python
# encoding: utf-8
"""
@author: zhourunlai
@time: 2016/09/13
"""
from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.selector import Selector
from Douban.items import DoubanItem
import sys

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)


class DoubanSpyder(BaseSpider):
    name = 'douban'
    allowed_domains = ["movie.douban.com"]
    start_urls = []

    # 电影搜索页
    def start_requests(self):
        file_opened = open('input.txt', 'r')
        try:
            url_head = "http://movie.douban.com/subject_search?search_text="
            for line in file_opened:
                self.start_urls.append(url_head + line + "&cat=1002")
            for url in self.start_urls:
                yield Request(url, callback=self.parse, cookies=[
                    {'name': 'COOKIE_NAME', 'value': 'VALUE', 'domain': '.douban.com', 'path': '/'}, ])
        finally:
            file_opened.close()

    # 解析搜索结果
    def parse(self, response):
        hxs = Selector(response)
        # tmp_keyword = hxs.xpath('//div[@class="mb40"]/div/p/a/text()').extract()
        # tmp = str(tmp_keyword[0]).split(' ')
        # keyword = tmp[1]
        movie_link = hxs.xpath('//*[@id="content"]/div/div/div/table/tr/td/a/@href').extract()
        # for item in movie_link:
        item = movie_link[0]
        yield Request(item, meta={'keyword': ''}, callback=self.parse_article,
                      cookies=[{'name': 'COOKIE_NAME', 'value': 'VALUE', 'domain': '.douban.com', 'path': '/'}, ])

    # 电影详情页
    def parse_article(self, response):
        hxs = Selector(response)
        comment_link = hxs.xpath('//div[@id="comments-section"]/div/h2/span/a/@href').extract()[0]
        yield Request(comment_link, meta={'item': comment_link}, callback=self.parse_item,
                      cookies=[{'name': 'COOKIE_NAME', 'value': 'VALUE', 'domain': '.douban.com', 'path': '/'}, ])

    # 电影评论页
    def parse_item(self, response):
        hxs = Selector(response)
        comment_link = response.meta['item']
        comment_content = hxs.xpath('//div[@class="comment-item"]/div[@class="comment"]/p/text()').extract()
        comment_grade = hxs.xpath(
            '//div[@class="comment-item"]/div[@class="comment"]/h3/span/span[contains(@class, "rating")]/@title').extract()
        item = DoubanItem()
        item['comment_content'] = comment_content
        item['comment_grade'] = comment_grade
        yield item
        # 后页
        next_page = '//div[@id="paginator"]/a[@class="next"]/@href'
        if hxs.xpath(next_page):
            url_nextpage = comment_link + hxs.xpath(next_page).extract()[0]
            yield Request(url_nextpage, meta={'item': url_nextpage}, callback=self.parse_item, cookies=[
                {'name': 'COOKIE_NAME', 'value': 'VALUE', 'domain': '.douban.com', 'path': '/'}, ])
