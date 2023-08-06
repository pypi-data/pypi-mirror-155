=========================
``psyclone.domain.lfric``
=========================

.. automodule:: psyclone.domain.lfric

   .. contents::
      :local:


Submodules
==========

.. toctree::

   psyclone.domain.lfric.algorithm
   psyclone.domain.lfric.arg_ordering
   psyclone.domain.lfric.function_space
   psyclone.domain.lfric.kern_call_acc_arg_list
   psyclone.domain.lfric.kern_call_arg_list
   psyclone.domain.lfric.kern_stub_arg_list
   psyclone.domain.lfric.kernel_interface
   psyclone.domain.lfric.lfric_arg_descriptor
   psyclone.domain.lfric.lfric_builtins
   psyclone.domain.lfric.lfric_constants
   psyclone.domain.lfric.psyir
   psyclone.domain.lfric.transformations

.. currentmodule:: psyclone.domain.lfric


Classes
=======

- :py:class:`ArgOrdering`:
  Base class capturing the arguments, type and ordering of data in

- :py:class:`FunctionSpace`:
  Manages the name of a function space. If it is an any_space or

- :py:class:`KernCallAccArgList`:
  Kernel call arguments that need to be declared by OpenACC

- :py:class:`KernCallArgList`:
  Creates the argument list required to call kernel "kern" from the

- :py:class:`KernelInterface`:
  Create the kernel arguments for the supplied kernel as specified by

- :py:class:`KernStubArgList`:
  Creates the argument list required to create and declare the

- :py:class:`LFRicArgDescriptor`:
  This class captures the information specified in one of LFRic API argument

- :py:class:`LFRicConstants`:
  This class stores all LFRic constants. Note that some constants


.. autoclass:: ArgOrdering
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: ArgOrdering
      :parts: 1

.. autoclass:: FunctionSpace
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: FunctionSpace
      :parts: 1

.. autoclass:: KernCallAccArgList
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: KernCallAccArgList
      :parts: 1

.. autoclass:: KernCallArgList
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: KernCallArgList
      :parts: 1

.. autoclass:: KernelInterface
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: KernelInterface
      :parts: 1

.. autoclass:: KernStubArgList
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: KernStubArgList
      :parts: 1

.. autoclass:: LFRicArgDescriptor
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LFRicArgDescriptor
      :parts: 1

.. autoclass:: LFRicConstants
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LFRicConstants
      :parts: 1
