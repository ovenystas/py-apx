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
   ws.loadXML(path_to_component_arxml, roles={'/ComponentType': 'ComponentType'})

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

Creates a new APX provide-port with assigned name.

arguments and examples are the same as for apx.RequirePort except of course that you use *apx.ProvidePort* as constructor instead.

Context
-------
.. py:class :: Context()

   The APX context is just a container for one or more (usually one) APX nodes.

Example::

   import apx
   
   context = apx.Context()

.. py:method :: append(node : apx.Node)

Appends an APX node to this context.

.. py:method :: write(file):

writes context to file object. The file object must be an open file with write permission.

For a context with a single node, this call is identical to performing node.write(file) except that the line "APX/1.2" will be inserted before the output from node.write().

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

.. py:method :: NodeGenerator.generate(node, header_fp, source_fp, name=None, includes=None):

Arguments:
  
  * node : an Instance of *apx.Node*
  * header_fp: The C header is written into this open file object. (Caller must open the file before calling this method.)
  * source_fp: The C source is written into this open file object. (Caller must open the file before calling this method.)
  * name (optional): This argument can be used to override the name of the node. Default behavior is to use the name from the node object.
  * includes (optional): A List of extra includes to add to the default list of includes in the header file.

  If you are generating an APX node containing AUTOSAR data type name, make sure that "Rte_Type.h" is added to the list of extra includes in the includes argument.

Example::

   import apx
   
   node = apx.Node('TestNode')
   node.append(apx.ProvidePort('TestSignal2','C'))
   node.append(apx.RequirePort('TestSignal1','S'))
   
   header_fp = open('Apx_TestNode.h', 'w')
   source_fp = open('Apx_TestNode.c', 'w')
   
   apx.NodeGenerator().generate(node, header_fp, source_fp, includes=['Rte_Type.h'])
   
   header_fp.close()
   source_fp.close()
   
   with open('Apx_TestNode.h') as fp:
      print(fp.read())

Output:

.. code-block:: C

   #ifndef APX_TESTNODE_H
   #define APX_TESTNODE_H
   
   #include "apx_nodeData.h"
   #include "Rte_Type.h"
   
   //////////////////////////////////////////////////////////////////////////////
   // CONSTANTS
   //////////////////////////////////////////////////////////////////////////////
   
   //////////////////////////////////////////////////////////////////////////////
   // FUNCTION PROTOTYPES
   //////////////////////////////////////////////////////////////////////////////
   void Apx_TestNode_init(void);
   apx_nodeData_t * Apx_TestNode_getNodeData(void);
   
   Std_ReturnType Apx_TestNode_Read_TestSignal1(sint16 *val);
   Std_ReturnType Apx_TestNode_Write_TestSignal2(uint8 val);
   void Apx_TestNode_inPortDataWritten(void *arg, apx_nodeData_t *nodeData, uint32_t offset, uint32_t len);
   
   #endif //APX_TESTNODE_H