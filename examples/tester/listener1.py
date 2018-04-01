#!/usr/bin/env python3
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import apx
import time

ref_time = time.time()

@apx.DataListener.register
class MyDataListener(apx.DataListener):
    global ref_time
    def on_data(self, port, data):
        delta_time = time.time() - ref_time
        print("%.3f: %s=%s"%(delta_time, port.name, str(data)))

if __name__ == '__main__':
    apx_text = """APX/1.2
N"Listener"
T"VehicleSpeed_T"S
T"EngineSpeed_T"S
R"VehicleSpeed"T["VehicleSpeed_T"]:=65535
R"EngineSpeed"T["EngineSpeed_T"]:=65535
"""
       
    with apx.Client(apx_text) as client:
        client.set_listener(MyDataListener())        
        if client.connect_tcp('localhost', 5000):
            while True:
                try:
                    time.sleep(1)                    
                except (KeyboardInterrupt, SystemExit):
                    break
