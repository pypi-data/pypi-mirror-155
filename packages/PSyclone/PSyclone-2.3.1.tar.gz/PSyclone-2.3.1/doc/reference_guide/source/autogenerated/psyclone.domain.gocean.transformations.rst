==========================================
``psyclone.domain.gocean.transformations``
==========================================

.. automodule:: psyclone.domain.gocean.transformations

   .. contents::
      :local:


Submodules
==========

.. toctree::

   psyclone.domain.gocean.transformations.gocean_const_loop_bounds_trans
   psyclone.domain.gocean.transformations.gocean_extract_trans
   psyclone.domain.gocean.transformations.gocean_loop_fuse_trans
   psyclone.domain.gocean.transformations.gocean_move_iteration_boundaries_inside_kernel_trans
   psyclone.domain.gocean.transformations.gocean_opencl_trans

.. currentmodule:: psyclone.domain.gocean.transformations


Classes
=======

- :py:class:`GOceanExtractTrans`:
  GOcean1.0 API application of ExtractTrans transformation     to extract code into a stand-alone program. For example:

- :py:class:`GOMoveIterationBoundariesInsideKernelTrans`:
  Provides a transformation that moves iteration boundaries that are

- :py:class:`GOceanLoopFuseTrans`:
  GOcean API specialisation of the :py:class:`base class <LoopFuseTrans>`

- :py:class:`GOOpenCLTrans`:
  Switches on/off the generation of an OpenCL PSy layer for a given

- :py:class:`GOConstLoopBoundsTrans`:
  Use of a common constant variable for each loop bound within


.. autoclass:: GOceanExtractTrans
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: GOceanExtractTrans
      :parts: 1

.. autoclass:: GOMoveIterationBoundariesInsideKernelTrans
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: GOMoveIterationBoundariesInsideKernelTrans
      :parts: 1

.. autoclass:: GOceanLoopFuseTrans
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: GOceanLoopFuseTrans
      :parts: 1

.. autoclass:: GOOpenCLTrans
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: GOOpenCLTrans
      :parts: 1

.. autoclass:: GOConstLoopBoundsTrans
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: GOConstLoopBoundsTrans
      :parts: 1
