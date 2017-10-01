import xs
import os
import logging
import threading
import pandas as pd
import time
INTERPRETER = "python"
from multiprocessing import Process, Value
import threading

#timeB = [['19:46', '23:00']]
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s -%(message)s')


#checkToday888(jdtm)


def followBook(ith, alive):
    logging.info('正在追' + xss[ith].name)

    while  alive.value:
        xss[ith].checkToday()
        xss[ith].relax(alive)


runFlag = Value('b', True)

def checkRunFlag():
    module_path = os.path.dirname(__file__)
    filename = module_path + '/zs888.pyrunable.txt'
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
    '''
    list = []
    for xsInfo in xss:
        list.append([xsInfo.name, xsInfo.getUrl(), xsInfo.timeB])
    columns = ['name', 'url', 'timeB']
    xsPd = pd.DataFrame(data=list, columns=columns)
    xsPd.to_csv('./ini.csv')
    '''
    module_path = os.path.dirname(__file__)
    filename = module_path + '/ini.csv'
    xsPd = pd.read_csv(filename).values
    #logging.info(xsPd)
    
    xss = []
    # 检查是否要运行
    checkRun = threading.Thread(target=checkRunFlag, args=())
    checkRun.start()
    
    for ith in xsPd:
        listtmp = eval(ith[3])
        xss.append(xs.xs(ith[1], ith[2], listtmp))
    
    for i in range(len(xss)):
        p = threading.Thread(target=followBook, args=(i, runFlag))
        #p = Process(target=followBook, args=(i,))
        p.start()

