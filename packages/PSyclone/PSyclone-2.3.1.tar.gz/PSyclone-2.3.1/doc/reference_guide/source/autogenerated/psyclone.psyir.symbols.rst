==========================
``psyclone.psyir.symbols``
==========================

.. automodule:: psyclone.psyir.symbols

   .. contents::
      :local:


Submodules
==========

.. toctree::

   psyclone.psyir.symbols.containersymbol
   psyclone.psyir.symbols.data_type_symbol
   psyclone.psyir.symbols.datasymbol
   psyclone.psyir.symbols.datatypes
   psyclone.psyir.symbols.routinesymbol
   psyclone.psyir.symbols.symbol
   psyclone.psyir.symbols.symboltable
   psyclone.psyir.symbols.typed_symbol

.. currentmodule:: psyclone.psyir.symbols


Classes
=======

- :py:class:`ArgumentInterface`:
  Captures the interface to a Symbol that is accessed as a routine

- :py:class:`ArrayType`:
  Describes an array datatype. Can be an array of intrinsic types (e.g.

- :py:class:`ContainerSymbol`:
  Symbol that represents a reference to a Container. The reference

- :py:class:`DataSymbol`:
  Symbol identifying a data element. It contains information about:

- :py:class:`DataType`:
  Abstract base class from which all types are derived.

- :py:class:`DataTypeSymbol`:
  Symbol identifying a user-defined type (e.g. a derived type in Fortran).

- :py:class:`DeferredType`:
  Indicates that the type is unknown at this point.

- :py:class:`ImportInterface`:
  Describes the interface to a Symbol that is imported from an external

- :py:class:`LocalInterface`:
  The symbol just exists in the Local context 

- :py:class:`NoType`:
  Indicates that the associated symbol has an empty type (equivalent

- :py:class:`RoutineSymbol`:
  Symbol identifying a callable routine.

- :py:class:`ScalarType`:
  Describes a scalar datatype (and its precision).

- :py:class:`StructureType`:
  Describes a 'structure' or 'derived' datatype that is itself composed

- :py:class:`Symbol`:
  Generic Symbol item for the Symbol Table and PSyIR References.

- :py:class:`SymbolTable`:
  Encapsulates the symbol table and provides methods to add new

- :py:class:`TypedSymbol`:
  Abstract base class for those Symbols that have an associated datatype.

- :py:class:`UnknownFortranType`:
  Indicates that a Fortran declaration is not supported by the PSyIR.

- :py:class:`UnknownType`:
  Indicates that a variable declaration is not supported by the PSyIR.

- :py:class:`UnresolvedInterface`:
  We have a symbol but we don't know where it is declared.


.. autoclass:: ArgumentInterface
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: ArgumentInterface
      :parts: 1

.. autoclass:: ArrayType
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: ArrayType
      :parts: 1

.. autoclass:: ContainerSymbol
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: ContainerSymbol
      :parts: 1

.. autoclass:: DataSymbol
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: DataSymbol
      :parts: 1

.. autoclass:: DataType
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: DataType
      :parts: 1

.. autoclass:: DataTypeSymbol
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: DataTypeSymbol
      :parts: 1

.. autoclass:: DeferredType
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: DeferredType
      :parts: 1

.. autoclass:: ImportInterface
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: ImportInterface
      :parts: 1

.. autoclass:: LocalInterface
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LocalInterface
      :parts: 1

.. autoclass:: NoType
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: NoType
      :parts: 1

.. autoclass:: RoutineSymbol
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: RoutineSymbol
      :parts: 1

.. autoclass:: ScalarType
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: ScalarType
      :parts: 1

.. autoclass:: StructureType
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: StructureType
      :parts: 1

.. autoclass:: Symbol
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: Symbol
      :parts: 1

.. autoclass:: SymbolTable
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: SymbolTable
      :parts: 1

.. autoclass:: TypedSymbol
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: TypedSymbol
      :parts: 1

.. autoclass:: UnknownFortranType
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: UnknownFortranType
      :parts: 1

.. autoclass:: UnknownType
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: UnknownType
      :parts: 1

.. autoclass:: UnresolvedInterface
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: UnresolvedInterface
      :parts: 1


Exceptions
==========

- :py:exc:`SymbolError`:
  PSyclone-specific exception for use with errors relating to the Symbol and


.. autoexception:: SymbolError

   .. rubric:: Inheritance
   .. inheritance-diagram:: SymbolError
      :parts: 1


Variables
=========

- :py:data:`BOOLEAN_TYPE`
- :py:data:`CHARACTER_TYPE`
- :py:data:`INTEGER_TYPE`
- :py:data:`INTEGER_SINGLE_TYPE`
- :py:data:`INTEGER_DOUBLE_TYPE`
- :py:data:`INTEGER4_TYPE`
- :py:data:`INTEGER8_TYPE`
- :py:data:`REAL_TYPE`
- :py:data:`REAL_SINGLE_TYPE`
- :py:data:`REAL_DOUBLE_TYPE`
- :py:data:`REAL4_TYPE`
- :py:data:`REAL8_TYPE`
- :py:data:`TYPE_MAP_TO_PYTHON`

.. autodata:: BOOLEAN_TYPE
   :annotation:

   .. code-block:: text

      <psyclone.psyir.symbols.datatypes.ScalarType object at 0x7f551edb6b20>

.. autodata:: CHARACTER_TYPE
   :annotation:

   .. code-block:: text

      <psyclone.psyir.symbols.datatypes.ScalarType object at 0x7f551edb6bb0>

.. autodata:: INTEGER_TYPE
   :annotation:

   .. code-block:: text

      <psyclone.psyir.symbols.datatypes.ScalarType object at 0x7f551edb6910>

.. autodata:: INTEGER_SINGLE_TYPE
   :annotation:

   .. code-block:: text

      <psyclone.psyir.symbols.datatypes.ScalarType object at 0x7f551edb6970>

.. autodata:: INTEGER_DOUBLE_TYPE
   :annotation:

   .. code-block:: text

      <psyclone.psyir.symbols.datatypes.ScalarType object at 0x7f551edb6a00>

.. autodata:: INTEGER4_TYPE
   :annotation:

   .. code-block:: text

      <psyclone.psyir.symbols.datatypes.ScalarType object at 0x7f551edb6a60>

.. autodata:: INTEGER8_TYPE
   :annotation:

   .. code-block:: text

      <psyclone.psyir.symbols.datatypes.ScalarType object at 0x7f551edb6ac0>

.. autodata:: REAL_TYPE
   :annotation:

   .. code-block:: text

      <psyclone.psyir.symbols.datatypes.ScalarType object at 0x7f551edb6760>

.. autodata:: REAL_SINGLE_TYPE
   :annotation:

   .. code-block:: text

      <psyclone.psyir.symbols.datatypes.ScalarType object at 0x7f551edb67c0>

.. autodata:: REAL_DOUBLE_TYPE
   :annotation:

   .. code-block:: text

      <psyclone.psyir.symbols.datatypes.ScalarType object at 0x7f551edb6820>

.. autodata:: REAL4_TYPE
   :annotation:

   .. code-block:: text

      <psyclone.psyir.symbols.datatypes.ScalarType object at 0x7f551edb6880>

.. autodata:: REAL8_TYPE
   :annotation:

   .. code-block:: text

      <psyclone.psyir.symbols.datatypes.ScalarType object at 0x7f551edb6580>

.. autodata:: TYPE_MAP_TO_PYTHON
   :annotation:

   .. code-block:: text

      {<Intrinsic.INTEGER: 1>: <class 'int'>,
       <Intrinsic.REAL: 2>: <class 'float'>,
       <Intrinsic.BOOLEAN: 3>: <class 'bool'>,
       <Intrinsic.CHARACTER: 4>: <class 'str'>}
