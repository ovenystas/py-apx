#!/bin/env python3
import autosar
import apx
import time
import threading

@apx.DataListener.register
class MyApxWorker(apx.DataListener):
    def __init__(self, client):
        self.client = client
        self.lock=threading.Lock()
        client.set_listener(self) #register on_data method to be called when new data arrives
        self.PTestSignal1=0
        self.PTestSignal2=0
        self.PTestSignal3=0
        self.PTestSignal4=[0,0,0,0]
        self.PTestSignal5={'Name':"Hello", 'Id':0}
        
    def on_data(self, port, data):
        pass
        #print(port.name)        
        #print("%s: %s"%(port.name, str(data)))
    
    def connect(self):
        return self.client.connect_tcp('localhost', 5000)
    
    def run(self):
        self.lock.acquire()
        self.PTestSignal1 = (self.PTestSignal1 + 1) & 0xFFFF
        self.PTestSignal2 = (self.PTestSignal2 + 1) & 0xFFFF
        self.PTestSignal3 = (self.PTestSignal3 + 1) & 0xFFFF        
        self.lock.release()
        self.client.write_port('PTestSignal1', self.PTestSignal1)
        self.client.write_port('PTestSignal2', self.PTestSignal2)
        self.client.write_port('PTestSignal3', self.PTestSignal3)        
    
    def stop(self):
        self.client.stop()
    

if __name__ == '__main__':    
    node = apx.Node('StressNode1')
    node.append(apx.ProvidePort('PTestSignal1','S'))
    node.append(apx.ProvidePort('PTestSignal2','S'))
    node.append(apx.ProvidePort('PTestSignal3','S'))
    node.append(apx.ProvidePort('PTestSignal4','C[4]'))
    node.append(apx.ProvidePort('PTestSignal5','{"Name"a[10]"Id"S}'))
    node.append(apx.RequirePort('QTestSignal1','S'))
    node.append(apx.RequirePort('QTestSignal2','S'))
    node.append(apx.RequirePort('QTestSignal3','S'))
    node.append(apx.RequirePort('QTestSignal4','S[4]'))
    node.append(apx.RequirePort('QTestSignal5','{"Name"a[10]"Id"S}'))
        
    with apx.Client(node) as client:
        worker = MyApxWorker(client)
        if worker.connect():
            while True:
                try:
                    time.sleep(0.005)
                    worker.run()
                except (KeyboardInterrupt, SystemExit):
                    break
            worker.stop()

