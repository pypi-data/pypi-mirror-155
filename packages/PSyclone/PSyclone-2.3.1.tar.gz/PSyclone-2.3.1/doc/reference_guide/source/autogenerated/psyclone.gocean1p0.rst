======================
``psyclone.gocean1p0``
======================

.. automodule:: psyclone.gocean1p0

   .. contents::
      :local:

.. currentmodule:: psyclone.gocean1p0


Classes
=======

- :py:class:`GOPSy`:
  The GOcean 1.0 specific PSy class. This creates a GOcean specific

- :py:class:`GOInvokes`:
  The GOcean specific invokes class. This passes the GOcean specific

- :py:class:`GOInvoke`:
  The GOcean specific invoke class. This passes the GOcean specific

- :py:class:`GOInvokeSchedule`:
  The GOcean specific InvokeSchedule sub-class. We call the base class

- :py:class:`GOLoop`:
  The GOcean specific PSyLoop class. This passes the GOcean specific

- :py:class:`GOBuiltInCallFactory`:
  A GOcean-specific built-in call factory. No built-ins

- :py:class:`GOKernCallFactory`:
  A GOcean-specific kernel-call factory. A standard kernel call in

- :py:class:`GOKern`:
  Stores information about GOcean Kernels as specified by the Kernel

- :py:class:`GOFparser2Reader`:
  Sub-classes the Fparser2Reader with GOcean 1.0 specific

- :py:class:`GOKernelArguments`:
  Provides information about GOcean kernel-call arguments

- :py:class:`GOKernelArgument`:
  Provides information about individual GOcean kernel call arguments

- :py:class:`GOKernelGridArgument`:
  Describes arguments that supply grid properties to a kernel.

- :py:class:`GOStencil`:
  GOcean 1.0 stencil information for a kernel argument as obtained by

- :py:class:`GO1p0Descriptor`:
  Description of a GOcean 1.0 kernel argument, as obtained by

- :py:class:`GOKernelType1p0`:
  Description of a kernel including the grid index-offset it

- :py:class:`GOACCEnterDataDirective`:
  Sub-classes ACCEnterDataDirective to provide the dl_esm_inf infrastructure-

- :py:class:`GOSymbolTable`:
  Sub-classes SymbolTable to provide a GOcean-specific implementation.

- :py:class:`GOKernelSchedule`:
  Sub-classes KernelSchedule to provide a GOcean-specific implementation.

- :py:class:`GOHaloExchange`:
  GOcean specific halo exchange class which can be added to and


.. autoclass:: GOPSy
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: GOPSy
      :parts: 1

.. autoclass:: GOInvokes
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: GOInvokes
      :parts: 1

.. autoclass:: GOInvoke
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: GOInvoke
      :parts: 1

.. autoclass:: GOInvokeSchedule
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: GOInvokeSchedule
      :parts: 1

.. autoclass:: GOLoop
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: GOLoop
      :parts: 1

.. autoclass:: GOBuiltInCallFactory
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: GOBuiltInCallFactory
      :parts: 1

.. autoclass:: GOKernCallFactory
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: GOKernCallFactory
      :parts: 1

.. autoclass:: GOKern
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: GOKern
      :parts: 1

.. autoclass:: GOFparser2Reader
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: GOFparser2Reader
      :parts: 1

.. autoclass:: GOKernelArguments
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: GOKernelArguments
      :parts: 1

.. autoclass:: GOKernelArgument
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: GOKernelArgument
      :parts: 1

.. autoclass:: GOKernelGridArgument
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: GOKernelGridArgument
      :parts: 1

.. autoclass:: GOStencil
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: GOStencil
      :parts: 1

.. autoclass:: GO1p0Descriptor
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: GO1p0Descriptor
      :parts: 1

.. autoclass:: GOKernelType1p0
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: GOKernelType1p0
      :parts: 1

.. autoclass:: GOACCEnterDataDirective
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: GOACCEnterDataDirective
      :parts: 1

.. autoclass:: GOSymbolTable
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: GOSymbolTable
      :parts: 1

.. autoclass:: GOKernelSchedule
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: GOKernelSchedule
      :parts: 1

.. autoclass:: GOHaloExchange
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: GOHaloExchange
      :parts: 1
