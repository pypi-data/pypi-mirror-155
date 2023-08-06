========================================
``psyclone.domain.lfric.lfric_builtins``
========================================

.. automodule:: psyclone.domain.lfric.lfric_builtins

   .. contents::
      :local:

.. currentmodule:: psyclone.domain.lfric.lfric_builtins


Classes
=======

- :py:class:`LFRicBuiltInCallFactory`:
  Creates the necessary framework for a call to an LFRic built-in,

- :py:class:`LFRicBuiltIn`:
  Abstract base class for a node representing a call to an LFRic Built-in.

- :py:class:`LFRicXPlusYKern`:
  Add one, real-valued, field to another and return the result as

- :py:class:`LFRicIncXPlusYKern`:
  Add the second, real-valued, field to the first field and return it.

- :py:class:`LFRicAPlusXKern`:
  `Y = a + X` where `a` is a real scalar and `X` and `Y` are

- :py:class:`LFRicIncAPlusXKern`:
  `X = a + X` where `a` is a real scalar and `X` is a real-valued

- :py:class:`LFRicAXPlusYKern`:
  `Z = a*X + Y` where `a` is a real scalar and `Z`, `X` and

- :py:class:`LFRicIncAXPlusYKern`:
  `X = a*X + Y` where `a` is a real scalar and `X` and `Y` are

- :py:class:`LFRicIncXPlusBYKern`:
  `X = X + b*Y` where `b` is a real scalar and `X` and `Y` are

- :py:class:`LFRicAXPlusBYKern`:
  `Z = a*X + b*Y` where `a` and `b` are real scalars and `Z`, `X` and

- :py:class:`LFRicIncAXPlusBYKern`:
  `X = a*X + b*Y` where `a` and `b` are real scalars and `X` and `Y`

- :py:class:`LFRicAXPlusAYKern`:
  `Z = a*X + a*Y = a*(X + Y)` where `a` is a real scalar and `Z`,

- :py:class:`LFRicXMinusYKern`:
  Subtract one, real-valued, field from another and return the

- :py:class:`LFRicIncXMinusYKern`:
  Subtract the second, real-valued, field from the first field

- :py:class:`LFRicAMinusXKern`:
  `Y = a - X` where `a` is a real scalar and `X` and `Y` are real-valued

- :py:class:`LFRicIncAMinusXKern`:
  `X = a - X` where `a` is a real scalar and `X` is a real-valued

- :py:class:`LFRicXMinusAKern`:
  `Y = X - a` where `a` is a real scalar and `X` and `Y` are real-valued

- :py:class:`LFRicIncXMinusAKern`:
  `X = X - a` where `a` is a real scalar and `X` is a real-valued

- :py:class:`LFRicAXMinusYKern`:
  `Z = a*X - Y` where `a` is a real scalar and `Z`, `X` and

- :py:class:`LFRicXMinusBYKern`:
  `Z = X - b*Y` where `b` is a real scalar and `Z`, `X` and

- :py:class:`LFRicIncXMinusBYKern`:
  `X = X - b*Y` where `b` is a real scalar and `X` and `Y` are

- :py:class:`LFRicAXMinusBYKern`:
  `Z = a*X - b*Y` where `a` and `b` are real scalars and `Z`, `X` and

- :py:class:`LFRicXTimesYKern`:
  DoF-wise product of one, real-valued, field with another with

- :py:class:`LFRicIncXTimesYKern`:
  Multiply the first, real-valued, field by the second and return it.

- :py:class:`LFRicIncAXTimesYKern`:
  `X = a*X*Y` where `a` is a real scalar and `X` and `Y` are

- :py:class:`LFRicATimesXKern`:
  Multiply the first, real-valued, field by a real scalar and

- :py:class:`LFRicIncATimesXKern`:
  Multiply a real-valued field by a real scalar and return it.

- :py:class:`LFRicXDividebyYKern`:
  Divide the first, real-valued, field by the second and return

- :py:class:`LFRicIncXDividebyYKern`:
  Divide the first, real-valued, field by the second and return it.

- :py:class:`LFRicXDividebyAKern`:
  Divide a real-valued field by a real scalar and return the

- :py:class:`LFRicIncXDividebyAKern`:
  Divide a real-valued field by a real scalar and return it.

- :py:class:`LFRicADividebyXKern`:
  DoF-wise division of a scalar value `a` by the elements

- :py:class:`LFRicIncADividebyXKern`:
  DoF-wise division of a scalar value `a` by the elements

- :py:class:`LFRicIncXPowrealAKern`:
  Raise a real-valued field to a real power and return it.

- :py:class:`LFRicIncXPowintNKern`:
  Raise a real-valued field to an integer power and return it.

- :py:class:`LFRicSetvalCKern`:
  Set a real-valued field equal to a real scalar value.

- :py:class:`LFRicSetvalXKern`:
  Set a real-valued field equal to another, real-valued, field.

- :py:class:`LFRicXInnerproductYKern`:
  Calculates the inner product of two real-valued fields,

- :py:class:`LFRicXInnerproductXKern`:
  Calculates the inner product of one real-valued field by itself,

- :py:class:`LFRicSumXKern`:
  Computes the sum of the elements of a real-valued field.

- :py:class:`LFRicSignXKern`:
  Returns the sign of a real-valued field elements using the

- :py:class:`LFRicMaxAXKern`:
  Returns the maximum of a real scalar and real-valued field

- :py:class:`LFRicIncMaxAXKern`:
  Returns the maximum of a real scalar and real-valued field

- :py:class:`LFRicMinAXKern`:
  Returns the minimum of a real scalar and real-valued field

- :py:class:`LFRicIncMinAXKern`:
  Returns the minimum of a real scalar and real-valued field

- :py:class:`LFRicIntXKern`:
  Converts real-valued field elements to integer-valued

- :py:class:`LFRicIntXPlusYKern`:
  Add corresponding elements of two, integer-valued, fields, `X`

- :py:class:`LFRicIntIncXPlusYKern`:
  Add each element of an integer-valued field, `X`, to the

- :py:class:`LFRicIntAPlusXKern`:
  Add an integer scalar value, `a`, to each element of an

- :py:class:`LFRicIntIncAPlusXKern`:
  Add an integer scalar value, `a`, to each element of an

- :py:class:`LFRicIntXMinusYKern`:
  Subtract each element of an integer-valued field, `Y`, from

- :py:class:`LFRicIntIncXMinusYKern`:
  Subtract each element of an integer-valued field, `Y`, from

- :py:class:`LFRicIntAMinusXKern`:
  Subtract each element of an integer-valued field, `X`, from

- :py:class:`LFRicIntIncAMinusXKern`:
  Subtract each element of an integer-valued field, `X`, from

- :py:class:`LFRicIntXMinusAKern`:
  Subtract an integer scalar value, `a`, from each element of an

- :py:class:`LFRicIntIncXMinusAKern`:
  Subtract an integer scalar value, `a`, from each element of an

- :py:class:`LFRicIntXTimesYKern`:
  Multiply each element of one, integer-valued, field, `X`, by

- :py:class:`LFRicIntIncXTimesYKern`:
  Multiply each element of one, integer-valued, field, `X`, by

- :py:class:`LFRicIntATimesXKern`:
  Multiply each element of the first, integer-valued, field, `X`,

- :py:class:`LFRicIntIncATimesXKern`:
  Multiply each element of an integer-valued field, `X` by

- :py:class:`LFRicIntSetvalCKern`:
  Assign a single constant integer scalar value, `c`, to all

- :py:class:`LFRicIntSetvalXKern`:
  Copy one element of an integer-valued field (second argument),

- :py:class:`LFRicIntSignXKern`:
  Returns the sign of an integer-valued field elements using the

- :py:class:`LFRicIntMaxAXKern`:
  Returns the maximum of an integer scalar and integer-valued

- :py:class:`LFRicIntIncMaxAXKern`:
  Returns the maximum of an integer scalar and integer-valued

- :py:class:`LFRicIntMinAXKern`:
  Returns the minimum of an integer scalar and integer-valued

- :py:class:`LFRicIntIncMinAXKern`:
  Returns the minimum of an integer scalar and integer-valued

- :py:class:`LFRicRealXKern`:
  Converts integer-valued field elements to real-valued


.. autoclass:: LFRicBuiltInCallFactory
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LFRicBuiltInCallFactory
      :parts: 1

.. autoclass:: LFRicBuiltIn
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LFRicBuiltIn
      :parts: 1

.. autoclass:: LFRicXPlusYKern
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LFRicXPlusYKern
      :parts: 1

.. autoclass:: LFRicIncXPlusYKern
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LFRicIncXPlusYKern
      :parts: 1

.. autoclass:: LFRicAPlusXKern
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LFRicAPlusXKern
      :parts: 1

.. autoclass:: LFRicIncAPlusXKern
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LFRicIncAPlusXKern
      :parts: 1

.. autoclass:: LFRicAXPlusYKern
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LFRicAXPlusYKern
      :parts: 1

.. autoclass:: LFRicIncAXPlusYKern
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LFRicIncAXPlusYKern
      :parts: 1

.. autoclass:: LFRicIncXPlusBYKern
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LFRicIncXPlusBYKern
      :parts: 1

.. autoclass:: LFRicAXPlusBYKern
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LFRicAXPlusBYKern
      :parts: 1

.. autoclass:: LFRicIncAXPlusBYKern
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LFRicIncAXPlusBYKern
      :parts: 1

.. autoclass:: LFRicAXPlusAYKern
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LFRicAXPlusAYKern
      :parts: 1

.. autoclass:: LFRicXMinusYKern
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LFRicXMinusYKern
      :parts: 1

.. autoclass:: LFRicIncXMinusYKern
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LFRicIncXMinusYKern
      :parts: 1

.. autoclass:: LFRicAMinusXKern
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LFRicAMinusXKern
      :parts: 1

.. autoclass:: LFRicIncAMinusXKern
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LFRicIncAMinusXKern
      :parts: 1

.. autoclass:: LFRicXMinusAKern
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LFRicXMinusAKern
      :parts: 1

.. autoclass:: LFRicIncXMinusAKern
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LFRicIncXMinusAKern
      :parts: 1

.. autoclass:: LFRicAXMinusYKern
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LFRicAXMinusYKern
      :parts: 1

.. autoclass:: LFRicXMinusBYKern
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LFRicXMinusBYKern
      :parts: 1

.. autoclass:: LFRicIncXMinusBYKern
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LFRicIncXMinusBYKern
      :parts: 1

.. autoclass:: LFRicAXMinusBYKern
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LFRicAXMinusBYKern
      :parts: 1

.. autoclass:: LFRicXTimesYKern
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LFRicXTimesYKern
      :parts: 1

.. autoclass:: LFRicIncXTimesYKern
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LFRicIncXTimesYKern
      :parts: 1

.. autoclass:: LFRicIncAXTimesYKern
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LFRicIncAXTimesYKern
      :parts: 1

.. autoclass:: LFRicATimesXKern
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LFRicATimesXKern
      :parts: 1

.. autoclass:: LFRicIncATimesXKern
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LFRicIncATimesXKern
      :parts: 1

.. autoclass:: LFRicXDividebyYKern
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LFRicXDividebyYKern
      :parts: 1

.. autoclass:: LFRicIncXDividebyYKern
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LFRicIncXDividebyYKern
      :parts: 1

.. autoclass:: LFRicXDividebyAKern
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LFRicXDividebyAKern
      :parts: 1

.. autoclass:: LFRicIncXDividebyAKern
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LFRicIncXDividebyAKern
      :parts: 1

.. autoclass:: LFRicADividebyXKern
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LFRicADividebyXKern
      :parts: 1

.. autoclass:: LFRicIncADividebyXKern
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LFRicIncADividebyXKern
      :parts: 1

.. autoclass:: LFRicIncXPowrealAKern
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LFRicIncXPowrealAKern
      :parts: 1

.. autoclass:: LFRicIncXPowintNKern
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LFRicIncXPowintNKern
      :parts: 1

.. autoclass:: LFRicSetvalCKern
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LFRicSetvalCKern
      :parts: 1

.. autoclass:: LFRicSetvalXKern
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LFRicSetvalXKern
      :parts: 1

.. autoclass:: LFRicXInnerproductYKern
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LFRicXInnerproductYKern
      :parts: 1

.. autoclass:: LFRicXInnerproductXKern
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LFRicXInnerproductXKern
      :parts: 1

.. autoclass:: LFRicSumXKern
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LFRicSumXKern
      :parts: 1

.. autoclass:: LFRicSignXKern
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LFRicSignXKern
      :parts: 1

.. autoclass:: LFRicMaxAXKern
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LFRicMaxAXKern
      :parts: 1

.. autoclass:: LFRicIncMaxAXKern
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LFRicIncMaxAXKern
      :parts: 1

.. autoclass:: LFRicMinAXKern
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LFRicMinAXKern
      :parts: 1

.. autoclass:: LFRicIncMinAXKern
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LFRicIncMinAXKern
      :parts: 1

.. autoclass:: LFRicIntXKern
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LFRicIntXKern
      :parts: 1

.. autoclass:: LFRicIntXPlusYKern
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LFRicIntXPlusYKern
      :parts: 1

.. autoclass:: LFRicIntIncXPlusYKern
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LFRicIntIncXPlusYKern
      :parts: 1

.. autoclass:: LFRicIntAPlusXKern
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LFRicIntAPlusXKern
      :parts: 1

.. autoclass:: LFRicIntIncAPlusXKern
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LFRicIntIncAPlusXKern
      :parts: 1

.. autoclass:: LFRicIntXMinusYKern
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LFRicIntXMinusYKern
      :parts: 1

.. autoclass:: LFRicIntIncXMinusYKern
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LFRicIntIncXMinusYKern
      :parts: 1

.. autoclass:: LFRicIntAMinusXKern
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LFRicIntAMinusXKern
      :parts: 1

.. autoclass:: LFRicIntIncAMinusXKern
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LFRicIntIncAMinusXKern
      :parts: 1

.. autoclass:: LFRicIntXMinusAKern
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LFRicIntXMinusAKern
      :parts: 1

.. autoclass:: LFRicIntIncXMinusAKern
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LFRicIntIncXMinusAKern
      :parts: 1

.. autoclass:: LFRicIntXTimesYKern
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LFRicIntXTimesYKern
      :parts: 1

.. autoclass:: LFRicIntIncXTimesYKern
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LFRicIntIncXTimesYKern
      :parts: 1

.. autoclass:: LFRicIntATimesXKern
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LFRicIntATimesXKern
      :parts: 1

.. autoclass:: LFRicIntIncATimesXKern
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LFRicIntIncATimesXKern
      :parts: 1

.. autoclass:: LFRicIntSetvalCKern
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LFRicIntSetvalCKern
      :parts: 1

.. autoclass:: LFRicIntSetvalXKern
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LFRicIntSetvalXKern
      :parts: 1

.. autoclass:: LFRicIntSignXKern
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LFRicIntSignXKern
      :parts: 1

.. autoclass:: LFRicIntMaxAXKern
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LFRicIntMaxAXKern
      :parts: 1

.. autoclass:: LFRicIntIncMaxAXKern
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LFRicIntIncMaxAXKern
      :parts: 1

.. autoclass:: LFRicIntMinAXKern
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LFRicIntMinAXKern
      :parts: 1

.. autoclass:: LFRicIntIncMinAXKern
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LFRicIntIncMinAXKern
      :parts: 1

.. autoclass:: LFRicRealXKern
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LFRicRealXKern
      :parts: 1
