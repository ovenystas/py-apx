import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import apx
import time

node = apx.Node('TestNode')
node.dataTypes.append(apx.DataType('InactiveActive_T','C(0,3)'))
node.requirePorts.append(apx.RequirePort('VehicleSpeed','S','=65535'))
node.requirePorts.append(apx.RequirePort('MainBeam','T[0]','=3'))
node.requirePorts.append(apx.RequirePort('FuelLevel','C'))
node.requirePorts.append(apx.RequirePort('ParkBrakeActive','T[0]','=3'))
node.providePorts.append(apx.ProvidePort('RheostatLevelRqst','C','=255'))
     
client = apx.Client(node)
if client.connectTcp('localhost', 5000):
   while True:
      try:
         time.sleep(500)
      except (KeyboardInterrupt, SystemExit):
         break
client.stop()
sys.exit()     
