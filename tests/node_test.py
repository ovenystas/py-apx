import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import apx
import unittest
import remotefile
import autosar

class TestNode(unittest.TestCase):
 
   def setUp(self):
      pass
 
   def test_autosar_ports(self):
      ws=autosar.workspace()
      dataTypes=ws.createPackage('DataType', role='DataType')
      dataTypes.createSubPackage('DataTypeSemantics', role='CompuMethod')
      dataTypes.createSubPackage('DataTypeUnits', role='Unit')

      dataTypes.createIntegerDataType('EngineSpeed_T', min=0, max=65535, offset=0, scaling=1/8, unit='rpm')
      dataTypes.createIntegerDataType('VehicleSpeed_T', min=0, max=65535, offset=0, scaling=1/64,unit='kph')
      dataTypes.createIntegerDataType('Percent_T', min=0, max=255, offset=0, scaling=0.4, unit='Percent')
      dataTypes.createIntegerDataType('CoolantTemp_T', min=0, max=255, offset=-40, scaling=0.5, unit='DegreeC')
      dataTypes.createIntegerDataType('InactiveActive_T', valueTable=[
           'InactiveActive_Inactive',       #0
           'InactiveActive_Active',         #1
           'InactiveActive_Error',          #2
           'InactiveActive_NotAvailable'])  #3
      dataTypes.createIntegerDataType('OnOff_T', valueTable=[
          "OnOff_Off",                      #0
          "OnOff_On",                       #1
          "OnOff_Error",                    #2
          "OnOff_NotAvailable"])            #3
      package = ws.createPackage('Constant', role='Constant')

      package.createConstant('EngineSpeed_IV', 'EngineSpeed_T', 65535)
      package.createConstant('VehicleSpeed_IV', 'VehicleSpeed_T', 65535)
      package.createConstant('FuelLevel_IV', 'Percent_T', 255)
      package.createConstant('CoolantTemp_IV', 'CoolantTemp_T', 255)
      package.createConstant('ParkBrakeState_IV', 'InactiveActive_T', 3) #3=NotAvailable
      package.createConstant('MainBeamState_IV', 'OnOff_T', 3) #3=NotAvailable
      package=ws.createPackage('PortInterface', role='PortInterface')

      package.createSenderReceiverInterface('EngineSpeed_I', autosar.DataElement('EngineSpeed','/DataType/EngineSpeed_T'))
      package.createSenderReceiverInterface('VehicleSpeed_I', autosar.DataElement('VehicleSpeed','/DataType/VehicleSpeed_T'))
      package.createSenderReceiverInterface('FuelLevel_I', autosar.DataElement('FuelLevel','/DataType/Percent_T'))
      package.createSenderReceiverInterface('CoolantTemp_I', autosar.DataElement('CoolantTemp','/DataType/CoolantTemp_T'))
      package.createSenderReceiverInterface('ParkBrakeState_I', autosar.DataElement('InactiveActive','/DataType/InactiveActive_T'))
      package.createSenderReceiverInterface('MainBeamState_I', autosar.DataElement('OnOff','/DataType/OnOff_T'))
      
      packate = ws.createPackage('ComponentType', role='ComponentType')
      package=ws.createPackage('ComponentType', role='ComponentType')
      swc=package.createApplicationSoftwareComponent('TestSWC')
      swc.createProvidePort('EngineSpeed', 'EngineSpeed_I', initValueRef='EngineSpeed_IV')
      swc.createProvidePort('VehicleSpeed', 'VehicleSpeed_I', initValueRef='VehicleSpeed_IV')
      swc.createRequirePort('FuelLevel', 'FuelLevel_I', initValueRef='FuelLevel_IV')
      swc.createRequirePort('CoolantTemp', 'CoolantTemp_I', initValueRef='CoolantTemp_IV')
      swc.createRequirePort('ParkBrakeState', 'ParkBrakeState_I', initValueRef='ParkBrakeState_IV')
      swc.createRequirePort('MainBeamState', 'MainBeamState_I', initValueRef='MainBeamState_IV')
      
      apx_node = apx.Node(swc.name)
      apx_node.import_autosar_swc(swc)
      
      lines=apx_node.lines()
      self.assertEqual(len(lines), 13)
      self.assertEqual(lines[0], 'N"TestSWC"')
      self.assertEqual(lines[1], 'T"EngineSpeed_T"S')
      self.assertEqual(lines[2], 'T"VehicleSpeed_T"S')
      self.assertEqual(lines[3], 'T"Percent_T"C')
      self.assertEqual(lines[4], 'T"CoolantTemp_T"C')
      self.assertEqual(lines[5], 'T"InactiveActive_T"C(0,3):VT("InactiveActive_Inactive","InactiveActive_Active","InactiveActive_Error","InactiveActive_NotAvailable")')
      self.assertEqual(lines[6], 'T"OnOff_T"C(0,3):VT("OnOff_Off","OnOff_On","OnOff_Error","OnOff_NotAvailable")')            
      self.assertEqual(lines[7], 'P"EngineSpeed"T[0]:=0xFFFF')
      self.assertEqual(lines[8], 'P"VehicleSpeed"T[1]:=0xFFFF')
      self.assertEqual(lines[9], 'R"FuelLevel"T[2]:=255')
      self.assertEqual(lines[10], 'R"CoolantTemp"T[3]:=255')
      self.assertEqual(lines[11], 'R"ParkBrakeState"T[4]:=3')
      self.assertEqual(lines[12], 'R"MainBeamState"T[5]:=3')
      

   def test_raw_ports(self):
      node = apx.Node('TestSWC')
      node.dataTypes.append(apx.DataType('InactiveActive_T','C(0,3)'))      
      node.providePorts.append(apx.ProvidePort('VehicleSpeed','S','=65535'))
      node.providePorts.append(apx.ProvidePort('MainBeam','T[0]','=3'))
      node.providePorts.append(apx.ProvidePort('FuelLevel','C'))
      node.providePorts.append(apx.ProvidePort('ParkBrakeActive','T[0]','=3'))
      node.requirePorts.append(apx.RequirePort('RheostatLevelRqst','C','=255'))
      node.requirePorts.append(apx.RequirePort('StrSignal','a[4]','=""'))
      node.requirePorts.append(apx.RequirePort('RecordSignal','{"Name"a[8]"Id"L"Data"S[3]}','={"",0xFFFFFFFF,{0,0,0}}'))
      lines=node.lines()
      self.assertEqual(len(lines), 9)
      self.assertEqual(lines[0],'N"TestSWC"')
      self.assertEqual(lines[1],'T"InactiveActive_T"C(0,3)')
      self.assertEqual(lines[2],'P"VehicleSpeed"S:=65535')
      self.assertEqual(lines[3],'P"MainBeam"T[0]:=3')
      self.assertEqual(lines[4],'P"FuelLevel"C')
      self.assertEqual(lines[5],'P"ParkBrakeActive"T[0]:=3')
      self.assertEqual(lines[6],'R"RheostatLevelRqst"C:=255')
      self.assertEqual(lines[7],'R"StrSignal"a[4]:=""')
      self.assertEqual(lines[8],'R"RecordSignal"{"Name"a[8]"Id"L"Data"S[3]}:={"",0xFFFFFFFF,{0,0,0}}')
      self.assertEqual(node.providePorts[0].dsg.calcStructFmtStr(node.dataTypes), '<H') #unsigned short
      self.assertEqual(node.providePorts[1].dsg.calcStructFmtStr(node.dataTypes), '<B') #unsigned char
      self.assertEqual(node.providePorts[2].dsg.calcStructFmtStr(node.dataTypes), '<B') #unsigned char
      self.assertEqual(node.providePorts[3].dsg.calcStructFmtStr(node.dataTypes), '<B') #unsigned char      
      self.assertEqual(node.requirePorts[0].dsg.calcStructFmtStr(node.dataTypes), '<B') #unsigned char
      self.assertEqual(node.requirePorts[1].dsg.calcStructFmtStr(node.dataTypes), '<4s') #char[4]
      self.assertEqual(node.requirePorts[2].dsg.calcStructFmtStr(node.dataTypes), '<8sI3H') #char[8],unsigned int, unsigned short[3]
      
   
if __name__ == '__main__':
    unittest.main()