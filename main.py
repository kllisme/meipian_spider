# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import time

from selenium import webdriver
from selenium.webdriver.chrome import options

# Press the green button in the gutter to run the script.

if __name__ == '__main__':
    try:
        o = options.Options()
        # o.headless = True
        driver = webdriver.Chrome(options=o)
        driver.get("https://www.meipian.cn")
        # driver.get("https://www.meipian.cn/3nimgip8?share_depth=1")

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
                print(url)
            next_button = driver.find_element_by_class_name("btn-next")
            next_button.get_attribute('text')
            if next_button.is_enabled():
                driver.execute_script("arguments[0].click();", next_button)
            else:
                flag = False
    except Exception as e:
        print(e)
        exit()
