from lxml import etree
import requests
import sendMail
import recMail
import time
import WorkInTime
import logging
from selenium import webdriver
import maiJia
from pydoc import browse
from multiprocessing import Process, Value
import threading
import os
import imMail

#timeB = [['19:46', '23:00']]

def findFood(maiJiaList):
    for maiJia in maiJiaList:
        maiJia.findFood(46)

def gundong(browser):
    for i in range(10):
        js="document.documentElement.scrollTop=1000000"
        browser.execute_script(js)
        time.sleep(1)
                    
def pinpai(browser):
    # '/html/body/div/ul/section[1]/div[2]/section[1]/h3/span'
    # '/html/body/div/ul/section[2]/div[2]/section[1]/h3/span'
    dians = browser.find_elements_by_xpath('/html/body/div/ul/section')
    diansList = []
    for dian in dians:
        name = dian.find_element_by_xpath('./div[2]/section[1]/h3/span').text
        diansList.append(name)
    return diansList
    
def findMaijia():
    browser = webdriver.Firefox()
    # browser = webdriver.PhantomJS()
    # 礼顿
    url = 'https://h5.ele.me/msite/food/#geohash=ws0ed952uqk9&#target={"category_schema":%20{"category_name":%20"\u7f8e\u98df",%20"complex_category_ids":%20[207,%20220,%20233,%20260],%20"is_show_all_category":%20false},%20"restaurant_category_id":%20[209,%20211,%20212,%20213,%20214,%20215,%20216,%20217,%20218,%20219,%20221,%20222,%20223,%20224,%20225,%20226,%20227,%20228,%20229,%20230,%20231,%20232,%20234,%20235,%20236,%20237,%20238,%20263,%20264,%20265,%20266,%20267,%20268,%20269]}&target_name=美食&animation_type=1&banner_type=0&business_flag=1&color_type=1&entry_id=15&search_source=1'
    # 国门
    url = 'https://h5.ele.me/msite/food/#geohash=ws0ed8snyj8u&#target={"category_schema": {"category_name": "\u7f8e\u98df", "complex_category_ids": [207, 220, 233, 260], "is_show_all_category": false}, "restaurant_category_id": [209, 211, 212, 213, 214, 215, 216, 217, 218, 219, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 234, 235, 236, 237, 238, 263, 264, 265, 266, 267, 268, 269]}&target_name=美食&animation_type=1&banner_type=0&business_flag=1&color_type=1&entry_id=15&search_source=1'
    browser.get(url)
    # 品牌
    time.sleep(2)
    browser.find_element_by_xpath('/html/body/div/div[1]/div/aside/div/a[3]').click()
    time.sleep(2)
    # 品牌商家
    browser.find_element_by_xpath('/html/body/div/div[1]/div/aside/section[3]/div[1]/dl[4]/dd[1]').click()
    browser.maximize_window()
    time.sleep(2)
    browser.find_element_by_xpath('/html/body/div/div[1]/div/aside/section[3]/div[2]/a[2]').click()
    time.sleep(6)
    # 晚餐
    '''
    browser.find_element_by_xpath('/html/body/div/div[1]/div/aside/div/a[1]').click()
    time.sleep(6)
    browser.find_element_by_xpath('/html/body/div/div[1]/div/aside/section[1]/div/ul[1]/li[15]').click()
    time.sleep(2)
    browser.find_element_by_xpath('/html/body/div/div[1]/div/aside/section[1]/div/ul[2]/li[1]').click()
    time.sleep(4)
    '''
    
    gundong(browser)
    diansList = pinpai(browser)
    # 礼顿
    url = 'https://www.ele.me/place/ws0ed952uqk?latitude=23.12089&longitude=113.31764'
    # 国门
    url = 'https://www.ele.me/place/ws0ed8snyj8?latitude=23.11917&longitude=113.31874'
    browser.get(url)
    time.sleep(4)
    browser.find_element_by_xpath('/html/body/div[4]/div[3]/div[1]/div/a[15]').click()

    
    #print(html.text)
    # /html/body/div[4]/div[3]/div[2]/div[1]/a[1]/div[2]/div[4]/i
    # /html/body/div[4]/div[3]/div[2]/div[1]/a[3]/div[2]/div[4]/i[2]
    
    # /html/body/div[4]/div[3]/div[2]/div[1]/a[1] /div[2]/div[1] 店名
    
    # /html/body/div[4]/div[3]/div[2]/div[1]/a[6]
    gundong(browser)
    time.sleep(1)
    # print(diansList)
    
    maijias = browser.find_elements_by_xpath('/html/body/div[4]/div[3]/div[2]/div[1]/a')
    maijiaList = []
    for maijia in maijias:
        link = (maijia.get_attribute("href"))
        name = (maijia.find_element_by_xpath('./div[2]/div[1]').text)
        if name not in diansList:
            continue
        tzs = maijia.find_elements_by_xpath('./div[2]/div[4]/i')
        mj = maiJia.maiJia(name, link)
        maijiaList.append(mj)
    browser.quit()
    findFood(maijiaList)
    
runFlag = Value('b', True)

def checkRunFlag():
    module_path = os.path.dirname(__file__)
    filename = module_path + '/waimai.pyrunable.txt'
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
    timeTrade = [['16:00', '16:10']]
    workTime = WorkInTime.WorkInTime(timeTrade, weekday='0,1,2,3,4')
    checkRun = threading.Thread(target=checkRunFlag, args=())
    checkRun.start()
    while runFlag.value:
        findMaijia()
        imMail.delMail(imMail.Ebox(), 'Sent')
        # mr.delSent()    #删除已发送邮件
        relaxNow = threading.Thread(target=workTime.relax, args=(runFlag,'Mtime'))
        relaxNow.start()
        relaxNow.join()
