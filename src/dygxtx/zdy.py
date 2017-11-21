import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import WorkInTime
from lxml import etree
import moiveE
import logging
import time
from multiprocessing import Process, Value
import threading
import os

logging.basicConfig(level=logging.CRITICAL, format='%(asctime)s - %(levelname)s -%(message)s')

def checkBtDy(dyWait):  # 
    session = requests.Session()
    #print(login_session.status_code)
    #print(_cookies.get_dict())
    site = 'http://www.btbtdy.com'
    url = 'http://www.btbtdy.com/btfl/dy1.html'
    time.sleep(5)
    f = session.get(url)
    selector = etree.HTML(f.text)
    # print(selector)
    ## /html/body/div[4]/div/div/div[2]/div/ul/li[1] /div[2]/ul/li[1] /a[1]/span
    # /html/body/div[4]/div/div/div[2]/div/ul/li[1] /div[2]/ul/li[1] /div/div/div/a[2]
    ## /html/body/div[4]/div/div/div[2]/div/ul/li[1]/div[2]/ul/li[2]/a[1]/span
    # /html/body/div[4]/div/div/div[2]/div/ul/li[1]/div[2]/ul/li[2]/div/div/div/a[2]
    
    # /html/body/div[4]/div/div/div[2]/div/ul/li[2]/div[2]/ul/li[1]/a[1]/span
    content_field = selector.xpath('//div[@class="liimg"]')
    for each in content_field:
        # /html/body/div[4]/ul/li[2]/div[1]  /a
        moiveName = each.xpath('./a/@title')[0]
        link = site + each.xpath('./a/@href')[0]
        banben = each.xpath('./a/span/text()')[0]
        if (banben == '预告片' or banben == '抢先版'):
            continue
        # /html/body/div[4]/ul/li[2]/div[1]  /a/span
        souce = each.xpath('../div[2]/p[1]/span/text()')[0]
        # /html/body/div[4]/ul/li[2]/div[2]/p[1]/span
        '''
        logging.debug(moiveName)
        logging.debug(link)
        logging.debug(banben + ' ' + souce)
        '''
        dyWait.check(moiveName, link)
    # print(f.content.decode())

    logging.critical('wait moive(s):' )
    logging.critical(dyWait.nameList)

runFlag = Value('b', True)

def checkRunFlag():
    module_path = os.path.dirname(__file__)
    filename = module_path + '/zdy.pyrunable.txt'
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
    
    
    timeBucket =[['17:29', '17:32']]
    
    workTime = WorkInTime.WorkInTime(timeBucket, relaxTime=60*10)
    
    while runFlag.value:
        
        relaxNow = threading.Thread(target=workTime.relax, args=(runFlag,))
        relaxNow.start()
        relaxNow.join()
        
        module_path = os.path.dirname(__file__)
        filename = module_path + '/ini.csv'
        dyPd = pd.read_csv(filename)
        dyWait = moiveE.Moives(dyPd)
        if (len(dyWait.nameList) == 0):
            logging.critical('no moives wait!')
        else:
            checkBtDy(dyWait)
            
