
import imMail
import logging
import sendMail
import requests
from lxml import etree

# 判断一个unicode是否是英文字母
def is_alphabet(uchar):         
    if ('\u0041' <= uchar<='\u005a') or ('\u0061' <= uchar<='\u007a'):
        return True
    else:
        return False
    
def is_punctuations(uchar):
    punctuations_list = ['.', '-', '\'']
    if (uchar in punctuations_list):
        return True
    else:
        return False

class moives:
    def __init__(self):
        self.sendedList = imMail.checkMailFolderList(['mv', 'downloaded', 'downloading'])
        logging.debug(self.sendedList)
    
    def send(self, moiveE):
        if (moiveE.nameEnglish in self.sendedList):
            return
        moiveE.findEd2kLink()
        if moiveE.ed2k:
            logging.critical(moiveE.nameEnglish + ' ' + moiveE.nameOrigin)
            self.sendedList.append(moiveE.nameEnglish)
            sendMail.sendMail(moiveE.nameEnglish, moiveE.ed2kLink)#, receiver='presouce@163.com', sendFrom='163')
    
    def downloaded(self, nameEnglish):
        imMail.moveMail(nameEnglish, 'downloading', 'downloaded')

class moiveE:
    def __init__(self, nameOrigin, link, session):
        self.nameOrigin = nameOrigin
        self.link = link
        self.session = session
        self.__changeEnglishName()
    # /resource/moreway/338623
    # http://www.zimuzu.tv/resource/moreway/353117
    def __changeEnglishName(self):
        nameEnglish = ''
        nameBegin = False
        for i in self.nameOrigin:
            if(is_alphabet(i)):
                nameBegin = True
            if nameBegin:
                if(i.isdigit() or is_alphabet(i) or is_punctuations(i)):
                    nameEnglish += i
                else:
                    break
        self.nameEnglish = 'mv:' + nameEnglish
        
    def findEd2kLink(self):
        url = 'http://www.zimuzu.tv'
        f = self.session.get(url+self.link)
        selector = etree.HTML(f.text)
        # /html/body/div[4]/div/div/ul[1]/li/div[2]/a[1]
        # /html/body/div[4]/div/div/ul[1]/li/div[2]/a[1]
        # self.ed2kLink = selector.xpath('/html/body/div[4]/div/div/ul[1]/li/div[2]/a[1]/@href')
        self.ed2kLink = selector.xpath('//div[@class="links"]/a[1]/@href')[0]
        if self.ed2kLink.startswith('ed2k'):
            self.ed2k = True
        else:
            self.ed2k = False
        
    def display(self):
        print(self.nameEnglish + " " + self.nameOrigin)
        #print(self.link)
        self.findEd2kLink()
        print(self.ed2kLink)
        if self.ed2k:
            print(self.ed2kLink)
        else:
            print('not ed2k')