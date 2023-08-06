====================================
``psyclone.psyir.symbols.datatypes``
====================================

.. automodule:: psyclone.psyir.symbols.datatypes

   .. contents::
      :local:

.. currentmodule:: psyclone.psyir.symbols.datatypes


Classes
=======

- :py:class:`UnknownType`:
  Indicates that a variable declaration is not supported by the PSyIR.

- :py:class:`UnknownFortranType`:
  Indicates that a Fortran declaration is not supported by the PSyIR.

- :py:class:`DeferredType`:
  Indicates that the type is unknown at this point.

- :py:class:`ScalarType`:
  Describes a scalar datatype (and its precision).

- :py:class:`ArrayType`:
  Describes an array datatype. Can be an array of intrinsic types (e.g.

- :py:class:`StructureType`:
  Describes a 'structure' or 'derived' datatype that is itself composed


.. autoclass:: UnknownType
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: UnknownType
      :parts: 1

.. autoclass:: UnknownFortranType
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: UnknownFortranType
      :parts: 1

.. autoclass:: DeferredType
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: DeferredType
      :parts: 1

.. autoclass:: ScalarType
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: ScalarType
      :parts: 1

.. autoclass:: ArrayType
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: ArrayType
      :parts: 1

.. autoclass:: StructureType
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: StructureType
      :parts: 1
