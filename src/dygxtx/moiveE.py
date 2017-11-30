import imMail
import logging
import sendMail
import requests
from lxml import etree
from selenium import webdriver
import pandas as pd
import os

from selenium.webdriver.common.keys import Keys

# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s -%(message)s')

# 判断一个unicode是否是英文字母
def is_alphabet(uchar):         
    if ('\u0041' <= uchar<='\u005a') or ('\u0061' <= uchar<='\u007a'):
        return True
    else:
        return False
    
class MoiveWait():
    def __init__(self, dyName, receiver, foundFlag):
        self.dyName = dyName
        self.receiver = receiver
        self.foundFlag = foundFlag
        
    def DownloadLink(self, link):
        session = requests.Session()
        headers = {
            'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
        }
        f = session.get(link, headers = headers)
        selector = etree.HTML(f.text)
        # /html/body/div[4]/div/div/ul[1]/li/div[2]/a[1]
        # /html/body/div[4]/div/div/ul[1]/li/div[2]/a[1]
        # self.ed2kLink = selector.xpath('/html/body/div[4]/div/div/ul[1]/li/div[2]/a[1]/@href')
        driver = webdriver.PhantomJS()
        driver.get(link)
        plists = driver.find_elements_by_xpath('//div[@id="nucms_downlist"]/div')
        downloadLink = ''
        minSize = 999
        # //*[@id="nucms_downlist"]/div[1]
        for plist in plists:
            plist.send_keys(Keys.DOWN)
            lis = plist.find_elements_by_xpath('./ul/li')
            checkPartName = plist.find_element_by_xpath('./h2').text
            logging.debug("now check" + checkPartName)
            if not plist.find_element_by_xpath('./h2').text[0].isnumeric() : 
                # 非 720/1080 p下载地址
                continue
            # //*[@id="nucms_downlist"]/div[3]/h2
            for li in lis:
                # //*[@id="nucms_downlist"]/div/ul/li[1] /a
                try:
                    sizeStr = li.find_element_by_xpath('./a').get_attribute('title').split('[')[1].split(']')[0]
                    if ('G' not in sizeStr):    # 大小不是GB 级别
                        continue
                    size = float(sizeStr.split('G')[0])
                except:
                    size = 99
                if (size < minSize):
                    minSize = size
                    logging.debug(size)
                    # //*[@id="nucms_downlist"]/div/ul/li[1] /span/a
                    # //*[@id="nucms_downlist"]/div[1]/ul/li/span/a
                    downloadLink = li.find_element_by_xpath('./span/a').get_attribute('href')
        driver.quit()
        return downloadLink
        
class Moives:
    def __init__(self, dyPd):
        self.moiveList = []
        self.nameList = []
        self.dyPd = dyPd
        for ith in dyPd.values:
            if ith[2] == 'F':
                self.addWaitMoive(ith[0], ith[1], ith[2])
        logging.debug(self.dyPd)
                
    def addWaitMoive(self, dyName, receiver, foundFlag):
        moiveWait = MoiveWait(dyName, receiver, foundFlag)
        self.moiveList.append(moiveWait)
        self.nameList.append(dyName)
        
    def sendMail(self, moiveWait, link):
        logging.info('mv: ' + moiveWait.dyName)
        logging.info(moiveWait.DownloadLink(link))
        sendMail.sendMail('mv: ' + moiveWait.dyName, moiveWait.DownloadLink(link))#, receiver='presouce@163.com', sendFrom='163')
        if (moiveWait.receiver == moiveWait.receiver):
            sendMail.sendMail('mv: ' + moiveWait.dyName, moiveWait.DownloadLink(link), receiver=moiveWait.receiver, sendFrom='163')
        else:
            logging.debug('only send to myself')
    
    def reWriteIni(self):
        module_path = os.path.dirname(__file__)
        filename = module_path + '/ini.csv'
        self.dyPd.to_csv(filename, encoding='utf-8', index=False)
    
    def check(self, dyName, link):
        if(dyName in self.nameList):
            for moive in self.moiveList:
                if(moive.dyName == dyName):
                    logging.critical(dyName + " found")
                    logging.debug(self.dyPd.loc[self.dyPd['name'] == dyName , 'foundFlag'])
                    self.dyPd.loc[self.dyPd['name'] == dyName , 'foundFlag'] = 'T'
                    self.sendMail(moive, link)
                    self.reWriteIni()
                    return
    

           
''' 
driver = webdriver.PhantomJS()
driver.get('http://www.btbtdy.com/btdy/dy11658.html#download')
link = driver.find_element_by_xpath('//*[@id="nucms_downlist"]/div[1]/ul/li/span/a')
print(link.get_attribute('href'))
driver.quit()
'''