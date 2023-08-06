==================================
``psyclone.psyir.nodes.operation``
==================================

.. automodule:: psyclone.psyir.nodes.operation

   .. contents::
      :local:

.. currentmodule:: psyclone.psyir.nodes.operation


Classes
=======

- :py:class:`Operation`:
  Abstract base class for PSyIR nodes representing operators.

- :py:class:`UnaryOperation`:
  Node representing a UnaryOperation expression. As such it has one operand

- :py:class:`BinaryOperation`:
  Node representing a BinaryOperation expression. As such it has two operands

- :py:class:`NaryOperation`:
  Node representing a n-ary operation expression. The n operands are


.. autoclass:: Operation
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: Operation
      :parts: 1

.. autoclass:: UnaryOperation
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: UnaryOperation
      :parts: 1

.. autoclass:: BinaryOperation
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: BinaryOperation
      :parts: 1

.. autoclass:: NaryOperation
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: NaryOperation
      :parts: 1
