import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import sendMail

class maiJia:
    def __init__(self, name, link):
        self.name = name
        self.link = link
        self.id = link.split('/')[-1]
        # print(link)
        # print(name + ' ' + self.id)
        
    def findFood(self, priceTotal = 50):
        browser = webdriver.Firefox()
        baseUrl = 'https://h5.ele.me/shop/#geohash=ws0ed952uqk9&id='
        linkM = baseUrl + str(self.id)
        browser.get(linkM)
        # /html/body/div[1]/div/div/div[3]/div[2]/div/footer/div[3]/a/span
        time.sleep(2)
        priceStr = browser.find_element_by_xpath('/html/body/div[1]/div/div/div[3]/div[2]/div/footer/div[3]/a/span').text
        priceMin = int(priceStr.split('¥')[1].split('起')[0])
        sendPriceStr = browser.find_element_by_xpath('/html/body/div[1]/div/div/div[3]/div[2]/div/footer/div[3]/div/p[2]').text
        if (len(sendPriceStr) == 0):
            sendPrice = -1
        else:
            sendPrice = float(sendPriceStr.split('¥')[1])
        # print(priceMin)
        time.sleep(1)
        browser.find_element_by_xpath('/html/body/div[1]/div/div/div[3]/div[2]/main/ul/li[2]/span').click()
        time.sleep(3)
        youhuiItems = browser.find_elements_by_xpath('/html/body/div[1]/div/div/div[3]/div[2]/main/section/div[1]/dl[2]/dd')
        text = ''
        textmin = ''
        for youhuiItem in youhuiItems:
            youhuiItem.send_keys(Keys.DOWN)
            nameItem = youhuiItem.find_element_by_xpath('./div/div/section/header/span').text
            priceItem = youhuiItem.find_elements_by_xpath('./div/div/section/strong/span')
            price = float(priceItem[0].text)
            if (price  >= priceMin and price + sendPrice <= priceTotal and price >= 2):
                # print(nameItem + str(price))
                text += (nameItem + ' ' + str(price)) + '\n'
            elif (price < 9 and price < priceMin):
                textmin += (nameItem + ' ' + str(price)) + '\n'
                
        if len(text) > 0:
            print(self.name + ' 配送费 ' + str(sendPrice))
            print(linkM + '\n' + text + textmin)
            sendMail.sendMail('wm: ' + self.name + ' 配送费 ' + str(sendPrice), linkM + '\n' + text + textmin, changeReceiver=True)
        browser.quit()
            # /div/div/section/header/span
            # ./div/div/section/header/span
            # ./div/div/section/p[1]
        # /html/body/div[1]/div/div/div[3]/div[2]/main/section/div[1]/dl[1]/dd[7]/div/div/section/strong/span[1]
        # /html/body/div[1]/div/div/div[3]/div[2]/main/section/div[1]/dl[4]/dd[2]/div/div/section/strong/span[1]
        # /html/body/div[1]/div/div/div[3]/div[2]/main/section/div[1]/dl[2] /dd[5]/div/div/section/strong/span[1]
        # /html/body/div[1]/div/div/div[3]/div[2]/main/section/div[1]/dl[2]/dd[1]/div/div/section/strong/span
        # 起
        # /html/body/div[1]/div/div/div[3]/div[2]/main/section/div[1]/dl[1]/dd[10]/div/div/section/strong/span
        # /html/body/div[1]/div/div/div[3]/div[2]/main/section/div[1]/dll[11]/dd[1]/div/div/section/strong/span
        
        
        # /html/body/div[1]/div/div/div[3]/div[2]/main/section/div[1]/dl[2]/dd[1]/div/div/section/strong/span
        # /html/body/div[1]/div/div/div[3]/div[2]/main/section/div[1]/dl[2]/dd[1]/div/div/section/strong/del
        