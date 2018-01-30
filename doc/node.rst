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

Here is a simple example of a programmtically created AUTOSAR SWC called **ExampleSWC**:

.. include:: examples/autosar_01.py
    :code: python




