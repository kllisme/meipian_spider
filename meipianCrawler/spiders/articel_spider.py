import time

import scrapy
from scrapy.loader import ItemLoader
from scrapy_selenium import SeleniumRequest
from selenium import webdriver
from selenium.webdriver.chrome import options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from meipianCrawler.items import ArticleItem


class ArticleSpider(scrapy.Spider):
    name = "articles"

    def start_requests(self):
        o = options.Options()
        o.headless = True
        driver = webdriver.Chrome(options=o)
        driver.get("https://www.meipian.cn")
        login_frame = driver.find_element_by_xpath('//iframe[@src="/officialWebsiteLogin"]')
        driver.switch_to.frame(login_frame)
        other_login_button = driver.find_element_by_xpath('//button[string()="其他方式登录"]')
        driver.execute_script("arguments[0].click();", other_login_button)

        id_login_button = driver.find_element_by_xpath('//button[string()="美篇号登录"]')
        driver.execute_script("arguments[0].click();", id_login_button)

        id_input = driver.find_element_by_xpath('//input[@placeholder="请输入美篇号"]')
        id_input.send_keys("18745199")

        passwd_input = driver.find_element_by_xpath('//input[@placeholder="请输入密码"]')
        passwd_input.send_keys("ldh888888")

        login_button = driver.find_element_by_xpath('//button[string()="登录"]')
        driver.execute_script("arguments[0].click();", login_button)
        time.sleep(3)
        driver.switch_to.default_content()
        flag = True
        while flag:
            shares = driver.find_elements_by_class_name("share")
            for share in shares:
                driver.execute_script("arguments[0].click();", share)
                url = driver.find_element_by_xpath('//button[string()="复制链接"]').get_attribute("data-clipboard-text")
                yield SeleniumRequest(url=url, callback=self.parse, wait_time=15,
                                      wait_until=EC.presence_of_element_located(
                                          (By.CSS_SELECTOR, 'div.mp-article-texts'))
                                      )
            next_button = driver.find_element_by_class_name("btn-next")
            next_button.get_attribute('text')
            if next_button.is_enabled():
                driver.execute_script("arguments[0].click();", next_button)
            else:
                flag = False
        driver.close()

    def parse(self, response):
        loader = ItemLoader(item=ArticleItem(), response=response)
        loader.add_xpath("caption", '//div[@class="caption-title-html"]/descendant::text()')
        loader.add_xpath("time", '//span[@class="mp-article-caption-subhead-time"]/text()')
        loader.add_xpath("time", '//div[@class="mp-article-caption-subhead-time"]/text()')
        loader.add_xpath("read_cnt", '//span[@class="mp-article-caption-subhead-count"]/span[2]/text()')
        loader.add_xpath("read_cnt", '//div[@class="mp-article-caption-subhead-count"]/text()')
        loader.add_xpath("content", '//div[@class="mp-article-texts mp-content"]/descendant::b/text()')
        loader.add_xpath("like_cnt", '//span[@class="content-like-word"]/text()')
        loader.add_xpath("images", '//img[@class="mp-article-images-item-img"]/@data-src')
        loader.add_css("jiajing",'span.img-icon-jiajing')
        loader.add_value("share_url", response.url)
        return loader.load_item()
