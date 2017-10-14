import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import sendMail
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s -%(message)s')

class maiJia:
    def __init__(self, name, link):
        self.name = name
        self.link = link
        self.id = link.split('/')[-1]
        # print(link)
        # print(name + ' ' + self.id)
        
    def findFood(self, priceTotal = 50):
        # browser = webdriver.Firefox()
        logging.info('checking ' + self.name)
        browser = webdriver.PhantomJS()
        baseUrl = 'https://h5.ele.me/shop/#geohash=ws0ed952uqk9&id='
        linkM = baseUrl + str(self.id)
        browser.get(linkM)
        # /html/body/div[1]/div/div/div[3]/div[2]/div/footer/div[3]/a/span
        time.sleep(4)
        priceStr = browser.find_element_by_xpath('/html/body/div[1]/div/div/div[3]/div[2]/div/footer/div[3]/a/span').text
        priceMin = int(priceStr.split('¥')[1].split('起')[0])
        sendPriceStr = browser.find_element_by_xpath('/html/body/div[1]/div/div/div[3]/div[2]/div/footer/div[3]/div/p[2]').text
        if (len(sendPriceStr) == 0):
            sendPrice = -1
        else:
            sendPrice = float(sendPriceStr.split('¥')[1])
        # print(priceMin)
        time.sleep(1)
        text = ''
        textmin = ''
        items = []
        for ith in range(1,4):
            # /html/body/div[1]/div/div/div[3]/div[2]/main/ul/li[2]
            browser.find_element_by_xpath('/html/body/div[1]/div/div/div[3]/div[2]/main/ul/li[%i]/span' % ith).click()
            time.sleep(3)
            youhuiItems = browser.find_elements_by_xpath('/html/body/div[1]/div/div/div[3]/div[2]/main/section/div[1]/dl[%i]/dd' % ith)
            for youhuiItem in youhuiItems:
                youhuiItem.send_keys(Keys.DOWN)
                try:
                    # /html/body/div[1]/div/div/div[3]/div[2]/main/section/div[1]/dl[2]/dd[2]/div/section/div[2]/span/span
                    textStatus = youhuiItem.find_element_by_xpath('./div/section/div[2]/span/span').text
                    if (textStatus == '已售完'):
                        continue
                except:
                    pass
                # /html/body/div[1]/div/div/div[3]/div[2]/main/section/div[1]/dl[1]/dd[2]/div/section/p[1]
                nameItem = youhuiItem.find_element_by_xpath('./div/section/p[1]').text
                logging.debug(nameItem)
                # /html/body/div[1]/div/div/div[3]/div[2]/main/section/div[1]/dl[1]/dd[4]/div/section/strong/span
                # /html/body/div[1]/div/div/div[3]/div[2]/main/section/div[1]/dl[1]/dd[5]/div/section/strong/span
                # /html/body/div[1]/div/div/div[3]/div[2]/main/section/div[1]/dl[1]/dd[5]/div/section/strong/span
                priceItem = youhuiItem.find_element_by_xpath('./div/section/strong')
                logging.debug(priceItem)
                price = float(priceItem.find_element_by_xpath('./span').text)
                priceDel = price
                try:
                    # /html/body/div[1]/div/div/div[3]/div[2]/main/section/div[1]/dl[2]/dd[2]/div/section/strong/del
                    # /html/body/div[1]/div/div/div[3]/div[2]/main/section/div[1]/dl[1]/dd[5]/div/section/strong/del
                    priceDel = float(priceItem.find_element_by_xpath('./del').text.replace('¥',''))
                except:
                    priceDel = price
                    pass
                if nameItem in items:
                    continue
                if (priceDel  >= priceMin and price + sendPrice <= priceTotal and price >= 2):
                    # print(nameItem + str(price))
                    text += (nameItem + ' ' + str(price)) + '\n'
                    items.append(nameItem)
                elif (price < 9 and price < priceMin):
                    textmin += (nameItem + ' ' + str(price)) + '\n'
                    items.append(nameItem)
                
        if len(text) > 0:
            print(self.name + ' 配送费 ' + str(sendPrice))
            print(linkM + '\n' + text + textmin)
            sendMail.sendMail('wm: ' + self.name + ' 配送费 ' + str(sendPrice), linkM + '\n' + text + textmin, changeReceiver=True)
        browser.quit()
            # /div/div/section/header/span
            # ./div/div/section/header/span
            # ./div/div/section/p[1]
        # /html/body/div[1]/div/div/div[3]/div[2]/main/section/div[1]/dl[2]/dd[3]/div/div/section/div/span/span (已售完)
        # /html/body/div[1]/div/div/div[3]/div[2]/main/section/div[1]/dl[2]/dd[1]/div/div/section/strong/span
        # /html/body/div[1]/div/div/div[3]/div[2]/main/section/div[1]/dl[2]/dd[18]/div/div/section/strong/span
        # /html/body/div[1]/div/div/div[3]/div[2]/main/section/div[1]/dl[2]/dd[18]/div/div/section/strong/del
        # 起
        # /html/body/div[1]/div/div/div[3]/div[2]/main/section/div[1]/dl[1]/dd[10]/div/div/section/strong/span
        # /html/body/div[1]/div/div/div[3]/div[2]/main/section/div[1]/dll[11]/dd[1]/div/div/section/strong/span
        
        
        # /html/body/div[1]/div/div/div[3]/div[2]/main/section/div[1]/dl[2]/dd[1]/div/div/section/strong/span
        # /html/body/div[1]/div/div/div[3]/div[2]/main/section/div[1]/dl[2]/dd[1]/div/div/section/strong/del

# maiJia('test', 'https://h5.ele.me/shop/#geohash=ws0ed952uqk9&id=154946185').findFood(46)