APX Documentation
=================

Node
----
.. py:class :: Node(name=None)

   Represents an APX node in Python. Setting a name during construction is optional but a valid name must be set before the node is taken in use (as client or for code/text generation purposes).
    
.. py:attribute:: Node.name : string

   The name of the node.

.. py:method:: Node.append(port)

   This is an overloded method that is used for creating new ports in the node object. It returns the port ID (type int) of the newly created port.
   
   There are three different ways of creating ports in a node object
   
Creating ports using APX Port objects
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   
APX port objects is the native form in which ports are stored in a node. Use *apx.RequirePort* or *apx.ProvidePort* to create new ports in a node.

Example::

   import sys
   import apx
   
   node = apx.Node()
   #create provide-port with name=TestSignal1 and type uint8
   node.append(apx.ProvidePort('TestSignal1','C'))
   #create require-port with name=TestSignal2 and type uint16
   node.append(apx.RequirePort('TestSignal2','S'))
   node.write(sys.stdout)

Output:

.. code-block:: console

   N"None"
   P"TestSignal1"C
   R"TestSignal2"S

.. note::

   When using Node.write() method to generate APX output the **provide** ports are always written before **require** ports.

Creating ports using raw APX text strings
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   
Raw text strings can be used in the append call, The string must be a valid line from an APX Text (.apx) file.
Before appending to internal port lists the string is transformed into *apx.RequirePort* or *apx.ProvidePort* objects depending on
contents of the string data.

Example::

   import sys
   import apx

   node = apx.Node()
   #create provide-port with name=TestSignal1 and type uint8
   node.append('P"TestSignal1"C')
   #create require-port with name=TestSignal2 and type uint16
   node.append('R"TestSignal2"S')
   node.write(sys.stdout)

Output:

.. code-block:: console

   N"None"
   P"TestSignal1"C
   R"TestSignal2"S


Creating ports from existing AUTOSAR ports
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   
ports in an APX node can also be created based on autosar ports.

Example::
  
   import sys
   import apx
   import autosar
   
   #Set all path_to_* variables seen below and set them to valid paths in the file system.
   #Set name_of_swc to the name of the SWC you are converting to an APX node.
  
   ws=autosar.workspace()
   ws.loadXML(path_to_datatypes_arxml, roles={'/DataType': 'DataType'})
   ws.loadXML(path_to_constants_arxml, roles={'/Constant': 'Constant'})
   ws.loadXML(path_to_portinterfaces_arxml, roles={'/PortInterface': 'PortInterface'})
   ws.loadXML(path_to_swc_arxml, roles={'/ComponentType': 'ComponentType'})

   swc = ws.find('/ComponentType/'+name_of_swc)
   assert(swc is not None)

   node = apx.Node(swc.name)
   #add all provide-ports to node object
   for autosar_port in swc.providePorts:
      portInterface = ws.find(autosar_port.portInterfaceRef)
      if (type(portInterface) is autosar.portinterface.SenderReceiverInterface) and (len(portInterface.dataElements)>0):
         node.append(autosar_port)
   #add all require-ports to node object
   for autosar_port in swc.requirePorts:
      portInterface = ws.find(autosar_port.portInterfaceRef)
      if (type(portInterface) is autosar.portinterface.SenderReceiverInterface) and (len(portInterface.dataElements)>0):
         node.append(autosar_port)
   
   
.. py:method :: Node.write(file):

Writes the APX node as APX Text into the file object. The file object must be an open file with write permission.
Normal user's should use the write method in the Context object instead of using this method.

.. py:method :: Node.mirror(name=None):

Returns a copy of the node where all require-ports and provide ports have been flipped. This is used to create APX proxy nodes.
A custom name of the new node can be set by the name argument (type string). If name is None the new node will have the same name as its original.

Example::

   import sys
   import apx

   node = apx.Node()   
   node.append('P"TestSignal1"C')   
   node.append('R"TestSignal2"S')
   proxy_node = node.mirror('ProxyNode')
   proxy_node.write(sys.stdout)

Output:

.. code-block:: console
   
   N"ProxyNode"
   P"TestSignal2"S
   R"TestSignal1"C

.. py:method :: Node.import_autosar_swc(swc, ws):

Imports all ports from an existing software component from an autosar workspace.

Example::
  
   import sys
   import apx
   import autosar
   
   #Set all path_to_* variables seen below and set them to valid paths in the file system.
   #Set name_of_swc to the name of the SWC you are converting to an APX node.
  
   ws=autosar.workspace()
   ws.loadXML(path_to_datatypes_arxml, roles={'/DataType': 'DataType'})
   ws.loadXML(path_to_constants_arxml, roles={'/Constant': 'Constant'})
   ws.loadXML(path_to_portinterfaces_arxml, roles={'/PortInterface': 'PortInterface'})
   ws.loadXML(path_to_swc_arxml, roles={'/ComponentType': 'ComponentType'})

   swc = ws.find('/ComponentType/'+name_of_swc)
   assert(swc is not None)

   node = apx.Node(swc.name)
   node.import_autosar_swc(swc, ws)

.. _Node_add_type:

.. py:method :: Node.add_type(data_type):

   Adds the data type to the node. When this method is called the data_type is assigned the 'id' attribute (which is an integer).
   This attribute can be used for referencing the type later when creating ports. See DataType_ for a full example.

RequirePort
-----------

.. py:class :: RequirePort(name : string, data_signature : string, attributes=None)

Creates a new APX require-port with assigned name.

The data_signature can be a single character string with a primitive type code (see `APX Text <http://apx.readthedocs.io/en/latest/apx_text.html>`_.) or it can be a more complex signature.
The optional attribute string can contain various port attributes. The full format of attribute strings is yet to be documented.
The only partially implemented attribute so far is the init-value of a port which is written as '=x' where x is the integer init value.

Example::
   
   #port with name 'Port1', type: 'uint8'
   port1 = apx.RequirePort('Port1', 'C')

   #port with name:'Port2', type:'uint8', init-value:7
   port2 = apx.RequirePort('Port2', 'C', '=7')
   
   #port with name:'Port3', type:'uint16', init-value:65535
   port3 = apx.RequirePort('Port3', 'S', '=65535')
   
   #port with name:'Port4', type:'uint32', init-value:0xFFFFFFFF
   port4 = apx.RequirePort('Port4', 'L', '=0xFFFFFFFF')
   
   #port with name:'Port5', type:'uint8', array-len:4, init-value:{0,0,0,0}
   port5 = apx.RequirePort('Port5', 'C[4]', '={0,0,0,0}')
   
   #port with name: 'Port6', type:'string', string-len=20, init-value:""
   port6 = apx.RequirePort('Port6', 'a[20]', '=""')
   
   #port with name: 'Port7', type:'record', record-elements: ['UserName', 'UserID'], init-value: {"",0xFFFFFFFF}
   Port7: apx.RequirePort('Port7', '{"UserName"a[32]"UserID"L}', '{"",0xFFFFFFFF}')

ProvidePort
-----------

.. py:class :: ProvidePort(name : string, data_signature : string, attributes=None)

Creates a new APX provide-port with the assigned name.

arguments and examples are the same as for apx.RequirePort except of course that you use *apx.ProvidePort* as constructor instead.

DataType
--------

.. py:class :: DataType(name : string, data_signature : string, attributes=None)

This creates a new APX data type with the assigned name and data signature.

Use the :ref:`Node.add_type <Node_add_type>` method to add the type to the node. The add_type method will set an id attribute on the datatype that you
can refer to later with referencing the datatype.

Example::

   import apx
   
   if __name__ == '__main__':    
       VehicleSpeed_T = apx.DataType('VehicleSpeed_T', 'S')
       EngineSpeed_T = apx.DataType('EngineSpeed_T', 'S')
       
       node = apx.Node('ExampleNode')
       node.add_type(VehicleSpeed_T)
       node.add_type(EngineSpeed_T)
       node.append(apx.ProvidePort('VehicleSpeed', 'T[%d]'%VehicleSpeed_T.id, '=65535'))
       node.append(apx.ProvidePort('EngineSpeed', 'T[%d]'%EngineSpeed_T.id, '=65535'))
       apx.Context().append(node).generateAPX()




Context
-------
.. py:class :: Context()

   The APX context is a container for one or more APX nodes.

Example::

   import apx
   
   context = apx.Context()

.. py:method :: append(node : apx.Node)

Appends an APX node to the context.

.. py:method :: generateAPX(output_dir):

For each node in context, generate a new APX Text file. outputDir is expected to be a directory where files are generated.

Returns:
A list of file names written to output_dir

Helper functions
~~~~~~~~~~~~~~~~

.. py::function :: apx.createContextfromPartition(partition)

A complete APX context can be generated automatically from an AUTOSAR partition.
A new APX node is created in the context for each AUTOSAR SWC found in the partition.

Example::

   import autosar
   import apx
   
   ws = autosar.workspace()
   ws.loadXML('SWC1.arxml')
   ws.loadXML('SWC2.arxml')
   partition = autosar.rte.Partition(prefix='ApxRte')
   partition.addComponent(ws.find('/ComponentType/SWC1'))
   partition.addComponent(ws.find('/ComponentType/SWC2'))
   context = apx.createContextfromPartition(partition)

Parser
------

.. py:class :: Parser()

The *apx.Parser* class is able to parse .apx file data back into *apx.Node* object(s).

.. py:method :: parse(filename)

Parses APX file from filename. Returns the first parsed node from the file.

Example::

   import apx
   
   node = apx.Parser().parse('MyNode.apx')

   for port in node.providePorts:      
      print(port.name)
   print("")
   for port in node.requirePorts:      
      print(port.name)

NodeGenerator
--------------

.. py:class :: NodeGenerator()

APX Node generator for `c-apx <https://github.com/cogu/c-apx>`_ (both full c-apx and apx-es nodes are supported).

.. py:method :: NodeGenerator.generate(self, output_dir, node, name=None, includes=None, callbacks=None):

Arguments:
  
  * output_dir: directory where source and header files will be written. If you want direct the output to current directory, use '.' as argument.
  * node : an Instance of *apx.Node*
  * name (optional): This argument can be used to override the name of the node. Default behavior is to use the name from the node object.
  * includes (optional): A list of extra includes to add to the default list of includes in the header file.
  * callbacks (optional): A dictionary where the key is a require port names and its value is the name of the C function to call (when a new value has been received).

  If you are generating an APX node containing AUTOSAR data type name, make sure to include "Rte_Type.h" in the includes argument list.

Example 1::

   import apx
   
   node = apx.Node('TestNode')
   node.append(apx.ProvidePort('TestSignal2','C'))
   node.append(apx.RequirePort('TestSignal1','S'))   
   apx.NodeGenerator().generate('.', node, includes=['Rte_Type.h'])
   
Example 2 (with callbacks)::

   import apx
   
   node = apx.Node('TestNode')
   node.append(apx.ProvidePort('TestSignal2','C'))
   node.append(apx.RequirePort('TestSignal1','S'))
   callback_map={'TestSignal1': 'TestSignal1_CallbackFunc'}      
   apx.NodeGenerator().generate('.', node, includes=['Rte_Type.h'], callbacks=callback_map)
   

