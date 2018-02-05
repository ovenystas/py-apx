import autosar
import apx

ws = autosar.workspace()
dataTypes = ws.createPackage('DataType', role='DataType')
dataTypes.createSubPackage('CompuMethod', role='CompuMethod')
dataTypes.createSubPackage('Unit', role='Unit')
dataTypes.createIntegerDataType('OffOn_T', valueTable=[
       "OffOn_Off",
       "OffOn_On",
       "OffOn_Error",
       "OffOn_NotAvailable"])
dataTypes.createIntegerDataType('Percent_T', min=0, max=255, offset=0, scaling=0.4, unit='Percent')
dataTypes.createIntegerDataType('VehicleSpeed_T', min=0, max=65535, offset=0, scaling=1/64, unit='km/h')
constants = ws.createPackage('Constant', role='Constant')
constants.createConstant('C_EngineRunningStatus_IV', 'OffOn_T', 3)
constants.createConstant('C_FuelLevelPercent_IV', 'Percent_T', 255)
constants.createConstant('C_VehicleSpeed_IV', 'VehicleSpeed_T', 65535)
portInterfaces = ws.createPackage('PortInterface', role='PortInterface')
portInterfaces.createSenderReceiverInterface('EngineRunningStatus_I',
                                             autosar.DataElement('EngineRunningStatus', 'OffOn_T'))
portInterfaces.createSenderReceiverInterface('FuelLevelPercent_I',
                                             autosar.DataElement('FuelLevelPercent', 'Percent_T'))
portInterfaces.createSenderReceiverInterface('VehicleSpeed_I',
                                             autosar.DataElement('VehicleSpeed', 'VehicleSpeed_T'))
components = ws.createPackage('ComponentType', role='ComponentType')
swc = components.createApplicationSoftwareComponent('ExampleSWC')
swc.createRequirePort('EngineRunningStatus', 'EngineRunningStatus_I', initValueRef=constants['C_EngineRunningStatus_IV'].ref)   
swc.createRequirePort('VehicleSpeed', 'VehicleSpeed_I', initValueRef=constants['C_VehicleSpeed_IV'].ref)
swc.createProvidePort('FuelLevelPercent', 'FuelLevelPercent_I', initValueRef=constants['C_FuelLevelPercent_IV'].ref)

