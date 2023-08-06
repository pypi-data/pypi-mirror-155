==========================
``psyclone.configuration``
==========================

.. automodule:: psyclone.configuration

   .. contents::
      :local:

.. currentmodule:: psyclone.configuration


Classes
=======

- :py:class:`APISpecificConfig`:
  A base class for functions that each API-specific class must provide.

- :py:class:`Config`:
  Handles all configuration management. It is implemented as a singleton

- :py:class:`LFRicConfig`:
  LFRic-specific (Dynamo 0.3) Config sub-class. Holds configuration options

- :py:class:`GOceanConfig`:
  Gocean1.0-specific Config sub-class. Holds configuration options

- :py:class:`NemoConfig`:
  Nemo-specific Config sub-class. Holds configuration options


.. autoclass:: APISpecificConfig
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: APISpecificConfig
      :parts: 1

.. autoclass:: Config
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: Config
      :parts: 1

.. autoclass:: LFRicConfig
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: LFRicConfig
      :parts: 1

.. autoclass:: GOceanConfig
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: GOceanConfig
      :parts: 1

.. autoclass:: NemoConfig
   :members:

   .. rubric:: Inheritance
   .. inheritance-diagram:: NemoConfig
      :parts: 1


Exceptions
==========

- :py:exc:`ConfigurationError`:
  Class for all configuration-related errors.


.. autoexception:: ConfigurationError

   .. rubric:: Inheritance
   .. inheritance-diagram:: ConfigurationError
      :parts: 1
