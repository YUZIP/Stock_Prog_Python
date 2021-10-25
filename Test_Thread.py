from threading import Thread
import time

def delA():
    for i in range(len(a)):
        del a[0]

class ThreadCalculate(Thread):
    def __init__(self,cond):
        Thread.__init__(self)
        self.Cond = cond
        self.Count = 0
        self.running = True

        self.start()
    def __del__(self):
        del self.Cond

    def run(self):
        while(self.running):
            if (self.Count > self.Cond):
                break
            self.Count += 0.5
            time.sleep(0.5)
        self.running = False
        return self.Cond

a = [ThreadCalculate(2),ThreadCalculate(4),ThreadCalculate(3)]
while (a[0].running or a[1].running or a[2].running):
    print('Still Waiting',a[0].Count,a[1].Count,a[2].Count)
    time.sleep(0.1)

print('isFinish',a)
b = []

for i in a:
    b.append(i.Count)
print('B', b)

for i in a:
    i.running = True
    i.start()

while (a[0].running or a[1].running or a[2].running):
    print('Still Waiting',a[0].Count,a[1].Count,a[2].Count)
    time.sleep(0.1)

print('A',a)
print('B',b)


