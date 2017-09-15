import tkinter
from tkinter.constants import LEFT
import logging
from multiprocessing import Process, Value
import os
import threading
from time import sleep
import pandas as pd

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s -%(message)s')


class SimpleGridApp(object):
    def __init__(self, root, iniPaths):
        self.paths = iniPaths
        self.pathsTexts = []
        self.path_sets = []
        self.proStartButton = []
        self.proStopButton = []
        self.texts = []
        self.process = []
        self.runable = []
        
        self.num_frame = tkinter.Frame()
        self.num = tkinter.Entry(self.num_frame)
        self.b = tkinter.Button(self.num_frame, text="setNum", width=10, command=self.numSet)
        self.num.pack(side=LEFT)
        self.b.pack(side=LEFT)
        self.num_frame.pack()
        
        self.numSet(len(iniPaths))
        
        self.startAll()
            
    def __resetText(self, ith):
        self.pathsTexts[ith].delete('1.0', "end-1c")
        self.pathsTexts[ith].insert(tkinter.INSERT, self.paths[ith])
        
    def __getPath(self, ith):
        return self.pathsTexts[ith].get('1.0', "end-1c")
    
    def startAll(self):
        for ith in range(len(iniPaths)):
            self.process[ith] = threading.Thread(target=self.subProcess, args=(ith, self.runable[ith]))
            self.__resetText(ith)
            
            self.proStartButton[ith]['state']=tkinter.DISABLED
            self.proStopButton[ith]['state']=tkinter.NORMAL
            self.runable[ith].value = True
            self.process[ith].start()
        
    def stopAll(self):
        for ith in range(len(iniPaths)):
            self.proStartButton[ith]['state']=tkinter.NORMAL
            self.proStopButton[ith]['state']=tkinter.DISABLED
            self.runable[ith].value = False
    
    def subProcess(self, ith, alive):
        cmd = 'python ' + self.paths[ith]
        logging.info('%i: %s start' % (ith, cmd))
        #os.system(cmd)
        #os.system(r'python C:\Users\jlgs-jz\git\gzr\zs888.py')    
        while alive.value:
            os.system(cmd)
            
        logging.info('%i: %s stoped' % (ith, cmd))
        
        
    def numSet(self, iniNum = 0):
        len_already = 0
        if iniNum == 0:
            self.numProcess = int(self.num.get())
            len_already = len(self.paths)
        else:
            self.numProcess = iniNum
            len_already = 0
            
        
        if (len_already >= self.numProcess):
            return
        logging.info('ini %i' % (iniNum))
        for i in range(len_already, self.numProcess):
            process_frame = tkinter.Frame()
            #check_button = tkinter.Checkbutton(process_frame)
            path = tkinter.Text(process_frame, height=1, width=20)
            path_set = tkinter.Button(process_frame, text="set", command=self.onSet(i))
            pstr = tkinter.Button(process_frame, text="start", command=self.onStart(i))
            pstp = tkinter.Button(process_frame, text="stop", command=self.onStop(i), state=tkinter.DISABLED)
            path.pack(side=LEFT)
            path_set.pack(side=LEFT)
            pstr.pack(side=LEFT)
            pstp.pack(side=LEFT)
            
            process_frame.pack()
            if iniNum == 0:
                self.paths.append('')
                
            self.pathsTexts.append(path)
            self.proStartButton.append(pstr)
            self.proStopButton.append(pstp)
            self.runable.append(Value('b', False))
            #self.pathsEntry[i]['text'] = self.paths[i]
            
            self.process.append(threading.Thread(target=self.subProcess, args=(i, self.runable[i])))
        logging.info(self.runable)
    
    def onSet(self, ith):
        def click():
            self.paths[ith] = (self.__getPath(ith))
            self.__resetText(ith)
            self.process[ith] = Process(target=self.subProcess, args=(ith,))
            logging.info('%i set, path = %s' % (ith, self.paths[ith]))
        return click
    
    
    def onStart(self, ith):
        def start():
            logging.info('%i start1' % ith)
            if len(self.__getPath(ith)) != 0:
                self.paths[ith] = (self.__getPath(ith))
            self.__resetText(ith)
            #self.process[ith] = Process(target=self.subProcess, args=(ith,))
            self.process[ith] = threading.Thread(target=self.subProcess, args=(ith, self.runable[ith]))
            #logging.info(self.runable)
            
            self.proStartButton[ith]['state']=tkinter.DISABLED
            self.proStopButton[ith]['state']=tkinter.NORMAL
            self.runable[ith].value = True
            self.process[ith].start()
            #self.process[ith].start()
        return start
    
    def onStop(self, ith):
        def stop():
            self.proStartButton[ith]['state']=tkinter.NORMAL
            self.proStopButton[ith]['state']=tkinter.DISABLED
            #self.process[ith].terminate()
            self.runable[ith].value = False
        return stop
    
        
if __name__ == '__main__':
    module_path = os.path.dirname(__file__)
    filename = module_path + '/ini.csv'
    iniPathsPd = pd.read_csv(filename).values
    #print(iniPathsPd)
    iniPaths = []
    for row in iniPathsPd:
        print(row[1])
        iniPaths.append(row[1])
    
    top = tkinter.Tk()
    
    test = SimpleGridApp(top, iniPaths)
    tkinter.mainloop()
    






            
            