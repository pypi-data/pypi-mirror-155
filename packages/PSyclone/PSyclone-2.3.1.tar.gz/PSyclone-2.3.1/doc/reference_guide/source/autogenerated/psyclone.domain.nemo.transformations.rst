========================================
``psyclone.domain.nemo.transformations``
========================================

.. automodule:: psyclone.domain.nemo.transformations

   .. contents::
      :local:


Submodules
==========

.. toctree::

   psyclone.domain.nemo.transformations.create_nemo_invoke_schedule_trans
   psyclone.domain.nemo.transformations.create_nemo_kernel_trans
   psyclone.domain.nemo.transformations.create_nemo_loop_trans
   psyclone.domain.nemo.transformations.create_nemo_psy_trans
   psyclone.domain.nemo.transformations.nemo_allarrayaccess2loop_trans
   psyclone.domain.nemo.transformations.nemo_allarrayrange2loop_trans
   psyclone.domain.nemo.transformations.nemo_arrayaccess2loop_trans
   psyclone.domain.nemo.transformations.nemo_arrayrange2loop_trans
   psyclone.domain.nemo.transformations.nemo_loop_fuse
   psyclone.domain.nemo.transformations.nemo_outerarrayrange2loop_trans

.. currentmodule:: psyclone.domain.nemo.transformations


Classes
=======

- :py:class:`CreateNemoInvokeScheduleTrans`:
  Transform a generic PSyIR Routine into a NEMO InvokeSchedule.

- :py:class:`CreateNemoKernelTrans`:
  Transform a generic PSyIR Schedule representing a loop body into a NEMO

- :py:class:`CreateNemoLoopTrans`:
  Transform a generic PSyIR Loop into a NemoLoop. For example:

- :py:class:`CreateNemoPSyTrans`:
  Transform generic (language-level) PSyIR representation into a PSyclone

- :py:class:`NemoAllArrayRange2LoopTrans`:
  Provides a transformation for all PSyIR Array Ranges in an

- :py:class:`NemoArrayRange2LoopTrans`:
  Provides a transformation from a PSyIR ArrayReference Range to a

- :py:class:`NemoLoopFuseTrans`:
  NEMO-specific implementation of the loop fusion transformation.

- :py:class:`NemoOuterArrayRange2LoopTrans`:
  Provides a transformation from the outermost PSyIR ArrayReference

- :py:class:`NemoArrayAccess2LoopTrans`:
  Provides a transformation to transform a constant index access to

- :py:class:`NemoAllArrayAccess2LoopTrans`:
  Provides a transformation from a PSyIR Assignment containing


.. autoclass:: CreateNemoInvokeScheduleTrans
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: CreateNemoInvokeScheduleTrans
      :parts: 1

.. autoclass:: CreateNemoKernelTrans
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: CreateNemoKernelTrans
      :parts: 1

.. autoclass:: CreateNemoLoopTrans
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: CreateNemoLoopTrans
      :parts: 1

.. autoclass:: CreateNemoPSyTrans
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: CreateNemoPSyTrans
      :parts: 1

.. autoclass:: NemoAllArrayRange2LoopTrans
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: NemoAllArrayRange2LoopTrans
      :parts: 1

.. autoclass:: NemoArrayRange2LoopTrans
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: NemoArrayRange2LoopTrans
      :parts: 1

.. autoclass:: NemoLoopFuseTrans
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: NemoLoopFuseTrans
      :parts: 1

.. autoclass:: NemoOuterArrayRange2LoopTrans
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: NemoOuterArrayRange2LoopTrans
      :parts: 1

.. autoclass:: NemoArrayAccess2LoopTrans
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: NemoArrayAccess2LoopTrans
      :parts: 1

.. autoclass:: NemoAllArrayAccess2LoopTrans
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: NemoAllArrayAccess2LoopTrans
      :parts: 1
