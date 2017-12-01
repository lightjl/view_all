
import imMail
import logging
import sendMail

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
        if moiveE.ed2k:
            logging.critical(moiveE.nameEnglish + ' ' + moiveE.nameOrigin)
            self.sendedList.append(moiveE.nameEnglish)
            sendMail.sendMail(moiveE.nameEnglish, moiveE.ed2kLink)#, receiver='presouce@163.com', sendFrom='163')
    
    def downloaded(self, nameEnglish):
        imMail.moveMail(nameEnglish, 'downloading', 'downloaded')

class moiveE:
    def __init__(self, nameOrigin, ed2kLink):
        self.nameOrigin = nameOrigin
        self.ed2kLink = ed2kLink
        self.__changeEnglishName()
        if ed2kLink.startswith('ed2k'):
            self.ed2k = True
        else:
            self.ed2k = False
        
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
        
    def display(self):
        print(self.nameEnglish + " " + self.nameOrigin)
        if self.ed2k:
            print(self.ed2kLink)
        else:
            print('not ed2k')