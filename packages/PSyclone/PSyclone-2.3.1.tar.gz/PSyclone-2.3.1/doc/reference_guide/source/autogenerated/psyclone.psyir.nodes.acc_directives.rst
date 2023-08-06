=======================================
``psyclone.psyir.nodes.acc_directives``
=======================================

.. automodule:: psyclone.psyir.nodes.acc_directives

   .. contents::
      :local:

.. currentmodule:: psyclone.psyir.nodes.acc_directives


Classes
=======

- :py:class:`ACCRegionDirective`:
  Base class for all OpenACC region directive statements. 

- :py:class:`ACCEnterDataDirective`:
  Class representing a "!$ACC enter data" OpenACC directive in

- :py:class:`ACCParallelDirective`:
  Class representing the !$ACC PARALLEL directive of OpenACC

- :py:class:`ACCLoopDirective`:
  Class managing the creation of a '!$acc loop' OpenACC directive.

- :py:class:`ACCKernelsDirective`:
  Class representing the !$ACC KERNELS directive in the PSyIR.

- :py:class:`ACCDataDirective`:
  Class representing the !$ACC DATA ... !$ACC END DATA directive

- :py:class:`ACCUpdateDirective`:
  Class representing the !$ACC UPDATE directive of OpenACC in the PSyIR.

- :py:class:`ACCStandaloneDirective`:
  Base class for all standalone OpenACC directive statements. 

- :py:class:`ACCDirective`:
  Base mixin class for all OpenACC directive statements.

- :py:class:`ACCRoutineDirective`:
  Class representing a "!$ACC routine" OpenACC directive in PSyIR. 


.. autoclass:: ACCRegionDirective
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: ACCRegionDirective
      :parts: 1

.. autoclass:: ACCEnterDataDirective
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: ACCEnterDataDirective
      :parts: 1

.. autoclass:: ACCParallelDirective
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: ACCParallelDirective
      :parts: 1

.. autoclass:: ACCLoopDirective
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: ACCLoopDirective
      :parts: 1

.. autoclass:: ACCKernelsDirective
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: ACCKernelsDirective
      :parts: 1

.. autoclass:: ACCDataDirective
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: ACCDataDirective
      :parts: 1

.. autoclass:: ACCUpdateDirective
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: ACCUpdateDirective
      :parts: 1

.. autoclass:: ACCStandaloneDirective
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: ACCStandaloneDirective
      :parts: 1

.. autoclass:: ACCDirective
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: ACCDirective
      :parts: 1

.. autoclass:: ACCRoutineDirective
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: ACCRoutineDirective
      :parts: 1
