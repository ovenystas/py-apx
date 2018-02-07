import apx

node = apx.Node('Example')
node.append(apx.DataType('BatteryVoltage_T', 'S'))
node.append(apx.DataType('Date_T', '{"Year"C"Month"C(1,13)"Day"C(1,32)}'))
node.append(apx.DataType('InactiveActive_T','C(0,3)', 'VT("InactiveActive_Inactive", "InactiveActive_Active", "InactiveActive_Error", "InactiveActive_NotAvailable")'))

node.append(apx.ProvidePort('BatteryVoltage','T["BatteryVoltage_T"]','=65535'))
node.append(apx.RequirePort('CurrentDate', 'T["Date_T"]', '={255, 13, 32}'))
node.append(apx.RequirePort('ExteriorLightsActive', 'T["InactiveActive_T"]', '=3'))

print(apx.Context().append(node).dumps())