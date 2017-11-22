from lxml import etree
import requests
import sendMail
import recMail
import time
import datetime
import getContent
import WorkInTime
import threading
import logging
import imMail
import threading
import sendShouqu

from multiprocessing import Process, Value

#timeB = [['19:46', '23:00']]

class xs:
    def __init__(self, name, url, timeB):
        self.name = name
        self.__url = url
        self.__getContent = getContent.saveToFile('xs')
        self.timeB = timeB
        self.timeB.append(['23:59'] * 2)
        #print(self.timeB)
        self.wk = WorkInTime.WorkInTime(self.timeB, 60*10, 11)  # 休息10分钟
        self.sendedList = []

    def getUrl(self):
        return self.__url

    def isSave(self, filename):
        return self.__getContent.isSended(filename)

    def save(self, filename, text):
        self.__getContent.save(filename, text)

    def sendToKindle(self, filename, url=''):
        sendHotmail = threading.Thread(target=sendMail.sendMail, args=(filename, \
                'xs:'+filename+'\n'+url, 'ming188199@hotmail.com', 'hotmail', False))
        sendHotmail.start()
        
        # sendMail.sendMail(filename, 'xs:'+filename, receiver='ming188199@hotmail.com', sendFrom='hotmail')
        
        self.sendedList.append(filename)  # 送出后更新
        if '第' in filename:
            logging.debug("更新了"+filename)
            sendMail.send_attachment_kd(self.__getContent.sub_folder, filename)

    def relax(self, alive):
        relaxNow = threading.Thread(target=self.wk.relax, args=(alive,self.name))
        relaxNow.start()
        relaxNow.join()

    def sendShouqu(self, link):
        ss = sendShouqu.SendShouqu()
        ss.send(link)
        
    def sodu888(self, selector):
        zjUrlHead = 'http://www.sodu888.com'
        zjs = selector.xpath('//a[@rel="nofollow"]')
        # print(zjs)
        for zj in zjs:
            zjName = (zj.xpath('./text()')[0])
            # print(zjName)

            zjHref = zjUrlHead + (zj.xpath('./@href')[0])
            # print(zjHref)
            if zjName not in self.sendedList:
                try:
                    html = requests.get(zjHref)
                except:
                    continue
                html.encoding = 'utf-8'
                selector = etree.HTML(html.content)

                divs = (selector.xpath('//div[@id]'))
                text = ''
                for div in divs:
                    id = (div.xpath('@id'))[0]
                    if id == 'content' or id == 'contents' or id == 'txtContent':
                        # print(div.xpath('//text()'))
                        for eachP in (div.xpath('./text()')):
                            text += eachP + '\r\n'

                # print(text)
                if len(text) > 89:     # 避免下载空文件
                    ss = threading.Thread(target=self.sendShouqu, args=(zjHref,))
                    self.save(zjName, text)
                    self.sendToKindle(zjName, zjHref)
                    
                    
    def sodu(self, selector):
        zjs = selector.xpath('//div[@class="main-html"]')
        for zj in zjs:
            # /html/body/div[6]/div[1]/a
            zjName = (zj.xpath('./div[1]/a/text()')[0])
            if (zjName[-1] == '('):
                zjName = zjName[:-1]
            # print(zjName)

            zjHref = (zj.xpath('./div[1]/a/@href')[0])
            zjHref = zjHref.split('url=')[1]
            # print(zjHref)
            if zjName not in self.sendedList:
                try:
                    html = requests.get(zjHref)
                except:
                    continue
                html.encoding = 'utf-8'
                selector = etree.HTML(html.content)

                divs = (selector.xpath('//div[@id]'))
                text = ''
                for div in divs:
                    id = (div.xpath('@id'))[0]
                    if id == 'content' or id == 'contents' or id == 'txtContent':
                        # print(div.xpath('//text()'))
                        for eachP in (div.xpath('./text()')):
                            text += eachP + '\r\n'

                # print(text)
                if len(text) > 89:     # 避免下载空文件
                    ss = threading.Thread(target=self.sendShouqu, args=(zjHref,))
                    ss.start()
                    # 
                    self.save(zjName, text)
                    self.sendToKindle(zjName, zjHref)
        
    def checkToday(self):
        self.sendedList = imMail.checkMailList('xiaoshuo')
        #logging.info('checking' + self.name)
        # logging.critical(self.getUrl())
        try:
            url = self.getUrl()
            html = requests.get(url)
            selector = etree.HTML(html.text)
        except:
            return
        #print(html.text)
        
        #zjs = selector.xpath('//a[@rel="nofollow"]/text()')
        #print(zjs)

        # /html/body/div[6]
        if ("cc" in self.name):
            self.sodu(selector)
        elif("sodu3" in url or "sodu888" in url):
            self.sodu888(selector)
            
                