import scrapy
from selenium import webdriver


class WoAiWoJiaHistory(scrapy.Spider):

    def __init__(self):
        self.driver = webdriver.Firefox()
        self.download_delay = 0.25
        self.driver.implicitly_wait(60)

    name = "woaiwojiahistory"
    start_urls = ["http://nj.5i5j.com//exchange//"]

    def parse(self, response):
        for url_sub in response.css("ul.list-body>li>a::attr(href)").extract():
            yield scrapy.Request(url=response.urljoin(url_sub), callback=self.parse_page2)

        page_list = response.css("div.list-page>a::attr(href)").extract()
        if len(page_list) != 0:
            next_page = page_list[len(page_list)-1]
            yield scrapy.Request(url=response.urljoin(next_page), callback=self.parse)

    def parse_page2(self, response):
        for item_history in response.css("ul.watch-record-text2"):

            layout = item_history.xpath('.//li/p[@class="hx-text"]/b/text()').extract()
            structure_condition = item_history.xpath('.//li/p[@class="hx-text"]/span[@class="small-font"]/text()').extract()
            square = item_history.xpath('.//li[2]/text()').extract()
            contract_date = item_history.xpath('.//li[3]/text()').extract()
            price = item_history.xpath('.//li[4]/text()').extract()
            unite_price = item_history.xpath('.//li[5]/text()').extract()

            yield {"layout": layout, "condition": structure_condition, "square": square, "contract_date": contract_date,
                   "price": price, "unite_price": unite_price}

        dealt_pages = response.xpath('//ul[@class="deal-page"]/a')

        self.driver.get(response.url)
        while True:
            for i in range(1, len(dealt_pages)):
                if (i == 1) | (i == 2):
                    continue
                next = self.driver.find_element_by_xpath('//ul[@class="deal-page"]/a['+str(i) + ']')
                try:
                    next.click()
                    info = self.driver.find_element_by_css_selector('ul.watch-record-text2')
                    layout = self.driver.find_element_by_css_selector('//ul[@class=watch-record-text2]/li/p[@class="hx-text"]/b/text()')
                    structure_condition = self.driver.find_element_by_xpath(
                        '//ul[@class=watch-record-text2]/li/p[@class="hx-text"]/span[@class="small-font"]/text()')
                    square = self.driver.find_element_by_xpath('//ul[@class=watch-record-text2]/li[2]/text()')
                    contract_date = self.driver.find_element_by_xpath('//ul[@class=watch-record-text2]/li[3]/text()')
                    price = self.driver.find_element_by_xpath('//ul[@class=watch-record-text2]/li[4]/text()')
                    unite_price = self.driver.find_element_by_xpath('//ul[@class=watch-record-text2]/li[5]/text()')

                    yield {"layout": layout, "condition": structure_condition, "square": square,
                           "contract_date": contract_date,
                           "price": price, "unite_price": unite_price}
                except:
                    break

        self.driver.close()









