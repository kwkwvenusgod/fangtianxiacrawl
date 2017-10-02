# -*- coding: utf-8 -*-
import scrapy


class FangtianxiaSpider(scrapy.Spider):
    name = 'fangtianxia'

    start_urls = ['http://esf.nanjing.fang.com//']

    def parse(self, response):
        house_list_price = response.css("span.price::text").extract()
        square_list = response.css("div.area > p:nth-child(-n+1)::text").extract()
        unit_price_list = self.proc_list(response.css("p.danjia::text").extract())
        location_list = response.css("span.iconAdress::text").extract()
        district_list = response.css("p.mt10>a>span::text").extract()
        instance_url_list = response.css("p.title>a::attr(href)").extract()

        for item in zip(house_list_price,square_list,unit_price_list,location_list,district_list,instance_url_list):
            yield {'price':item[0],
                   'square meter':item[1],
                   'unit price': item[2],
                   'location': item[3],
                   'district': item[4],
                   'detail_url': item[5]}

        next_page_url = response.css("a#PageControl1_hlk_next::attr(href)").extract_first()
        if next_page_url is not None:
            yield scrapy.Request(url=response.urljoin(next_page_url))

    def proc_list(self,list_item):
        res = []
        for i in xrange(0,len(list_item),2):
            res.append(list_item[i])
        return res


