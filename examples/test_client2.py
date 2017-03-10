import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import apx
import time

@apx.DataListener.register
class MyDataListener(apx.DataListener):
   global client
   def on_data(self, port_id, port_name, value):
      print("%s: %s"%(port_name,str(value)))
      if port_name=='TestSignal1':
         client.write_port('TestSignal2', value) #just return whatever is on TestSignal1 multiplied by 2      
         
      
node = apx.Node('TestNode2')
node.append(apx.RequirePort('TestSignal1','S'))
node.append(apx.ProvidePort('TestSignal2','S'))
     
client = apx.Client(node)
client.set_listener(MyDataListener())
if client.connectTcp('localhost', 5000):
   while True:
      try:
         time.sleep(1)
      except (KeyboardInterrupt, SystemExit):
         break
client.stop()
sys.exit()     
