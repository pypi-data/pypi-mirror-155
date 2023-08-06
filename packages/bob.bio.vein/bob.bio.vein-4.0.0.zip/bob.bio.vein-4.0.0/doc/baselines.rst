.. vim: set fileencoding=utf-8 :
.. date: Thu Sep 20 11:58:57 CEST 2012

.. _bob.bio.vein.baselines:

=============================
Executing Baseline Algorithms
=============================


In this section we introduce the baselines available in this pakcage.
To execute one of then in the databases available just run the following command::

$ bob bio pipeline simple [DATABASE_NAME] [BASELINE]

.. note::
  Both, `[DATABASE_NAME]` and `[BASELINE]` can be either python resources or
  python files.

  Please, refer to :ref:`bob.bio.base <bob.bio.base>` for more information.


Repeated Line-Tracking with Miura Matching
==========================================

Detailed description at :ref:`bob.bio.vein.resources.recognition.rlt`.

To run the baseline on the ``VERA fingervein`` database, using the ``Nom``
protocol (deprecated), do the following:


.. code-block:: sh

   $ bob bio pipeline simple verafinger rlt -vv -c


.. tip::

   If you have more processing cores on your local machine and don't want to
   submit your job for SGE execution, you can run it in parallel by adding the options ``-l local-parallel``.

   .. code-block:: sh

      $ bob bio pipeline simple verafinger rlt -vv -c -l local-parallel

   To run on the Idiap SGE grid use:

   .. code-block:: sh

      $ bob bio pipeline simple rlt -vv -c -l sge


This command line selects and runs the following implementations for the
toolchain:

* ``bob.bio.vein.resources.database.verafinger``
* :ref:`bob.bio.vein.resources.recognition.rlt`

As the tool runs, you'll see printouts that show how it advances through
preprocessing, feature extraction and matching. In a 4-core machine and using
4 parallel tasks, it takes around 4 hours to process this baseline with the
current code implementation.

To complete the evaluation, run the command bellow, that will output the equal
error rate (EER) and plot the detector error trade-off (DET) curve with the
performance:

.. code-block:: sh

   $ bob bio metrics <path-to>/verafinger/rlt/Nom/nonorm/scores-dev --no-evaluation
   [Min. criterion: EER ] Threshold on Development set `scores-dev`: 0.31835292
   ======  ========================
   None    Development scores-dev
   ======  ========================
   FtA     0.0%
   FMR     23.6% (11388/48180)
   FNMR    23.6% (52/220)
   FAR     23.6%
   FRR     23.6%
   HTER    23.6%
   ======  ========================


Maximum Curvature with Miura Matching
=====================================

Detailed description at :ref:`bob.bio.vein.resources.recognition.mc`.

To run the baseline on the ``VERA fingervein`` database, using the ``Nom``
protocol like above, do the following:


.. code-block:: sh

   $ bob bio pipeline simple verafinger mc -vv -c


This command line selects and runs the following implementations for the
toolchain:

* ``bob.bio.vein.resources.database.verafinger``
* :ref:`bob.bio.vein.resources.recognition.mc`

In a 4-core machine and using 4 parallel tasks, it takes around 1 hour and 40
minutes to process this baseline with the current code implementation. Results
we obtained:

.. code-block:: sh

   $ bob bio metrics <path-to>/verafinger/mc/Nom/nonorm/scores-dev --no-evaluation
   [Min. criterion: EER ] Threshold on Development set `scores-dev`: 7.372830e-02
   ======  ========================
   None    Development scores-dev
   ======  ========================
   FtA     0.0%
   FMR     4.4% (2116/48180)
   FNMR    4.5% (10/220)
   FAR     4.4%
   FRR     4.5%
   HTER    4.5%
   ======  ========================


Wide Line Detector with Miura Matching
======================================

You can find the description of this method on the paper from Huang *et al.*
[HDLTL10]_.

To run the baseline on the ``VERA fingervein`` database, using the ``Nom``
protocol like above, do the following:


.. code-block:: sh

   $ bob bio pipeline simple verafinger wld -vv -c


This command line selects and runs the following implementations for the
toolchain:

* ``bob.bio.vein.resources.database.verafinger``
* :ref:`bob.bio.vein.resources.recognition.wld`

In a 4-core machine and using 4 parallel tasks, it takes only around 5 minutes
minutes to process this baseline with the current code implementation.Results
we obtained:

.. code-block:: sh

   $ bob bio metrics <path-to>/verafinger/wld/Nom/nonorm/scores-dev --no-evaluation
   [Min. criterion: EER ] Threshold on Development set `scores-dev`: 2.402707e-01
   ======  ========================
   None    Development scores-dev
   ======  ========================
   FtA     0.0%
   FMR     9.8% (4726/48180)
   FNMR    10.0% (22/220)
   FAR     9.8%
   FRR     10.0%
   HTER    9.9%


Results for other Baselines
===========================

This package may generate results for other combinations of protocols and
databases. Here is a summary table for some variants (results expressed
correspond to the the equal-error rate on the development set, in percentage):

======================== ====== ====== ====== ====== ======
       Toolchain              Vera Finger         UTFVP
------------------------ -------------------- -------------
   Feature Extractor      Full     B    Nom   1vsall  nom
======================== ====== ====== ====== ====== ======
Repeated Line Tracking    14.6   13.4   23.6   3.4    1.4
Wide Line Detector         5.8    5.6    9.9   2.8    1.9
Maximum Curvature          2.5    1.4    4.5   0.9    0.4
======================== ====== ====== ====== ====== ======

In a machine with 48 cores, running these baselines took the following time
(hh:mm):

======================== ====== ====== ====== ====== ======
       Toolchain              Vera Finger         UTFVP
------------------------ -------------------- -------------
   Feature Extractor      Full     B    Nom   1vsall  nom
======================== ====== ====== ====== ====== ======
Repeated Line Tracking    01:16  00:23  00:23  12:44  00:35
Wide Line Detector        00:07  00:01  00:01  02:25  00:05
Maximum Curvature         03:28  00:54  00:59  58:34  01:48
======================== ====== ====== ====== ====== ======


Modifying Baseline Experiments
------------------------------

It is fairly easy to modify baseline experiments available in this package. To
do so, you must copy the configuration files for the given baseline you want to
modify, edit them to make the desired changes and run the experiment again.

For example, suppose you'd like to change the protocol on the Vera Fingervein
database and use the protocol ``full`` instead of the default protocol ``nom``.
First, you identify where the configuration file sits:

.. code-block:: sh

   $ resources.py -tc -p bob.bio.vein
   - bob.bio.vein X.Y.Z @ /path/to/bob.bio.vein:
     + mc         --> bob.bio.vein.configurations.maximum_curvature
     + parallel   --> bob.bio.vein.configurations.parallel
     + rlt        --> bob.bio.vein.configurations.repeated_line_tracking
     + utfvp      --> bob.bio.vein.configurations.utfvp
     + verafinger --> bob.bio.vein.configurations.verafinger
     + wld        --> bob.bio.vein.configurations.wide_line_detector


The listing above tells the ``verafinger`` configuration file sits on the
file ``/path/to/bob.bio.vein/bob/bio/vein/configurations/verafinger.py``. In
order to modify it, make a local copy. For example:

.. code-block:: sh

   $ cp /path/to/bob.bio.vein/bob/bio/vein/configurations/verafinger.py verafinger_full.py
   $ # edit verafinger_full.py, change the value of "protocol" to "full"


Also, don't forget to change all relative module imports (such as ``from
..database.verafinger import Database``) to absolute imports (e.g. ``from
bob.bio.vein.database.verafinger import Database``). This will make the
configuration file work irrespectively of its location w.r.t. ``bob.bio.vein``.
The final version of the modified file could look like this:

.. code-block:: python

   from bob.bio.vein.database.verafinger import Database

   database = Database(original_directory='/where/you/have/the/raw/files',
     original_extension='.png', #don't change this
     )

   protocol = 'full'


Now, re-run the experiment using your modified database descriptor:

.. code-block:: sh

   $ bob bio pipeline simple ./verafinger_full.py wld -vv -c


Notice we replace the use of the registered configuration file named
``verafinger`` by the local file ``verafinger_full.py``. This makes the program
``verify.py`` take that into consideration instead of the original file.


Other Resources
---------------

This package contains other resources that can be used to evaluate different
bits of the vein processing toolchain.


Region of Interest Goodness of Fit
==================================

Automatic region of interest (RoI) finding and cropping can be evaluated using
a couple of scripts available in this package. The program
``bob_bio_vein_compare_rois.py`` compares two sets of ``preprocessed`` images
and masks, generated by *different* preprocessors (see
:py:class:`bob.bio.base.preprocessor.Preprocessor`) and calculates a few
metrics to help you determine how both techniques compare.  Normally, the
program is used to compare the result of automatic RoI to manually annoted
regions on the same images. To use it, just point it to the outputs of two
experiments representing the manually annotated regions and automatically
extracted ones. E.g.:

.. code-block:: sh

   $ bob_bio_vein_compare_rois.py ~/verafinger/mc_annot/preprocessed ~/verafinger/mc/preprocessed
   Jaccard index: 9.60e-01 +- 5.98e-02
   Intersection ratio (m1): 9.79e-01 +- 5.81e-02
   Intersection ratio of complement (m2): 1.96e-02 +- 1.53e-02


Values printed by the script correspond to the `Jaccard index`_
(:py:func:`bob.bio.vein.preprocessor.utils.jaccard_index`), as well as the
intersection ratio between the manual and automatically generated masks
(:py:func:`bob.bio.vein.preprocessor.utils.intersect_ratio`) and the ratio to
the complement of the intersection with respect to the automatically generated
mask
(:py:func:`bob.bio.vein.preprocessor.utils.intersect_ratio_of_complement`). You
can use the option ``-n 5`` to print the 5 worst cases according to each of the
metrics.


Pipeline Display
================

You can use the program ``bob_bio_vein_view_sample.py`` to display the images
after full processing using:

.. code-block:: sh

   $ bob_bio_vein_view_sample.py --save=output-dir verafinger /path/to/processed/directory 030-M/030_L_1
   $ # open output-dir

And you should be able to view images like these (example taken from the Vera
fingervein database, using the automatic annotator and Maximum Curvature
feature extractor):

.. figure:: img/preprocessed.*
   :scale: 50%

   Example RoI overlayed on finger vein image of the Vera fingervein database,
   as produced by the script ``bob_bio_vein_view_sample.py``.


.. figure:: img/binarized.*
   :scale: 50%

   Example of fingervein image from the Vera fingervein database, binarized by
   using Maximum Curvature, after pre-processing.


.. include:: links.rst
