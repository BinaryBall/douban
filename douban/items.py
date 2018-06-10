# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 标题
    title = scrapy.Field()
    # 导演
    director = scrapy.Field()
    # 编剧
    writers = scrapy.Field()
    # 主演
    starring = scrapy.Field()
    # 类型
    type = scrapy.Field()
    # 制片地区
    areas = scrapy.Field()
    # 语言
    language = scrapy.Field()
    # 上映日期
    date = scrapy.Field()
    # 片长
    run_time = scrapy.Field()
    # 评分
    score = scrapy.Field()
    # 剧情简介
    summary = scrapy.Field()
    #电影连接
    movie_url = scrapy.Field()
