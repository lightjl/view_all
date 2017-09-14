import tkinter
from tkinter.constants import LEFT
import logging
from multiprocessing import Process, Value
import os
import threading
from time import sleep

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s -%(message)s')


class SimpleGridApp(object):
    def __init__(self, root):
        self.paths = []
        self.pathsEntry = []
        self.path_sets = []
        self.proStartButton = []
        self.proStopButton = []
        self.process = []
        self.runable = []
        
        self.num_frame = tkinter.Frame()
        self.num = tkinter.Entry(self.num_frame)
        self.b = tkinter.Button(self.num_frame, text="get", width=10, command=self.numSet)
        self.num.pack(side=LEFT)
        self.b.pack(side=LEFT)
        self.num_frame.pack()
        pass
    
    def subProcess(self, ith, alive):
        cmd = 'python ' + self.paths[ith]
        logging.info('%i: %s start' % (ith, cmd))
        #os.system(cmd)
        #os.system(r'python C:\Users\jlgs-jz\git\gzr\zs888.py')    
        while alive.value:
            os.system(cmd)
            
        logging.info('%i: %s stoped' % (ith, cmd))
        
        
    def numSet(self):
        self.numProcess = int(self.num.get())
        len_already = len(self.paths)
        if (len_already >= self.numProcess):
            return
        for i in range(len_already, self.numProcess):
            process_frame = tkinter.Frame()
            #check_button = tkinter.Checkbutton(process_frame)
            path = tkinter.Entry(process_frame)
            path_set = tkinter.Button(process_frame, text="set", command=self.onSet(i))
            pstr = tkinter.Button(process_frame, text="start", command=self.onStart(i))
            pstp = tkinter.Button(process_frame, text="stop", command=self.onStop(i), state=tkinter.DISABLED)
            path.pack(side=LEFT)
            path_set.pack(side=LEFT)
            pstr.pack(side=LEFT)
            pstp.pack(side=LEFT)
            
            process_frame.pack()
            self.paths.append('')
            self.pathsEntry.append(path)
            self.proStartButton.append(pstr)
            self.proStopButton.append(pstp)
            self.runable.append(Value('b', False))
            
            #p = Process(target=self.subProcess, args=(i,))
            #p = 
            #p.start()
            #p = threading.Thread(target=self.subProcess, args=(i,))
            #p._stop()
            #self.process.append(threading.Thread(target=self.subProcess, args=(i,)))
            self.process.append(threading.Thread(target=self.subProcess, args=(i, self.runable[i])))
            #button = tkinter.Button(root, text=k, width=5, relief='raised',
            #                   command=onclick(k))
            #button.grid(row=i, column=0)
            #self.keyboardButtons.append(button)
        logging.info(self.runable)
    
    def onSet(self, ith):
        def click():
            self.paths[ith] = (self.pathsEntry[ith].get())
            self.process[ith] = Process(target=self.subProcess, args=(ith,))
            logging.info('%i set, path = %s' % (ith, self.paths[ith]))
        return click
    
    def onStart(self, ith):
        def start():
            logging.info('%i start1' % ith)
            self.paths[ith] = (self.pathsEntry[ith].get())
            #self.process[ith] = Process(target=self.subProcess, args=(ith,))
            self.process[ith] = threading.Thread(target=self.subProcess, args=(ith, self.runable[ith]))
            logging.info(self.runable)
            
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
    top = tkinter.Tk()
    
    test = SimpleGridApp(top)
    tkinter.mainloop()






            
            