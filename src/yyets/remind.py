
import WorkInTime
from multiprocessing import Process, Value
import logging
import threading
import os
import time

import imMail
import logging
import sendMail

logging.basicConfig(level=logging.CRITICAL, format='%(asctime)s - %(levelname)s -%(message)s')


def checkMV():
    mvList = imMail.checkMailList('mv', True)
    if (len(mvList) == 0):
        return
    text = ''
    for name in mvList:
        text += name + '\n'
    sendMail.sendMail(str(len(mvList)) + ' moive(s) unread in MV', text)
    return

runFlag = Value('b', True)

def checkRunFlag():
    module_path = os.path.dirname(__file__)
    filename = module_path + '/mj.pyrunable.txt'
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
    
def remind():
    checkRun = threading.Thread(target=checkRunFlag, args=())
    checkRun.start()
    timeBucket =[['15:01', '15:06']]
    workTime = WorkInTime.WorkInTime(timeBucket, relaxTime=60*40)
    
    while runFlag.value:
        relaxNow = threading.Thread(target=workTime.relax, args=(runFlag,))
        relaxNow.start()
        relaxNow.join()
        logging.critical('reminding mv')
        checkMV()
    logging.critical('remind stopped')