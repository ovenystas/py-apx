import apx
import autosar

def createContextfromPartition(autosar_partition):
   context = Context()
   for component in autosar_partition.components:
      assert(component.swc is not None)
      swc = component.swc
      ws = swc.rootWS()
      apx_node = apx.Node(swc.name)
      for port in swc.requirePorts + swc.providePorts:
         portInterface = ws.find(port.portInterfaceRef)
         if portInterface is None:
            print('Warning (port=%s): PortInterface with ref %s not found in ECU extract'%(port.name, port.portInterfaceRef))
         else:
            if (type(portInterface) is autosar.portinterface.SenderReceiverInterface) and (len(portInterface.dataElements)>0):
               apx_node.append(port)
      context.append(apx_node)
   return context

class Context:
   def __init__(self):
      self.nodes = []
   
   def append(self, node):
      assert(isinstance(node, apx.Node))
      self.nodes.append(node)
      
   def write(self, fp):
      """
      writes context to file fp
      """
      fp.write("APX/1.2\n")
      for node in self.nodes:
         node.write(fp)
      fp.write("\n") #always end file with a new line

   def dumps(self):
      """
      returns context as a string
      """
      lines = []
      lines.append("APX/1.2")
      for node in self.nodes:
         lines.extend(node.lines())
      text = '\n'.join(lines)+'\n'
      return text
   
