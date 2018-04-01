#!/usr/bin/env python3
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import apx

if __name__ == "__main__":    
    apx_text = """APX/1.2
N"Tester"
T"VehicleSpeed_T"S
T"EngineSpeed_T"S
P"VehicleSpeed"T["VehicleSpeed_T"]:=65535
P"EngineSpeed"T["EngineSpeed_T"]:=65535
"""
    tester = apx.Tester(apx_text)
    tester.connect_tcp('localhost', 5000)
    tester.set('VehicleSpeed', 0)
    tester.set('EngineSpeed', 0)
    tester.sleep(50)
    tester.ramp('VehicleSpeed', 65535, 1000, 20)
    tester.ramp('EngineSpeed', 65535, 1000, 20)
    tester.end()
        