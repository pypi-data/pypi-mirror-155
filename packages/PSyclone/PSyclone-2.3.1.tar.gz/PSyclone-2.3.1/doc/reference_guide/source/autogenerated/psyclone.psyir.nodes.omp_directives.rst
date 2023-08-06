=======================================
``psyclone.psyir.nodes.omp_directives``
=======================================

.. automodule:: psyclone.psyir.nodes.omp_directives

   .. contents::
      :local:

.. currentmodule:: psyclone.psyir.nodes.omp_directives


Classes
=======

- :py:class:`OMPRegionDirective`:
  Base class for all OpenMP region-related directives.

- :py:class:`OMPParallelDirective`:
  Class representing an OpenMP Parallel directive. 

- :py:class:`OMPSingleDirective`:
  Class representing an OpenMP SINGLE directive in the PSyIR.

- :py:class:`OMPMasterDirective`:
  Class representing an OpenMP MASTER directive in the PSyclone AST.

- :py:class:`OMPDoDirective`:
  Class representing an OpenMP DO directive in the PSyIR.

- :py:class:`OMPParallelDoDirective`:
  Class for the !$OMP PARALLEL DO directive. This inherits from

- :py:class:`OMPSerialDirective`:
  Abstract class representing OpenMP serial regions, e.g.

- :py:class:`OMPTaskloopDirective`:
  Class representing an OpenMP TASKLOOP directive in the PSyIR.

- :py:class:`OMPTargetDirective`:
  Class for the !$OMP TARGET directive that offloads the code contained

- :py:class:`OMPTaskwaitDirective`:
  Class representing an OpenMP TASKWAIT directive in the PSyIR.

- :py:class:`OMPDirective`:
  Base mixin class for all OpenMP-related directives.

- :py:class:`OMPStandaloneDirective`:
  Base class for all OpenMP-related standalone directives

- :py:class:`OMPLoopDirective`:
  Class for the !$OMP LOOP directive that specifies that the iterations

- :py:class:`OMPDeclareTargetDirective`:
  Class representing an OpenMP Declare Target directive in the PSyIR.


.. autoclass:: OMPRegionDirective
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: OMPRegionDirective
      :parts: 1

.. autoclass:: OMPParallelDirective
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: OMPParallelDirective
      :parts: 1

.. autoclass:: OMPSingleDirective
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: OMPSingleDirective
      :parts: 1

.. autoclass:: OMPMasterDirective
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: OMPMasterDirective
      :parts: 1

.. autoclass:: OMPDoDirective
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: OMPDoDirective
      :parts: 1

.. autoclass:: OMPParallelDoDirective
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: OMPParallelDoDirective
      :parts: 1

.. autoclass:: OMPSerialDirective
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: OMPSerialDirective
      :parts: 1

.. autoclass:: OMPTaskloopDirective
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: OMPTaskloopDirective
      :parts: 1

.. autoclass:: OMPTargetDirective
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: OMPTargetDirective
      :parts: 1

.. autoclass:: OMPTaskwaitDirective
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: OMPTaskwaitDirective
      :parts: 1

.. autoclass:: OMPDirective
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: OMPDirective
      :parts: 1

.. autoclass:: OMPStandaloneDirective
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: OMPStandaloneDirective
      :parts: 1

.. autoclass:: OMPLoopDirective
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: OMPLoopDirective
      :parts: 1

.. autoclass:: OMPDeclareTargetDirective
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: OMPDeclareTargetDirective
      :parts: 1
