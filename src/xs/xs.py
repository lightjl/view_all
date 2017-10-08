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

from multiprocessing import Process, Value

#timeB = [['19:46', '23:00']]

class xs:
    def __init__(self, name, url, timeB):
        self.name = name
        self.__url = url
        self.__getContent = getContent.saveToFile('xs')
        self.zjUrlHead = 'http://www.sodu888.com'
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

    def sendToKindle(self, filename):
        sendMail.sendMail(filename, filename, receiver='ming188199@hotmail.com', sendFrom='hotmail')
        
        self.sendedList.append(filename)  # 送出后更新
        if '第' in filename:
            logging.debug("更新了"+filename)
            sendMail.send_attachment_kd(self.__getContent.sub_folder, filename)

    def relax(self, alive):
        relaxNow = threading.Thread(target=self.wk.relax, args=(alive,self.name))
        relaxNow.start()
        relaxNow.join()


    def checkToday(self):
        self.sendedList = imMail.checkMailList('xiaoshuo')
        #logging.info('checking' + self.name)
        try:
            url = self.getUrl()
            html = requests.get(url)
            selector = etree.HTML(html.text)
        except:
            return
        #print(html.text)
        gxsj = selector.xpath('//td[@class="time"]/text()')

        if (len(gxsj) == 0):
            return

        #zjs = selector.xpath('//a[@rel="nofollow"]/text()')
        #print(zjs)


        zjs = selector.xpath('//a[@rel="nofollow"]')
        #print(zjs)
        for zj in zjs:
            zjName = (zj.xpath('./text()')[0])
            # print(zjName)

            zjHref = self.zjUrlHead + (zj.xpath('./@href')[0])
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
                if len(text) > 896:     # 避免下载空文件
                    self.save(zjName, text)
                    self.sendToKindle(zjName)
                