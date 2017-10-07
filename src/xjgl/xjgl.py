
import json
import requests
from datetime import *
import os
import time
import sendMail
import WorkInTime
from multiprocessing import Process, Value
import threading
import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s -%(message)s')

class Xjgl(object):
    __highIn = 0

    def __init__(self, highIn, setDay = datetime.now().day):
        self.__highIn = highIn
        self.__initHigh = highIn
        self.__setDay = setDay

    def setInitHigh(self, highIn):
        self.__initHigh = highIn

    def reset(self):
        self.__highIn = self.__initHigh
        self.__setDay = datetime.now().day

    def WatchXjgl(self):
        sendString = ''
        if datetime.now().day != self.__setDay:
            self.__setDay = now.day

    def WatchXjgl(self):
        sendString = ''
        if now.day != self.__setDay:
            self.reset()
        try:
            check_seesion = requests.Session()
            url = 'https://www.jisilu.cn/data/repo/sz_repo_list/?___t=1489544161142'
            xjglInfo = check_seesion.get(url)
            #print(xjglInfo.content.decode())
            jsonXjgl = json.loads(xjglInfo.content.decode())
        except:
            return
        i = 0
        #for row in jsonXjgl['rows']:
        row = jsonXjgl['rows'][0]
        #print(row)
        rowHigh = float(row['cell']['price'])
        if rowHigh > self.__highIn:    #新高超过前基准
            sub = '逆回购: ' + row['id'] + ' 破 ' + str(self.__highIn) + ', 现价: ' + row['cell']['price']
            self.__highIn = max(self.__highIn * 1.3, rowHigh)
            print(sub)
            sendMail.sendMail(sub, "")


now = datetime.now()
nowDay = now.day
priceIn = 4.6
logging.info("现金管理正在运行")
timeTrade = [['9:30', '11:30'], ['13:00', '15:00']]
workTime = WorkInTime.WorkInTime(timeTrade, weekday='0,1,2,3,4')


runFlag = Value('b', True)

def checkRunFlag():
    module_path = os.path.dirname(__file__)
    filename = module_path + '/xjgl.pyrunable.txt'
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
    
    xjglWatch = Xjgl(priceIn)
    module_path = os.path.dirname(__file__)
        
    while runFlag.value:
        if now.weekday() ==4:
            xjglWatch.setInitHigh(priceIn*3)
        else:
            xjglWatch.setInitHigh(priceIn)
        #logging.info(datetime.now())
        xjglWatch.WatchXjgl()
        
        relaxNow = threading.Thread(target=workTime.relax, args=(runFlag,))
        relaxNow.start()
        relaxNow.join()
        

