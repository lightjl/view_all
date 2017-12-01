from datetime import *
from datetime import datetime,timedelta
import os
from lxml import etree
import requests
import calendar
import sendMail
import time
import datetime
import WorkInTime
import recMail
import logging
from multiprocessing import Process, Value
import threading
import imMail
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

#timeB = [['19:46', '23:00']]
logging.basicConfig(level=logging.CRITICAL, format='%(asctime)s - %(levelname)s -%(message)s')

class room:
    def __init__(self):
        self.timeB = [['9:00', '23:00']]
        self.wk = WorkInTime.WorkInTime(self.timeB, relaxTime=60*60)  # 周四

    def checkToday(self): 
        url = 'http://www.plateno.com/detail.html?innId=2990&checkInDate=1512144000000&checkOutDate=1512230400000&days=1'
        # url = 'http://www.plateno.com/detail.html?innId=2990&checkInDate=1512835200000&checkOutDate=1512921600000&days=1'   # test
        driver = webdriver.Firefox()
        # driver = webdriver.PhantomJS()
        driver.set_window_size(1024, 768)
        driver.get(url)
        
        content_field = driver.find_elements_by_xpath('//*[@id="roomBox"]/div')
        text = ''
        roomflag = False
        for each in content_field:
            each.send_keys(Keys.DOWN)
            fx = each.find_element_by_xpath('./div/div[2]/p').text
            # print(fx)
            time.sleep(1)
            # //*[@id="roomBox"]/div[1]/table/tbody/tr[3]/td[4]/div
            # //*[@id="roomBox"]/div[1]/table/tbody/tr[2]/td[4]/div
            # //*[@id="roomBox"]/div[2]/table/tbody/tr[2]/td[4]/div
            # //*[@id="roomBox"]/div[1]/table/tbody/tr[5]/td[4]/div
            # //*[@id="roomBox"]/div[2]/table/tbody/tr[5]/td[4]/div
            for i in range(2,5):
                zt = each.find_element_by_xpath('./table/tbody/tr[' + str(i) + ']/td[4]/div')
                # print(zt.get_attribute("class"))
                if (zt.get_attribute("class") != "reserve icon-house-btn indent-btn"):
                    if (fx != "商务套房" and fx != "浪漫优享房"):
                        roomflag = True
                        text+=(fx + "have house!\n")
                        break
        if roomflag:
            logging.critical(text)
            runFlag.value = False
            sendMail.sendMail('have room(s)', \
                'room:'+text+'\n'+url, 'ming188199@hotmail.com', 'hotmail', False)
        else:
            logging.critical("no room")
        driver.quit()

runFlag = Value('b', True)

def checkRunFlag():
    module_path = os.path.dirname(__file__)
    filename = module_path + '/room.pyrunable.txt'
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
    rm = room()
    # rm.checkToday()
    checkRun = threading.Thread(target=checkRunFlag, args=())
    checkRun.start()
    while runFlag.value:
        logging.critical('check room')
        rm.checkToday()
        
        relaxNow = threading.Thread(target=rm.wk.relax, args=(runFlag,'room'))
        relaxNow.start()
        relaxNow.join()