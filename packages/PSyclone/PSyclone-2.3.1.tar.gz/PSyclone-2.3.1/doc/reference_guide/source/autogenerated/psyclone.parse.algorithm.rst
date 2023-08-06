============================
``psyclone.parse.algorithm``
============================

.. automodule:: psyclone.parse.algorithm

   .. contents::
      :local:

.. currentmodule:: psyclone.parse.algorithm


Functions
=========

- :py:func:`parse`:
  Takes a PSyclone conformant algorithm file as input and outputs a

- :py:func:`get_builtin_defs`:
  Get the names of the supported built-in operations and the file

- :py:func:`get_invoke_label`:
  Takes an invoke argument contained in the parse_tree argument and

- :py:func:`get_kernel`:
  Takes the parse tree of an invoke kernel argument and returns the

- :py:func:`create_var_name`:
  Creates a valid variable name from an argument that optionally


.. autofunction:: parse

.. autofunction:: get_builtin_defs

.. autofunction:: get_invoke_label

.. autofunction:: get_kernel

.. autofunction:: create_var_name


Classes
=======

- :py:class:`Parser`:
  Supports the parsing of PSyclone conformant algorithm code within a

- :py:class:`FileInfo`:
  Captures information about the algorithm file and the invoke calls

- :py:class:`InvokeCall`:
  Keeps information about an individual invoke call.

- :py:class:`ParsedCall`:
  Base class for information about a user-supplied or built-in

- :py:class:`KernelCall`:
  Store information about a user-supplied (coded) kernel. Specialises

- :py:class:`BuiltInCall`:
  Store information about a system-supplied (builtin)

- :py:class:`Arg`:
  Description of an argument as obtained from parsing kernel or


.. autoclass:: Parser
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: Parser
      :parts: 1

.. autoclass:: FileInfo
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: FileInfo
      :parts: 1

.. autoclass:: InvokeCall
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: InvokeCall
      :parts: 1

.. autoclass:: ParsedCall
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: ParsedCall
      :parts: 1

.. autoclass:: KernelCall
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: KernelCall
      :parts: 1

.. autoclass:: BuiltInCall
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: BuiltInCall
      :parts: 1

.. autoclass:: Arg
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: Arg
      :parts: 1
