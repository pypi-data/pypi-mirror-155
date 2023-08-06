======================
``psyclone.dynamo0p3``
======================

.. automodule:: psyclone.dynamo0p3

   .. contents::
      :local:

.. currentmodule:: psyclone.dynamo0p3


Classes
=======

- :py:class:`DynFuncDescriptor03`:
  The Dynamo 0.3 API includes a function-space descriptor as

- :py:class:`DynKernMetadata`:
  Captures the Kernel subroutine code and metadata describing

- :py:class:`DynamoPSy`:
  The LFRic-specific PSy class. This creates an LFRic-specific

- :py:class:`DynamoInvokes`:
  The Dynamo specific invokes class. This passes the Dynamo

- :py:class:`DynCollection`:
  Base class for managing the declaration and initialisation of a

- :py:class:`DynStencils`:
  Stencil information and code generation associated with a PSy-layer

- :py:class:`DynDofmaps`:
  Holds all information on the dofmaps (including column-banded and

- :py:class:`DynFunctionSpaces`:
  Handles the declaration and initialisation of all function-space-related

- :py:class:`LFRicFields`:
  Manages the declarations for all field arguments required by an Invoke

- :py:class:`DynProxies`:
  Handles all proxy-related declarations and initialisation. Unlike other

- :py:class:`DynCellIterators`:
  Handles all entities required by kernels that operate on cell-columns.

- :py:class:`LFRicScalarArgs`:
  Handles the declarations of scalar kernel arguments appearing in either

- :py:class:`DynLMAOperators`:
  Handles all entities associated with Local-Matrix-Assembly Operators.

- :py:class:`DynCMAOperators`:
  Holds all information on the Column-Matrix-Assembly operators

- :py:class:`DynMeshes`:
  Holds all mesh-related information (including colour maps if

- :py:class:`DynInterGrid`:
  Holds information on quantities required by an inter-grid kernel.

- :py:class:`DynBasisFunctions`:
  Holds all information on the basis and differential basis

- :py:class:`DynBoundaryConditions`:
  Manages declarations and initialisation of quantities required by

- :py:class:`DynInvoke`:
  The Dynamo specific invoke class. This passes the Dynamo specific

- :py:class:`DynInvokeSchedule`:
  The Dynamo specific InvokeSchedule sub-class. This passes the Dynamo-

- :py:class:`DynGlobalSum`:
  Dynamo specific global sum class which can be added to and

- :py:class:`DynHaloExchange`:
  Dynamo specific halo exchange class which can be added to and

- :py:class:`DynHaloExchangeStart`:
  The start of an asynchronous halo exchange. This is similar to a

- :py:class:`DynHaloExchangeEnd`:
  The end of an asynchronous halo exchange. This is similar to a

- :py:class:`HaloDepth`:
  Determines how much of the halo a read to a field accesses (the

- :py:class:`HaloWriteAccess`:
  Determines how much of a field's halo is written to (the halo depth)

- :py:class:`HaloReadAccess`:
  Determines how much of a field's halo is read (the halo depth) and

- :py:class:`DynLoop`:
  The LFRic-specific PSyLoop class. This passes the LFRic-specific

- :py:class:`DynKern`:
  Stores information about Dynamo Kernels as specified by the

- :py:class:`FSDescriptor`:
  Provides information about a particular function space used by

- :py:class:`FSDescriptors`:
  Contains a collection of FSDescriptor objects and methods

- :py:class:`DynStencil`:
  Provides stencil information about a Dynamo argument 

- :py:class:`DynKernelArguments`:
  Provides information about Dynamo kernel call arguments

- :py:class:`DynKernelArgument`:
  This class provides information about individual LFRic kernel call

- :py:class:`DynKernCallFactory`:
  Create the necessary framework for a Dynamo kernel call.

- :py:class:`DynACCEnterDataDirective`:
  Sub-classes ACCEnterDataDirective to provide an API-specific implementation


.. autoclass:: DynFuncDescriptor03
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: DynFuncDescriptor03
      :parts: 1

.. autoclass:: DynKernMetadata
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: DynKernMetadata
      :parts: 1

.. autoclass:: DynamoPSy
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: DynamoPSy
      :parts: 1

.. autoclass:: DynamoInvokes
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: DynamoInvokes
      :parts: 1

.. autoclass:: DynCollection
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: DynCollection
      :parts: 1

.. autoclass:: DynStencils
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: DynStencils
      :parts: 1

.. autoclass:: DynDofmaps
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: DynDofmaps
      :parts: 1

.. autoclass:: DynFunctionSpaces
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: DynFunctionSpaces
      :parts: 1

.. autoclass:: LFRicFields
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LFRicFields
      :parts: 1

.. autoclass:: DynProxies
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: DynProxies
      :parts: 1

.. autoclass:: DynCellIterators
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: DynCellIterators
      :parts: 1

.. autoclass:: LFRicScalarArgs
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LFRicScalarArgs
      :parts: 1

.. autoclass:: DynLMAOperators
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: DynLMAOperators
      :parts: 1

.. autoclass:: DynCMAOperators
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: DynCMAOperators
      :parts: 1

.. autoclass:: DynMeshes
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: DynMeshes
      :parts: 1

.. autoclass:: DynInterGrid
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: DynInterGrid
      :parts: 1

.. autoclass:: DynBasisFunctions
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: DynBasisFunctions
      :parts: 1

.. autoclass:: DynBoundaryConditions
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: DynBoundaryConditions
      :parts: 1

.. autoclass:: DynInvoke
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: DynInvoke
      :parts: 1

.. autoclass:: DynInvokeSchedule
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: DynInvokeSchedule
      :parts: 1

.. autoclass:: DynGlobalSum
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: DynGlobalSum
      :parts: 1

.. autoclass:: DynHaloExchange
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: DynHaloExchange
      :parts: 1

.. autoclass:: DynHaloExchangeStart
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: DynHaloExchangeStart
      :parts: 1

.. autoclass:: DynHaloExchangeEnd
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: DynHaloExchangeEnd
      :parts: 1

.. autoclass:: HaloDepth
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: HaloDepth
      :parts: 1

.. autoclass:: HaloWriteAccess
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: HaloWriteAccess
      :parts: 1

.. autoclass:: HaloReadAccess
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: HaloReadAccess
      :parts: 1

.. autoclass:: DynLoop
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: DynLoop
      :parts: 1

.. autoclass:: DynKern
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: DynKern
      :parts: 1

.. autoclass:: FSDescriptor
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: FSDescriptor
      :parts: 1

.. autoclass:: FSDescriptors
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: FSDescriptors
      :parts: 1

.. autoclass:: DynStencil
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: DynStencil
      :parts: 1

.. autoclass:: DynKernelArguments
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: DynKernelArguments
      :parts: 1

.. autoclass:: DynKernelArgument
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: DynKernelArgument
      :parts: 1

.. autoclass:: DynKernCallFactory
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: DynKernCallFactory
      :parts: 1

.. autoclass:: DynACCEnterDataDirective
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: DynACCEnterDataDirective
      :parts: 1
