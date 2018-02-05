Creating APX nodes
==================

It's easy to create your own APX nodes directly in Python. There are two different paths you can take.
Which one you choose is really a matter of choice and convenience.

- Importing an exsting software component using the `AUTOSAR Python module <https://github.com/cogu/autosar>`_.
- Programmatically create your own APX node using the `APX Text syntax <http://apx.readthedocs.io/en/latest/apx_text.html>`_.

Importing an AUTOSAR software component
---------------------------------------

In AUTOSAR, software components are used to describe the boundaries between application logic. Somewhat simplified, each software component
can be treated as a black box containing some kind of logic with input signals going into it and output signals coming out of it.
The term *signal* isn't really used in AUTOSAR, instead we use the term *port* to mean the same thing.

Input signals are therefore known as *Require Ports* while output signals are known as *Provide Ports*.

Limitations and restrictions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In order to use an existing AUTOSAR software component (SWC) as an APX node the component need to fulfill the following criterias:

- The SWC must be of type ApplicationSoftwareComponent
- In supports data ports only (ClientServerInterface ports or Mode ports are not supported in APX).
- Each data port must have a single data element defined in its SenderReceiverInterface.
- Only supports AUTOSAR 3 data types (AUTOSAR 4 support in APX is far into the future).

.. note::

    The single data element limit isn't really a limitation at all since you can always declare single data elements using a record (struct) definition
    of arbitrary complexity of your choice.

Example
~~~~~~~

Here is a simple example of an AUTOSAR SWC called **ExampleSWC**:

.. include:: examples/autosar_01.py
    :code: python

Alternatively you can load an SWC from existing XML. The section :ref:`ref_create_from_autosar` in the API reference provides examples where this is done.

Once you have an instance of an AUTOSAR SWC you can easily turn it into an APX node using one of the following ways.

.. code-block:: python

    node = apx.Node()
    node.import_autosar_swc(swc)

This is equivalent to:

.. code-block:: python

    node = apx.Node.from_autosar_swc(swc)    

.. _programmatic_apx_node:

Creating APX nodes programatically
----------------------------------

APX nodes can be created directly in Python without the use of AUTOSAR.

An APX Node has the following components:

- Node name: The name must be a unique name within the APX network (to prevent name-clash).
- A list internal data types (0 or more)
- A list of provide ports (0 or more)
- A list of require ports (0 or more)

Creating the APX node
~~~~~~~~~~~~~~~~~~~~~~

Use the Node class to create a new node with your selected node name.

.. code-block:: python

    import apx
    
    node = apx.Node('MyNode')
    
Creating ports
~~~~~~~~~~~~~~

APX ports are created using the two classes apx.RequirePort and apx.ProvidePort.

.. code-block:: python
    
    r_port = apx.RequirePort(port_name, data_signature, port_attribute)
    
    p_port = apx.ProvidePort(port_name, data_signature, port_attribute)

Each of the three parameters (above) are string types:

- port_name: name of the port
- data_signature: describes its data type (see below)
- port_attribute(s): describes 1 or more port attributes (see below)

.. note::

    The port_attribute argument is optional, you can call the RequirePort and ProvidePort classes with just 2 arguments if you should wish.

Data Signatures
~~~~~~~~~~~~~~~

The data signature describes the data type of the port. It is a string that can take many shapes and forms but
most of the time it is simply a single character describing an integer data type.


Integer data types
^^^^^^^^^^^^^^^^^^

APX currently supports the following integer data types:

+-----------+-----------+------+-------------+------------+
| Type Code | Type Name | Bits | Min         | Max        |
+===========+===========+======+=============+============+
| c         | sint8     |  8   |  -128       | 127        |
+-----------+-----------+------+-------------+------------+
| s         | sint16    | 16   |  -32768     | 32767      |
+-----------+-----------+------+-------------+------------+
| l         | sint32    | 32   | -2147483648 | 2147483647 |
+-----------+-----------+------+-------------+------------+
| C         | uint8     |  8   |   0         | 255        |
+-----------+-----------+------+-------------+------------+
| S         | uint16    |  16  |   0         | 65535      |
+-----------+-----------+------+-------------+------------+
| L         | uint32    |  32  |   0         | 4294967295 |
+-----------+-----------+------+-------------+------------+

Example ports:

.. code-block:: python
    
    u8_port = apx.RequirePort('U8Port','C')
    u16_port = apx.RequirePort('U16Port','S')
    u32_port = apx.RequirePort('U32Port','L')
