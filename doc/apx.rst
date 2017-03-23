APX Documentation
=================

Node
----
.. py:class :: Node(name=None)

   Represents an APX node in Python. Setting a name during construction is optional but a valid name must be set before the node is taken in use (as client or for code/text generation purposes).
    
.. py:attribute:: Node.name : string

   The name of the node.

.. py:method:: Node.append(port)

   This is an overloded method that is used for creating new ports in the node object.
   
Creating ports using APX Port objects
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   
TBD

Creating ports using raw APX text
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   
TBD

Creating ports from existing AUTOSAR ports
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   
TBD



.. py:method :: Node.write(fp):

Writes the APX node as APX Text into the file object fp. fp must be an open file.
Normal user's should use the write method in the Context object instead of using this method.

Context
-------
.. py:class :: Context()

   The APX context is just a container for one or more (usually one) APX nodes.

Example::

   import apx
   
   context = apx.Context()


