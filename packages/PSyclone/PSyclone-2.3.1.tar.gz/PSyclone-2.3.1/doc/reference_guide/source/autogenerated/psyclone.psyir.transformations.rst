==================================
``psyclone.psyir.transformations``
==================================

.. automodule:: psyclone.psyir.transformations

   .. contents::
      :local:


Submodules
==========

.. toctree::

   psyclone.psyir.transformations.arrayrange2loop_trans
   psyclone.psyir.transformations.chunk_loop_trans
   psyclone.psyir.transformations.extract_trans
   psyclone.psyir.transformations.fold_conditional_return_expressions_trans
   psyclone.psyir.transformations.hoist_local_arrays_trans
   psyclone.psyir.transformations.hoist_trans
   psyclone.psyir.transformations.intrinsics
   psyclone.psyir.transformations.loop_fuse_trans
   psyclone.psyir.transformations.loop_swap_trans
   psyclone.psyir.transformations.loop_tiling_2d_trans
   psyclone.psyir.transformations.loop_trans
   psyclone.psyir.transformations.nan_test_trans
   psyclone.psyir.transformations.omp_taskwait_trans
   psyclone.psyir.transformations.profile_trans
   psyclone.psyir.transformations.psy_data_trans
   psyclone.psyir.transformations.read_only_verify_trans
   psyclone.psyir.transformations.region_trans
   psyclone.psyir.transformations.transformation_error

.. currentmodule:: psyclone.psyir.transformations


Classes
=======

- :py:class:`ArrayRange2LoopTrans`:
  Provides a transformation from a PSyIR Array Range to a PSyIR

- :py:class:`ChunkLoopTrans`:
  Apply a chunking transformation to a loop (in order to permit a

- :py:class:`ExtractTrans`:
  This transformation inserts an ExtractNode or a node derived

- :py:class:`FoldConditionalReturnExpressionsTrans`:
  Provides a transformation that folds conditional expressions with only

- :py:class:`HoistLocalArraysTrans`:
  This transformation takes a Routine and promotes any local, 'automatic'

- :py:class:`HoistTrans`:
  This transformation takes an assignment and moves it outside of

- :py:class:`Abs2CodeTrans`:
  Provides a transformation from a PSyIR ABS Operator node to

- :py:class:`DotProduct2CodeTrans`:
  Provides a transformation from a PSyIR DOT_PRODUCT Operator node to

- :py:class:`Matmul2CodeTrans`:
  Provides a transformation from a PSyIR MATMUL Operator node to

- :py:class:`Max2CodeTrans`:
  Provides a transformation from a PSyIR MAX Operator node to

- :py:class:`Min2CodeTrans`:
  Provides a transformation from a PSyIR MIN Operator node to

- :py:class:`Sign2CodeTrans`:
  Provides a transformation from a PSyIR SIGN Operator node to

- :py:class:`LoopFuseTrans`:
  Provides a generic loop-fuse transformation to two Nodes in the

- :py:class:`LoopSwapTrans`:
  Provides a loop-swap transformation, e.g.:

- :py:class:`LoopTiling2DTrans`:
  Apply a 2D loop tiling transformation to a loop. For example:

- :py:class:`LoopTrans`:
  This abstract class is a base class for all transformations that act

- :py:class:`NanTestTrans`:
  This transformation inserts a NanTestNode into the PSyIR of a

- :py:class:`OMPTaskwaitTrans`:
  Adds zero or more OpenMP Taskwait directives to an OMP parallel region.

- :py:class:`ProfileTrans`:
  Create a profile region around a list of statements. For

- :py:class:`PSyDataTrans`:
  Create a PSyData region around a list of statements. For

- :py:class:`ReadOnlyVerifyTrans`:
  This transformation inserts a ReadOnlyVerifyNode or a node derived

- :py:class:`RegionTrans`:
  This abstract class is a base class for all transformations that act


.. autoclass:: ArrayRange2LoopTrans
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: ArrayRange2LoopTrans
      :parts: 1

.. autoclass:: ChunkLoopTrans
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: ChunkLoopTrans
      :parts: 1

.. autoclass:: ExtractTrans
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: ExtractTrans
      :parts: 1

.. autoclass:: FoldConditionalReturnExpressionsTrans
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: FoldConditionalReturnExpressionsTrans
      :parts: 1

.. autoclass:: HoistLocalArraysTrans
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: HoistLocalArraysTrans
      :parts: 1

.. autoclass:: HoistTrans
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: HoistTrans
      :parts: 1

.. autoclass:: Abs2CodeTrans
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: Abs2CodeTrans
      :parts: 1

.. autoclass:: DotProduct2CodeTrans
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: DotProduct2CodeTrans
      :parts: 1

.. autoclass:: Matmul2CodeTrans
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: Matmul2CodeTrans
      :parts: 1

.. autoclass:: Max2CodeTrans
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: Max2CodeTrans
      :parts: 1

.. autoclass:: Min2CodeTrans
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: Min2CodeTrans
      :parts: 1

.. autoclass:: Sign2CodeTrans
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: Sign2CodeTrans
      :parts: 1

.. autoclass:: LoopFuseTrans
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LoopFuseTrans
      :parts: 1

.. autoclass:: LoopSwapTrans
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LoopSwapTrans
      :parts: 1

.. autoclass:: LoopTiling2DTrans
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LoopTiling2DTrans
      :parts: 1

.. autoclass:: LoopTrans
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LoopTrans
      :parts: 1

.. autoclass:: NanTestTrans
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: NanTestTrans
      :parts: 1

.. autoclass:: OMPTaskwaitTrans
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: OMPTaskwaitTrans
      :parts: 1

.. autoclass:: ProfileTrans
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: ProfileTrans
      :parts: 1

.. autoclass:: PSyDataTrans
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: PSyDataTrans
      :parts: 1

.. autoclass:: ReadOnlyVerifyTrans
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: ReadOnlyVerifyTrans
      :parts: 1

.. autoclass:: RegionTrans
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: RegionTrans
      :parts: 1


Exceptions
==========

- :py:exc:`TransformationError`:
  Provides a PSyclone-specific error class for errors found during


.. autoexception:: TransformationError

   .. rubric:: Inheritance
   .. inheritance-diagram:: TransformationError
      :parts: 1
