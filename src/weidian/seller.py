import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import sendMail
import logging
import requests
from lxml import etree
import re
import imMail

class Seller:
    def __init__(self, name, link):
        self.name = name
        self.link = link
        # print(link)
        # print(name + ' ' + self.id)
        
    def matchBuyer(self, itemData, flagMathMode1=False):
        result = ''
        if(itemData['stock'] == 0):
            return result
        # 寻找L, LL, XL 型号
        match1 = (re.search('.?.?L', (itemData['title'])))
        if match1: 
            flagMathMode1 = True
            # 使用Match获得分组信息 
            if (len(match1.group()) >= 2):
                if(match1.group()[0] == 'X' or match1.group()[0].isdigit() or match1.group()[1].isdigit()):
                    return result
            result = itemData['title'] + ' ' + str(itemData['stock'])
        if flagMathMode1:
            return result
        match2 = (re.search('175|180', (itemData['title'])))
        if match2: 
            # 使用Match获得分组信息 
            flag = True
            result = itemData['title'] + ' ' + str(itemData['stock'])
        return result
    
    def findItemRecDay(self):
        self.sendedList = imMail.checkMailFolderList(['wm', 'notbuy'])
        # print(self.sendedList)
        browser = webdriver.PhantomJS()
        html = requests.get(self.link)
        selector = etree.HTML(html.text)
        browser.get(self.link)
        time.sleep(1)
        js="document.documentElement.scrollTop=890"
        browser.execute_script(js)
        time.sleep(10)
        browser.find_element_by_xpath('//*[@id="tabbarItems"]/span[4]').click()
        # //*[@id="J-tab-bar"]/div[4]/div[1]/ul/div[2]/li[2]
        divs = browser.find_elements_by_xpath('//*[@id="J-tab-bar"]/div[4]/div[1]/ul/div')
        for div in divs:
            lis = div.find_elements_by_xpath('./li')
            # time.sleep(4)
            # todo sleep
            for li in lis:
                itemName = li.find_element_by_xpath('./a/p').text
                if (self.filtName(itemName)):
                    continue
                # //*[@id="J-tab-bar"]/div[4]/div[1]/ul/div[1]/li[2]/a/div[2]/p[1]/em[2]
                itemPrice = li.find_element_by_xpath('./a/div[2]/p[1]/em[2]').text
                title = str(itemPrice) + ": " + itemName
                if (('yf:'+title) in self.sendedList):
                    logging.critical('already sended ' + title)
                    continue
                # link
                # //*[@id="J-tab-bar"]/div[4]/div[30]/ul/div[2]/li[1]/a
                link = li.find_element_by_xpath('./a').get_attribute("href")
                # //*[@id="tuijianItem"]/ul/div[7]/li[1]/a/div[1]/div/span/img
                # data-src
                picLink = li.find_element_by_xpath('./a/div[1]/div/span/img').get_attribute("data-src")
                
                # //*[@id="J-tab-bar"]/div[4]/div[1]/ul/div[1]/li[1]/a/div[2]/div
                # 
                try:    #售罄则跳过
                    itemDataDiv = li.find_element_by_xpath('./a/div[2]/div')
                    itemDatas = eval(itemDataDiv.get_attribute("data-skuid")[1:-1])
                except:
                    continue
                
                logging.debug(itemDatas)
                logging.debug(type(itemDatas))
                findResult = ''
                if(type(itemDatas) == tuple):
                    for itemData in itemDatas:
                        findResult += self.matchBuyer(itemData)
                else:
                    findResult += self.matchBuyer(itemDatas)
                if (len(findResult) > 1):
                    logging.critical('Send mail:' + title)
                    context = link + '\n'
                    context += findResult + '\n'
                    logging.critical(context)
                    # print(picLink)
                    sendMail.sendMailPic('yf:'+title, context, picLink)
            
            
        logging.info('test')
        browser.quit()
    
    def gundong(self, browser):
        for i in range(10):
            js="document.documentElement.scrollTop=1000000"
            browser.execute_script(js)
            time.sleep(1)
    
    def filtName(self, itemName):
        if ('童' in itemName):
            return True
        if ('女' in itemName and '男女' not in itemName):
            return True
        return False
        
    
    def findAllItem(self):
        browser = webdriver.Firefox()
        html = requests.get(self.link)
        selector = etree.HTML(html.text)
        browser.get(self.link)
        time.sleep(1)
        js="document.documentElement.scrollTop=890"
        browser.execute_script(js)
        time.sleep(4)
        browser.find_element_by_xpath('//*[@id="tabbarItems"]/span[4]').click()
        # time.sleep(4)
        self.gundong(browser)
        # //*[@id="J-tab-bar"]/div[4]/div[1]
        # //*[@id="J-tab-bar"]/div[4]/div[4]
        time.sleep(3)
        divs = browser.find_elements_by_xpath('//*[@id="J-tab-bar"]/div[4]/div')
        # todo sleep
        # //*[@id="J-tab-bar"]/div[3]/div
        for div in divs:
            div2s = div.find_elements_by_xpath('./ul/div')
            for div2 in div2s:
                lis = div2.find_elements_by_xpath('./li')
                for li in lis:
                    li.send_keys(Keys.DOWN)
                    # //*[@id="J-tab-bar"]/div[3]/div[2]/ul[1]/div[1]/li[2]
                    # //*[@id="J-tab-bar"]/div[4]/div[1]/ul/div[1]/li[1]/a/p
                    itemName = li.find_element_by_xpath('./a/p').text
                    if (self.filtName(itemName)):
                        continue
                    # //*[@id="J-tab-bar"]/div[4]/div[1]/ul/div[1]/li[2]/a/div[2]/p[1]/em[2]
                    itemPrice = li.find_element_by_xpath('./a/div[2]/p[1]/em[2]').text
                    # link
                    # //*[@id="J-tab-bar"]/div[4]/div[30]/ul/div[2]/li[1]/a
                    link = li.find_element_by_xpath('./a').get_attribute("href")
                    # //*[@id="tuijianItem"]/ul/div[7]/li[1]/a/div[1]/div/span/img
                    # data-src
                    picLink = li.find_element_by_xpath('./a/div[1]/div/span/img').get_attribute("data-src")
                    
                    # //*[@id="J-tab-bar"]/div[4]/div[1]/ul/div[1]/li[1]/a/div[2]/div
                    # 
                    try:    #售罄则跳过
                        itemDataDiv = li.find_element_by_xpath('./a/div[2]/div')
                        itemDatas = eval(itemDataDiv.get_attribute("data-skuid")[1:-1])
                    except:
                        continue
                    
                    logging.debug(itemDatas)
                    logging.debug(type(itemDatas))
                    findResult = ''
                    if(type(itemDatas) == tuple):
                        for itemData in itemDatas:
                            findResult += self.matchBuyer(itemData)
                    else:
                        findResult += self.matchBuyer(itemDatas)
                    if (len(findResult) > 1):
                        title = str(itemPrice) + ": " + itemName
                        print(title)
                        context = link + '\n'
                        context += findResult + '\n'
                        print(context)
                        print(picLink)
                        sendMail.sendMailPic('yf:'+title, context, picLink)
                        # return
            
        logging.info('test')
        # browser.quit()
        