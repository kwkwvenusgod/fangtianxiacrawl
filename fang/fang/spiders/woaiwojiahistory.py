import scrapy


class WoAiWoJiaHistory(scrapy.Spider):

    name = "woaiwojiahistory"
    start_urls = ["http://nj.5i5j.com/exchange/"]

    def parse(self, response):
        for url_sub in response.css("ul.list-body>li>a::attr(href)").extract():
            yield scrapy.Request(url=response.urljoin(url_sub), callback=self.parse_page2)

    def parse_page2(self, response):
        for item_history in response.css("watch-record-text2").extract():
            item_detail = item_history.xpath(".//li/text()").extract()
            tmp = {'square': item_detail[1], 'contract date': item_detail[2], 'deal price': item_detail[3], 'unit price':item_detail[3]}
            yield tmp




