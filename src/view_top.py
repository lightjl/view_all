import tkinter
from tkinter.constants import LEFT
import logging
from multiprocessing import Process, Value
import os
import threading
from time import sleep
import pandas as pd
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s -%(message)s')


class SimpleGridApp(object):
    def __init__(self, root, iniPaths):
        self.paths = iniPaths
        self.pathsTexts = []
        self.path_sets = []
        self.proReStartButton = []
        self.proStartButton = []
        self.proStopButton = []
        self.texts = []
        self.process = []
        self.runable = []
        
        self.num_frame = tkinter.Frame()
        self.num = tkinter.Entry(self.num_frame, width=10)
        self.b = tkinter.Button(self.num_frame, text="setNum", width=4, command=self.numSet)
        self.startAllB = tkinter.Button(self.num_frame, text="startAll", width=8, command=self.startAll)
        self.stopAllB = tkinter.Button(self.num_frame, text="stopAll", width=8, command=self.stopAll)
        self.num.pack(side=LEFT)
        self.b.pack(side=LEFT)
        self.startAllB.pack(side=LEFT)
        self.stopAllB.pack(side=LEFT)
        self.num_frame.pack()
        
        self.numSet(len(iniPaths))
        
        for ith in range(len(iniPaths)):
            self.__resetText(ith)
        #self.startAll()
            
    def __resetText(self, ith):
        self.pathsTexts[ith].delete('1.0', "end-1c")
        self.pathsTexts[ith].insert(tkinter.INSERT, self.paths[ith])
        
    def __getPath(self, ith):
        return self.pathsTexts[ith].get('1.0', "end-1c")
    
    def __getFlagFileName(self, ith):
        if self.paths[ith][0] == '.':
            return module_path + self.paths[ith][1:] +'runable.txt'
        else:
            return self.paths[ith] +'runable.txt'
    
    def __setRun(self, ith):
        file_object = open(self.__getFlagFileName(ith), 'w')
        try:
            file_object.write('True')
        finally:
            file_object.close()
                
                
    def __setStop(self, ith):
            file_object = open(self.__getFlagFileName(ith), 'w')
            try:
                file_object.write('False')
            finally:
                file_object.close()
    
    def startAll(self):
        for ith in range(len(iniPaths)):
            self.process[ith] = threading.Thread(target=self.subProcess, args=(ith, self.runable[ith]))
            self.__resetText(ith)
            self.__setRun(ith)
            
            self.proStartButton[ith]['state']=tkinter.DISABLED
            self.proStopButton[ith]['state']=tkinter.NORMAL
            self.runable[ith].value = True
            self.process[ith].start()
        
    def stopAll(self):
        for ith in range(len(iniPaths)):
            self.proStartButton[ith]['state']=tkinter.NORMAL
            self.proStopButton[ith]['state']=tkinter.DISABLED
            self.__setStop(ith)
            self.runable[ith].value = False
    
    def __getFileName(self, ith):
        if self.paths[ith][0] == '.':
            return module_path + self.paths[ith][1:]
        else:
            return self.paths[ith]
        
    def subProcess(self, ith, alive):
        cmd = 'python3 ' + self.__getFileName(ith)
        logging.info('%i: %s start' % (ith, cmd))
        self.runState[ith] = True
        #os.system(cmd)
        #os.system(r'python C:\Users\jlgs-jz\git\gzr\zs888.py')    
        while alive.value:
            os.system(cmd)
            
        logging.info('%i: %s stoped' % (ith, cmd))
        self.runState[ith] = False
        
        
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
        self.runState = []
        for i in range(len_already, self.numProcess):
            process_frame = tkinter.Frame()
            #check_button = tkinter.Checkbutton(process_frame)
            prestr = tkinter.Button(process_frame, text="restart", command=self.onReStart(i))
            path = tkinter.Text(process_frame, height=1, width=20)
            path_set = tkinter.Button(process_frame, text="set", command=self.onSet(i))
            pstr = tkinter.Button(process_frame, text="start", command=self.onStart(i))
            pstp = tkinter.Button(process_frame, text="stop", command=self.onStop(i), state=tkinter.DISABLED)
            prestr.pack(side=LEFT)
            path.pack(side=LEFT)
            path_set.pack(side=LEFT)
            pstr.pack(side=LEFT)
            pstp.pack(side=LEFT)
            
            process_frame.pack()
            if iniNum == 0:
                self.paths.append('')
            
            self.proReStartButton.append(prestr)
            self.pathsTexts.append(path)
            self.proStartButton.append(pstr)
            self.proStopButton.append(pstp)
            self.runable.append(Value('b', False))
            self.runState.append(False)
            #self.pathsEntry[i]['text'] = self.paths[i]
            
            self.process.append(threading.Thread(target=self.subProcess, args=(i, self.runable[i])))
        logging.info(self.runable)
    
    def restart(self, ith):
        self.waitStop(ith)
        self.start(ith)
        
    def waitStop(self, ith):
        while self.runState[ith] == True:
            time.sleep(5)
        self.proStartButton[ith]['state']=tkinter.NORMAL
        self.proReStartButton[ith]['state']=tkinter.NORMAL
    
    def onReStart(self, ith):
        def reStart():
            self.proReStartButton[ith]['state']=tkinter.DISABLED
            # logging.info('%s restart ' % self.__getFileName(ith))
            self.stop(ith)
            self.proStartButton[ith]['state']=tkinter.DISABLED
            
            restartThread = threading.Thread(target=self.restart, args=(ith,))
            restartThread.start()
            
            #self.process[ith].start()
        return reStart
    
    def onSet(self, ith):
        def click():
            self.paths[ith] = (self.__getPath(ith))
            self.__resetText(ith)
            self.process[ith] = Process(target=self.subProcess, args=(ith,))
            logging.info('%i set, path = %s' % (ith, self.paths[ith]))
        return click
    
    def start(self, ith):
        # logging.info('%i start1' % ith)
        if len(self.__getPath(ith)) != 0:
            self.paths[ith] = (self.__getPath(ith))
        self.__resetText(ith)
        self.__setRun(ith)
        #self.process[ith] = Process(target=self.subProcess, args=(ith,))
        self.process[ith] = threading.Thread(target=self.subProcess, args=(ith, self.runable[ith]))
        #logging.info(self.runable)
        
        self.proStartButton[ith]['state']=tkinter.DISABLED
        self.proStopButton[ith]['state']=tkinter.NORMAL
        self.runable[ith].value = True
        self.process[ith].start()
    
    def onStart(self, ith):
        def start():
            #logging.info('%s start' % self.__getFileName(ith))
            if len(self.__getPath(ith)) != 0:
                self.paths[ith] = (self.__getPath(ith))
            self.__resetText(ith)
            self.__setRun(ith)
            #self.process[ith] = Process(target=self.subProcess, args=(ith,))
            self.process[ith] = threading.Thread(target=self.subProcess, args=(ith, self.runable[ith]))
            #logging.info(self.runable)
            
            self.proStartButton[ith]['state']=tkinter.DISABLED
            self.proStopButton[ith]['state']=tkinter.NORMAL
            self.runable[ith].value = True
            self.process[ith].start()
            #self.process[ith].start()
        return start
    
    def stop(self, ith):
        logging.info('%s stoping' % self.__getFileName(ith))
        self.proStartButton[ith]['state']=tkinter.NORMAL
        self.proStopButton[ith]['state']=tkinter.DISABLED
        self.__setStop(ith)
        self.runable[ith].value = False
        
    def onStop(self, ith):
        def stop():
            logging.info('%s stoping' % self.__getFileName(ith))
            waitStopThread = threading.Thread(target=self.waitStop, args=(ith,))
            waitStopThread.start()
            self.proStopButton[ith]['state']=tkinter.DISABLED
            self.proReStartButton[ith]['state']=tkinter.DISABLED
            self.__setStop(ith)
            self.runable[ith].value = False
        return stop
    
        
if __name__ == '__main__':
    module_path = os.path.dirname(__file__)
    filename = module_path + '/ini.csv'
    iniPathsPd = pd.read_csv(filename).values
    #print(iniPathsPd)
    iniPaths = []
    for row in iniPathsPd:
        #print(row[1])
        if (row[0] != 0):
            continue
        iniPaths.append(row[1])
    
    top = tkinter.Tk()
    
    test = SimpleGridApp(top, iniPaths)
    tkinter.mainloop()
    






            
            