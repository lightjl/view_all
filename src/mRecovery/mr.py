import os
import logging
import threading
import time
from multiprocessing import Process, Value
import threading
import WorkInTime
import emailAccount
from imbox import Imbox

#timeB = [['19:46', '23:00']]
logging.basicConfig(level=logging.CRITICAL, format='%(asctime)s - %(levelname)s -%(message)s')


#checkToday888(jdtm)

def markReaded(emailbox, folder):
    
    messagesToRead = emailbox.messages(folder=folder, unread=True)
    for uid, message in messagesToRead:
    # Every message is an object with the following keys
        logging.info(message.subject)
        emailbox.mark_seen(uid)

def recoveryMail(alive, wk):
    while  alive.value:
        logging.critical('正在回收邮件')
        eBox = Imbox('imap-mail.outlook.com',
            username=emailAccount.hotname,
            password=emailAccount.hotpass,
            ssl=True,
            ssl_context=None)
        messages_folder = eBox.messages(folder='Inbox')
        for uid, message in messages_folder:
        # Every message is an object with the following keys
            logging.info(message.subject)
            eBox.delete(uid)
            # print((message.body)['plain'])
        markReaded(eBox, 'xiaoshuo')
        markReaded(eBox, 'nihuigou')
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

