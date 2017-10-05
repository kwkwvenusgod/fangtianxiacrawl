import scrapy
import time
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
        else:
            self.driver.close()

    def parse_page2(self, response):

        district = response.xpath('//p[@class="now-search-term"]/a[2]/text()').extract()
        for item_history in response.css("ul.watch-record-text2"):

            layout = item_history.xpath('.//li/p[@class="hx-text"]/b/text()').extract()
            structure_condition = item_history.xpath('.//li/p[@class="hx-text"]/span[@class="small-font"]/text()').extract()
            square = item_history.xpath('.//li[2]/text()').extract()
            contract_date = item_history.xpath('.//li[3]/text()').extract()
            price = item_history.xpath('.//li[4]/text()').extract()
            unit_price = item_history.xpath('.//li[5]/text()').extract()

            yield {"layout": layout, "condition": structure_condition, "square": square, "contract_date": contract_date,
                   "price": price, "unit_price": unit_price, "district":district}

        dealt_pages = response.xpath('//ul[@class="deal-page"]/a')

        self.driver.get(response.url)

        for i in range(1, len(dealt_pages)):
            if (i == 1) | (i == 2) | (i == len(dealt_pages)):
                continue
            next_deal_script = self.driver.find_element_by_css_selector('.deal-page a:nth-child(' + str(i) + ')').get_attribute('onclick')
            self.driver.execute_script(next_deal_script)
            time.sleep(5)
            infos = self.driver.find_elements_by_css_selector('ul.watch-record-text2')
            for info in infos:
                layout = info.find_element_by_css_selector('li p.hx-text b').text
                structure_condition = info.find_element_by_css_selector('li p.hx-text span.small-font').text
                square = info.find_elements_by_css_selector('li:nth-child(2)')[0].text
                contract_date = info.find_elements_by_css_selector('li:nth-child(3)')[0].text
                price = info.find_elements_by_css_selector('li:nth-child(4)')[0].text
                unit_price = info.find_elements_by_css_selector('li:nth-child(5)')[0].text

                yield {"layout": layout, "condition": structure_condition, "square": square,
                        "contract_date": contract_date,"price": price, "unit_price": unit_price,"district":district}












