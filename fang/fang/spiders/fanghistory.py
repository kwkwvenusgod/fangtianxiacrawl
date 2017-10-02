# -*- coding: utf-8 -*-
import scrapy
import copy


class FangtianxiahistorySpider(scrapy.Spider):
    name = 'fangtianxiahistory'

    start_urls = ['http://esf.nanjing.fang.com//']

    def parse(self, response):
        instance_url_list = response.css("p.title>a::attr(href)").extract()

        for instance_url in instance_url_list:
            yield scrapy.Request(url=response.urljoin(instance_url),callback=self.parse_page2)

        next_page_url = response.css("a#PageControl1_hlk_next::attr(href)").extract_first()
        if next_page_url is not None:
            yield scrapy.Request(url=response.urljoin(next_page_url), callback=self.parse)

    def parse_page2(self, response):
        general_info = {'小区':'','区域':'','学校':''}
        for item in response.xpath('//div[@class="trl-item2"]'):
            key = item.xpath('.//div[@class="lab"]').extract()
            value = item.xpath('.//div[@class="rcont"]/a').extract()
            if key == '小区':
                general_info['小区'] = value
            elif key == '区域':
                general_info['区域'] = value
            elif key == '学校':
                general_info['学校'] = value

        for item in response.xpath('//div[@class="ti-item-t"]'):
            keys = item.xpath('.//span[@class="lab"]/text()').extract()
            values = item.xpath('.//span[@class="lab-c"]/text()').extract()
            info_dict = copy.deepcopy(general_info)
            for i in range(len(keys)):
                info_dict.update({keys[i]: values[i]})
            yield info_dict



