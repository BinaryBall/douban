# -*- coding: utf-8 -*-
import json
import re

import scrapy
from scrapy import Request, FormRequest

from douban.items import DoubanItem


class MovieSpider(scrapy.Spider):
    name = 'movie'
    # allowed_domains = ['https://movie.douban.com']
    start_urls = 'https://movie.douban.com/j/search_subjects?type=movie&tag=%E7%83%AD%E9%97%A8&sort=recommend&page_limit=20&page_start=20'
    login_url = 'https://accounts.douban.com/login?source=movie'

    def start_requests(self):
        return [FormRequest(url=self.login_url,
                            formdata={'form_email': 'username', 'form_password': 'password'},
                            callback=self.parse)]

    def parse(self, response):
        # 请求电影列表js
        yield Request(url=self.start_urls, callback=self.parse_url)

    def parse_url(self, response):
        # 将返回的数据转换成json
        subjects = json.loads(response.text)
        # 取出电影列表
        subject_list = subjects.get('subjects')
        # 遍历电影列表
        for subject in subject_list:
            # 获取电影详情的url
            detail_url = subject.get('url')
            yield Request(url=detail_url, callback=self.parse_detail)

    def parse_detail(self, response):
        # 导演
        director = response.xpath('//div[@id="info"]//span[@class="attrs"]//a[@rel="v:directedBy"]/text()').extract()[0]
        # 编剧
        writers = response.xpath('//div[@id="info"]//span[@class="attrs"]//a/text()').extract()[1]
        # 主演
        starring = str(response.xpath('//div[@id="info"]//span[@class="attrs"]//a[@rel="v:starring"]/text()').extract())
        # 剧情类型
        type = str(response.xpath('//div[@id="info"]/span[@property="v:genre"]/text()').extract())
        # 上映时间
        date = str(response.xpath('//div[@id="info"]/span[@property="v:initialReleaseDate"]/text()').extract())
        # 片长
        run_time = str(response.xpath('//div[@id="info"]/span[@property="v:runtime"]/text()').extract()[0])
        # 电影名称
        title = ''.join(response.xpath('//div[@id="content"]/h1/span/text()').extract())
        # 电影评分
        score = str(response.xpath('//div[@id="interest_sectl"]//strong[@property="v:average"]/text()').extract()[0])
        # 电影简介
        summary = str(
            response.xpath('//div[@id="link-report"]//span[@property="v:summary"]/text()').extract()[0]).strip()
        regex = re.compile('.*?<span class="pl">语言:</span>(.*?)<br>.*?')
        # 电影语言，由于没有具体的标签，所以使用正则解析
        language = str(response.xpath('//div[@id="info"]').re(regex)[0])
        regex = re.compile('.*?<span class="pl">制片国家/地区:</span>(.*?)<br>.*?')
        # 电影制片国家/地区，采用正则解析
        areas = str(response.xpath('//div[@id="info"]').re(regex)[0])
        # 电影豆瓣url
        movie_url = response.url
        item = DoubanItem()
        for field in item.fields:
            item[field] = eval(field)
        yield item
