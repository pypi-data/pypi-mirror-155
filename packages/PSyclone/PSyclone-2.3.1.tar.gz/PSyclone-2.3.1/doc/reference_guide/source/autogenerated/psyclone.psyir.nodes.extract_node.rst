=====================================
``psyclone.psyir.nodes.extract_node``
=====================================

.. automodule:: psyclone.psyir.nodes.extract_node

   .. contents::
      :local:

.. currentmodule:: psyclone.psyir.nodes.extract_node


Classes
=======

- :py:class:`ExtractNode`:
  This class can be inserted into a Schedule to mark Nodes for     code extraction using the ExtractRegionTrans transformation. By     applying the transformation the Nodes marked for extraction become     children of (the Schedule of) an ExtractNode.


.. autoclass:: ExtractNode
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: ExtractNode
      :parts: 1
