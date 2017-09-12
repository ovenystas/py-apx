import apx
   
node = apx.Node('TestNode')
node.append(apx.ProvidePort('TestSignal2','C'))
node.append(apx.RequirePort('TestSignal1','S'))
callback_map={'TestSignal1': 'TestSignal1_CallbackFunc'}      
apx.NodeGenerator().generate('.', node, includes=['Rte_Type.h'], callbacks=callback_map)
