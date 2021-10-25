from threading import Thread
from multiprocessing import Process
import time

def delA():
    for i in range(len(a)):
        del a[0]

class ThreadCalculate(Process):
    def __init__(self,cond):
        Process.__init__(self)
        self.Cond = cond
        self.Count = 0
        self.running = True
        print("Getin Setting",self.Cond)

        #self.start()
    #def __del__(self):
    #    del self.Cond
    def getCond(self):
        return self.Count

    def doSomeThing(self):
        while (self.running):
            if (self.Count > self.Cond):
                break
            self.Count += 0.5
            time.sleep(0.5)
        self.running = False
        return self.Cond
    def run(self):
        self.running = True

        while (self.running):
            if (self.Count > self.Cond):
                print("Getin Stoped", self.Cond)
                break
            print("Getin Process", self.Count)
            self.Count += 0.5
            time.sleep(0.5)

        self.running = False
        return self.Cond
        #return self.doSomeThing()

if __name__ == '__main__':

    a = [ThreadCalculate(2),ThreadCalculate(4),ThreadCalculate(3)]

    for i in a:
        i.start()

    while (a[0].is_alive() or a[1].is_alive() or a[2].is_alive()):
        print('Still Waiting',a[0].Count,a[1].Count,a[2].Count)
        time.sleep(0.1)

    print('isFinish',a)
    b = []
    print('Still ', a[0].getCond(), a[1].getCond(), a[2].getCond())
    for i in a:
        b.append(i.Count)
    print('B', b)
    '''
    for i in a:
        i.running = True
        i.start()
    
    while (a[0].running or a[1].running or a[2].running):
        print('Still Waiting',a[0].Count,a[1].Count,a[2].Count)
        time.sleep(0.1)
    
    print('A',a)
    print('B',b)
    
    
    '''