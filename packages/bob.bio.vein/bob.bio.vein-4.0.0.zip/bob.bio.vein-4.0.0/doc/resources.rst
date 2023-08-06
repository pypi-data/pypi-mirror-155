.. vim: set fileencoding=utf-8 :
.. Mon 11 Jul 2016 16:39:15 CEST


.. _bob.bio.vein.resources:

===========
 Resources
===========

This section contains a listing of all ready-to-use resources you can find in
this package. Each module may contain references different resource types,
including ``database``, ``preprocessor``, ``extractor`` and ``algorithm``. By
combining *complementary* resources, you can run baseline experiments as
explained on :ref:`bob.bio.vein.baselines`.


.. _bob.bio.vein.resources.databases:

Databases
---------

These resources represent configuration files containing at least settings for
the following runtime attributes of ``verify.py``:

  * ``database``
  * ``protocol``


.. _bob.bio.vein.resources.database.utfvp:

UTFVP Database
==============

.. .. automodule:: bob.bio.vein.config.database.utfvp
..    :members:


.. _bob.bio.vein.resources.recognition:

Recognition Systems
-------------------

These resources represent configuration files containing at least settings for
the following runtime attributes of ``verify.py``:

  * ``sub_directory``
  * ``preprocessor``
  * ``extractor``
  * ``algorithm``


.. _bob.bio.vein.resources.recognition.rlt:

Repeated Line Tracking and Miura Matching
=========================================

.. automodule:: bob.bio.vein.config.repeated_line_tracking
   :members:


.. _bob.bio.vein.resources.recognition.mc:

Maximum Curvature and Miura Matching
====================================

.. automodule:: bob.bio.vein.config.maximum_curvature
   :members:


.. _bob.bio.vein.resources.recognition.wld:

Wide-Line Detector and Miura Matching
=====================================

.. automodule:: bob.bio.vein.config.wide_line_detector
   :members:
