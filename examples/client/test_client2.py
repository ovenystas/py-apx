import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import apx
import time

@apx.DataListener.register
class MyDataListener(apx.DataListener):
    global client
    def on_data(self, port, value):
        print("%s: %s"%(port.name,str(value)))
        if port.name=='TestSignal1':
            client.write_port('TestSignal2', value) #just return whatever is on TestSignal1 multiplied by 2      
         
if __name__ == '__main__':

    node = apx.Node('TestNode2')
    node.append(apx.RequirePort('TestSignal1','S'))
    node.append(apx.ProvidePort('TestSignal2','S'))
     
    with apx.Client(node) as client:
        client.set_listener(MyDataListener())        
        if client.connect_tcp('localhost', 5000):
            while True:
                try:
                   time.sleep(1)
                except (KeyboardInterrupt, SystemExit):
                    break