from lxml import etree
import requests
import time
from selenium import webdriver


class SendShouqu:
    def __init__(self):
        pass
    
    def login(self):
        self.browser.get('http://shouqu.me/#')
        self.browser.find_element_by_xpath('//*[@id="link_login"]').click()
        time.sleep(4)
        self.browser.find_element_by_xpath('//*[@id="login"]/div[1]/input').send_keys('18819954764')
        self.browser.find_element_by_xpath('//*[@id="login"]/div[2]/input').send_keys('q12345')
        # //*[@id="btn_login"]
        self.browser.find_element_by_xpath('//*[@id="btn_login"]').click()
        time.sleep(4)
        
    def send(self, link):
        # self.browser = webdriver.Firefox()
        self.browser = webdriver.PhantomJS()
        self.browser.set_window_size(1920, 1080)
        self.login()
        # //*[@id="firstcontent"]/img[2]
        self.browser.find_element_by_xpath('//*[@id="firstcontent"]/img[2]').click()
        time.sleep(4)
        # //*[@id="addMarkbubble"]/div[3]/input[1]
        self.browser.find_element_by_xpath('//*[@id="addMarkbubble"]/div[3]/input[1]').send_keys(link)
        # //*[@id="addMarkbubble"]/div[3]/input[2]
        self.browser.find_element_by_xpath('//*[@id="addMarkbubble"]/div[3]/input[2]').click()
        self.quit()
        
    def quit(self):
        self.browser.quit()
        