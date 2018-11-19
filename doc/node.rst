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

Alternatively you can load an SWC from existing XML. The section :ref:`ref_create_from_autosar` in the API reference shows examples of this.

Once you have an instance of an AUTOSAR SWC you can easily turn it into an APX node using the following code:

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
The node name shall be a unique string that isn't in use by any other APX node you aim to connect to.

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
- data_signature: describes its data type (introduced later)
- port_attribute(s): describes 1 or more port attributes (introduced later)

.. note::

    The port_attribute argument is optional, you can call the RequirePort and ProvidePort classes with just 2 arguments if you should wish.

Introduction to Data Signatures
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The data signature describes the data type of the port. It is a string that can take many shapes and forms but
most often it is just a single character, which is code for an integer type.


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

Examples:

.. code-block:: python
    
    u8_port = apx.RequirePort('U8Port','C')
    u16_port = apx.RequirePort('U16Port','S')
    u32_port = apx.RequirePort('U32Port','L')

String data types
^^^^^^^^^^^^^^^^^

APX supports strings by declaring arrays of characters.

+-----------+-----------+------+-------------+------------+
| Type Code | Type Name | Bits | Min         | Max        |
+===========+===========+======+=============+============+
| a         | string    |  8   |  0          | 255        |
+-----------+-----------+------+-------------+------------+

Examples:

.. code-block:: python
    
    str1_port = apx.RequirePort('Str1','a[20]') #A string with max-length 20
    str2_port = apx.RequirePort('Str2','a[100]') #A string with max-length 100

In a future version of APX the z-type character will be introduced to better distuingish between strings that reserve a byte for null-terminating character vs. those who do not.

Adding ports to the node
~~~~~~~~~~~~~~~~~~~~~~~~

Use the append method to add new ports to your APX node.

Example:

.. code-block:: python

    import apx
    
    node = apx.Node('MyNode')
    node.append(apx.ProvidePort('U8Port', 'C'))
    node.append(apx.RequirePort('U16Port', 'S'))

More about data signatures
--------------------------

Data signatures can be a lot more complex than just integer types. You can also create arrays, type references and records.

Array signatures
~~~~~~~~~~~~~~~~

You can create arrays of other types (like integers) by appending *[n]* to the type code where n is the number of array elements.

Examples:

.. code-block:: python
        
    u8_ar_port = apx.RequirePort('U8Array','C[6]') #array of 6 uint8 elements
    u16_ar_port = apx.RequirePort('U16Array','S[4]') #array of 4 uint16 elements
    u32_ar_port = apx.RequirePort('U32Array','L[2]') #array of 2 uint32 elements

Records
~~~~~~~

Records are data types that contains multiple named fields. Records are sometimes known as struct (or structures) in some programming languages.

Records are defined within two brace characters '{}'. Field names always comes first and is always a string literal (enclosed by '"' characters).
Immediately following the field name comes the data type, this can be any integer or string type code or for that matter another record definition.

Examples:

.. code-block:: python
    
    user_data_port = apx.RequirePort('UserData','{"UserName"a[100]"UserId"L}') #A record which has length 104 bytes and two fields
    rectangle_port = apx.RequirePort('Rectangle', '{"From"{"x"L"y"L}"To"{"x"L"y"L}}') # A record containing two sub-records.

Type References
~~~~~~~~~~~~~~~~

TBD

Port Attributes
---------------

TBD

Init Values
~~~~~~~~~~~

TBD

Array Init Values
^^^^^^^^^^^^^^^^^^

TBD

Record Init Values
^^^^^^^^^^^^^^^^^^

TBD

Example Node
------------

The following APX node is purely intended as a demonstration of how to create an APX node from scratch using some automotive signal types and definitions

Data Types
~~~~~~~~~~

**BatteryVoltage_T (physical type):**

+--------+-----------+-----------------------------+
| Min    | Max       | Unit / ValueTable           |
+========+===========+=============================+
| 0      | 65535     | Volts (65535=Not Available) |
+--------+-----------+-----------------------------+

.. note::

    Currently there is no method to describe physical scaling and offset using APX. It might be introduced in a future version.

**Date_T (record type):**

+--------------+--------+-----------+----------------------------+
| Element Name | Min    | Max       | Unit / ValueTable          |
+==============+========+===========+============================+
| Year         | 0      | 255       | Years (255=Not Available)  |
+--------------+--------+-----------+----------------------------+
| Month        | 1      | 13        | Months  (13=Not Available) |
+--------------+--------+-----------+----------------------------+
| Day          | 1      | 32        | Days (32=Not Available)    |
+--------------+--------+-----------+----------------------------+

**InactiveActive_T (enumeration type):**

+--------+-------+-------------------------------+
| Min    | Max   | Unit / ValueTable             |
+========+=======+===============================+
| 0      | 3     | 0=InactiveActive_Inactive,    |
|        |       | 1=InactiveActive_Active,      |
|        |       | 2=InactiveActive_Error,       |
|        |       | 3=InactiveActive_NotAvailable |
+--------+-------+-------------------------------+

Signals
~~~~~~~

+----------------------+------------------+------------------+
| Name                 | Data Type        | Init Value       |
+======================+==================+==================+
| BatteryVoltage       | BatteryVoltage_T | 65535            |
+----------------------+------------------+------------------+
| CurrentDate          | Date_T           | {255, 13, 32}    |
+----------------------+------------------+------------------+
| ExteriorLightsActive | InactiveActive_T | 3                |
+----------------------+------------------+------------------+

APX Node
~~~~~~~~

The following apx node contains:

- 3 type definitions
- 1 provide port
- 2 require port
- 3 type references
- 3 init values (port attribute strings)

.. include:: examples/node_01.py
    :code: python
