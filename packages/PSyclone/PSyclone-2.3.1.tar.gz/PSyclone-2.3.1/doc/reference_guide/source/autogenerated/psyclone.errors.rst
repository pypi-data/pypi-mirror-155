===================
``psyclone.errors``
===================

.. automodule:: psyclone.errors

   .. contents::
      :local:

.. currentmodule:: psyclone.errors


Classes
=======

- :py:class:`LazyString`:
  Utility that defers any computation associated with computing a


.. autoclass:: LazyString
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LazyString
      :parts: 1


Exceptions
==========

- :py:exc:`PSycloneError`:
  Provides a PSyclone specific error class as a generic parent class for

- :py:exc:`GenerationError`:
  Provides a PSyclone specific error class for errors found during PSy

- :py:exc:`FieldNotFoundError`:
  Provides a PSyclone-specific error class when a field with the

- :py:exc:`InternalError`:
  PSyclone-specific exception for use when an internal error occurs (i.e.


.. autoexception:: PSycloneError

   .. rubric:: Inheritance
   .. inheritance-diagram:: PSycloneError
      :parts: 1

.. autoexception:: GenerationError

   .. rubric:: Inheritance
   .. inheritance-diagram:: GenerationError
      :parts: 1

.. autoexception:: FieldNotFoundError

   .. rubric:: Inheritance
   .. inheritance-diagram:: FieldNotFoundError
      :parts: 1

.. autoexception:: InternalError

   .. rubric:: Inheritance
   .. inheritance-diagram:: InternalError
      :parts: 1
