import WorkInTime
from lxml import etree
import logging
import time
from multiprocessing import Process, Value
import threading
import os
import seller

logging.basicConfig(level=logging.CRITICAL, format='%(asctime)s - %(levelname)s -%(message)s')


runFlag = Value('b', True)
ljxp = seller.Seller('邻居小铺', 'https://weidian.com/?userid=1173561383')

def checkRunFlag():
    module_path = os.path.dirname(__file__)
    filename = module_path + '/watch.pyrunable.txt'
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
    # 检查是否要运行
    checkRun = threading.Thread(target=checkRunFlag, args=())
    checkRun.start()
    timeBucket =[['9:00', '11:30'], ['15:00', '21:06']]
    
    workTime = WorkInTime.WorkInTime(timeBucket, relaxTime=60*5)
    logging.critical("watching weidian")
    # while True:
        #downloaded = checkDownloaded.checkDownloaded()
    while runFlag.value:
        ljxp.findItemRecDay()
        relaxNow = threading.Thread(target=workTime.relax, args=(runFlag,))
        relaxNow.start()
        relaxNow.join()
    # workTime.relax()


