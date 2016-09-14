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
        movie_link = hxs.xpath('//*[@id="content"]/div/div/div/table/tr/td/a/@href').extract()
        # for item in movie_link:
        item = movie_link[0]
        yield Request(item, meta={'keyword': ''}, callback=self.parse_article,
                      cookies=[{'name': 'COOKIE_NAME', 'value': 'VALUE', 'domain': '.douban.com', 'path': '/'}, ])

    # 电影详情页
    def parse_article(self, response):
        hxs = Selector(response)
        movie_name = hxs.xpath('//*[@id="content"]/h1/span[1]/text()').extract()
        comment_link = hxs.xpath('//div[@id="comments-section"]/div/h2/span/a/@href').extract()[0]
        item = DoubanItem()
        item['movie_name'] = movie_name
        item['comment_link'] = comment_link
        yield Request(comment_link, meta={'item': item}, callback=self.parse_item,
                      cookies=[{'name': 'COOKIE_NAME', 'value': 'VALUE', 'domain': '.douban.com', 'path': '/'}, ])

    # 电影评论页
    def parse_item(self, response):
        hxs = Selector(response)
        item = response.meta['item']
        comment_link = item['comment_link']
        comment_content = hxs.xpath('//div[@class="comment-item"]/div[@class="comment"]/p/text()').extract()
        comment_grade = hxs.xpath(
            '//div[@class="comment-item"]/div[@class="comment"]/h3/span/span[contains(@class, "rating")]/@title').extract()
        item['comment_content'] = comment_content
        item['comment_grade'] = comment_grade
        yield item
        # 后页
        next_page = '//div[@id="paginator"]/a[@class="next"]/@href'
        if hxs.xpath(next_page):
            url_nextpage = comment_link + hxs.xpath(next_page).extract()[0]
            item['comment_link'] = url_nextpage
            yield Request(url_nextpage, meta={'item': item}, callback=self.parse_item, cookies=[
                {'name': 'COOKIE_NAME', 'value': 'VALUE', 'domain': '.douban.com', 'path': '/'}, ])
