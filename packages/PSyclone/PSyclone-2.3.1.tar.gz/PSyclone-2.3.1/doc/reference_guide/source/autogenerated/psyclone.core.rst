=================
``psyclone.core``
=================

.. automodule:: psyclone.core

   .. contents::
      :local:


Submodules
==========

.. toctree::

   psyclone.core.access_info
   psyclone.core.access_type
   psyclone.core.component_indices
   psyclone.core.signature
   psyclone.core.symbolic_maths

.. currentmodule:: psyclone.core


Classes
=======

- :py:class:`AccessInfo`:
  This class stores information about a single access

- :py:class:`AccessType`:
  A simple enum-class for the various valid access types.

- :py:class:`ComponentIndices`:
  This class stores index information for variable accesses. It stores

- :py:class:`Signature`:
  Given a variable access of the form ``a(i,j)%b(k,l)%c``, the signature

- :py:class:`SingleVariableAccessInfo`:
  This class stores a list with all accesses to one variable.

- :py:class:`SymbolicMaths`:
  A wrapper around the symbolic maths package 'sympy'. It

- :py:class:`VariablesAccessInfo`:
  This class stores all `SingleVariableAccessInfo` instances for all


.. autoclass:: AccessInfo
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: AccessInfo
      :parts: 1

.. autoclass:: AccessType
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: AccessType
      :parts: 1

.. autoclass:: ComponentIndices
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: ComponentIndices
      :parts: 1

.. autoclass:: Signature
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: Signature
      :parts: 1

.. autoclass:: SingleVariableAccessInfo
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: SingleVariableAccessInfo
      :parts: 1

.. autoclass:: SymbolicMaths
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: SymbolicMaths
      :parts: 1

.. autoclass:: VariablesAccessInfo
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: VariablesAccessInfo
      :parts: 1
