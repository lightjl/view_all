import os
import logging
import threading
import time
from multiprocessing import Process, Value
import threading
import WorkInTime
import emailAccount
from imbox import Imbox
import imMail

#timeB = [['19:46', '23:00']]
logging.basicConfig(level=logging.CRITICAL, format='%(asctime)s - %(levelname)s -%(message)s')


#checkToday888(jdtm)


def recoveryMail(alive, wk):
    while  alive.value:
        logging.critical('正在回收邮件')
        eBox = Imbox('imap-mail.outlook.com',
            username=emailAccount.hotname,
            password=emailAccount.hotpass,
            ssl=True,
            ssl_context=None)
        imMail.delMail(eBox, 'Inbox')
        imMail.delMail(eBox, 'Sent')
        imMail.delMailLt(eBox, 'dy', 15)
        imMail.markReaded(eBox, 'xiaoshuo')
        imMail.delMailLt(eBox, 'xiaoshuo', 20)
        imMail.markReaded(eBox, 'nihuigou')
        imMail.delMailLt(eBox, 'nihuigou', 1)
        eBox.logout()
        relaxNow = threading.Thread(target=wk.relax, args=(alive, '邮件回收'))
        relaxNow.start()
        relaxNow.join()


runFlag = Value('b', True)

def checkRunFlag():
    module_path = os.path.dirname(__file__)
    filename = module_path + '/mr.pyrunable.txt'
    file_object = open(filename, 'r')
    try:
        flag_run = file_object.read()
    finally:
        file_object.close()
    while flag_run == 'True':
        time.sleep(5)
        file_object = open(filename, 'r')
        try:
            flag_run = file_object.read()
        finally:
            file_object.close()
    runFlag.value = False

if __name__ == '__main__':
    timeB = [['23:03', '23:09']]
    wk = WorkInTime.WorkInTime(timeB, 60*10, 11)  # 休息10分钟
    #logging.info(xsPd)
    
    # 检查是否要运行
    checkRun = threading.Thread(target=checkRunFlag, args=())
    checkRun.start()
    
    recoveryMail(runFlag, wk)

