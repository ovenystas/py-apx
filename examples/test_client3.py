import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import apx
import time

@apx.DataListener.register
class MyDataListener(apx.DataListener):
   def on_data(self, port_id, port_name, data):
      global value
      global client
      print("%s: %s"%(port_name, str(data)))
      if port_name=='TestSignal2' and value is not None:
         value = (value + 1) & 0xFFFF #wraparound to zero after 65535
         client.write_port('TestSignal1', value)

if __name__ == '__main__':
   node = apx.Node('TestNode1')
   node.append(apx.ProvidePort('TestSignal1','S'))
   node.append(apx.RequirePort('TestSignal2','S'))   
   value=1
   client = apx.Client(node)
   client.set_listener(MyDataListener())
   client.write_port('TestSignal1',value)
   if client.connectTcp('localhost', 5000):
      while True:
         try:         
            time.sleep(10)            
            break
         except (KeyboardInterrupt, SystemExit):
            break
   value=None
   time.sleep(0.2)
   client.stop()
   
