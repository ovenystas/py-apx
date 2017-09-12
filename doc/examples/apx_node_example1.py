import apx
   
node = apx.Node('TestNode')
node.append(apx.ProvidePort('TestSignal2','C'))
node.append(apx.RequirePort('TestSignal1','S'))
      
apx.NodeGenerator().generate('.', node, includes=['Rte_Type.h'])