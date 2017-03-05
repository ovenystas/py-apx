import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import apx
import time

class MyDataListener(apx.DataListener):
   def on_connect(self):
      print("MyDataListener.on_connect")
   def on_data(self, port, data):
      print("MyDataListener.on_data")



node = apx.Node('Simulator')
node.dataTypes.append(apx.DataType('InactiveActive_T','C(0,3)'))
node.providePorts.append(apx.ProvidePort('VehicleSpeed','S','=65535'))
node.providePorts.append(apx.ProvidePort('MainBeam','T[0]','=3'))
node.providePorts.append(apx.ProvidePort('FuelLevel','C'))
node.providePorts.append(apx.ProvidePort('ParkBrakeActive','T[0]','=3'))
node.requirePorts.append(apx.RequirePort('RheostatLevelRqst','C','=255'))
     
client = apx.Client(node)
client.set_listener(MyDataListener())
if client.connectTcp('localhost', 5000):
   while True:
      try:         
         time.sleep(10)
      except (KeyboardInterrupt, SystemExit):
         break
client.stop()
sys.exit()   
