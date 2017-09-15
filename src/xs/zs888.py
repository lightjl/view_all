import xs
import os
import logging
import threading
import pandas as pd
INTERPRETER = "python"

#timeB = [['19:46', '23:00']]
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s -%(message)s')


#checkToday888(jdtm)


def followBook(ith, module_path):
    logging.info('正在追' + xss[ith].name)
    filename = module_path + '/zs888.pyrunable.txt'
    file_object = open(filename, 'r')
    try:
        flag_run = file_object.read()
    finally:
        file_object.close()
        
    while flag_run == 'True':
        xss[ith].checkToday()
        xss[ith].relax()
        file_object = open(filename, 'r')
        try:
            flag_run = file_object.read()
        finally:
            file_object.close()


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
    
    for ith in xsPd:
        listtmp = eval(ith[3])
        xss.append(xs.xs(ith[1], ith[2], listtmp))
    
    for i in range(len(xss)):
        p = threading.Thread(target=followBook, args=(i,module_path))
        #p = Process(target=followBook, args=(i,))
        p.start()
'''

txt = open('D:/xs/蛊真人 请假一天.txt', encoding='utf-8')
all_the_text = txt.read( )
print(len(all_the_text))
print('end')
'''

'''
while True:
    timeWork.relax()
    checkToday(timeWork)
'''

'''
html = requests.get(url)
selector = etree.HTML(html.text)
print(selector.xpath('//div[@id]'))
'''