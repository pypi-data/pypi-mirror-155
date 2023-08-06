#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Victor <vbros@idiap.ch>

"""
  Utfvp database implementation
"""

from sklearn.pipeline import make_pipeline

import bob.io.base

from bob.bio.base.database import CSVDataset, CSVToSampleLoaderBiometrics
from bob.bio.vein.database.roi_annotation import ROIAnnotation
from bob.extension import rc
from bob.extension.download import get_file


class UtfvpDatabase(CSVDataset):
    """
    The University of Twente Finger Vascular Pattern dataset

    .. warning::

      To use this dataset protocol, you need to have the original files of the UTFVP dataset.
      Once you have it downloaded, please run the following command to set the path for Bob

        .. code-block:: sh

            bob config set bob.bio.vein.utfvp.directory [DATABASE PATH]

    The fingervein image database consists of 1440 images taken in 2 distinct
    session in two days (May 9th, 2012 and May 23rd, 2012) using a custom built
    fingervein sensor. In each session, each of the 60 subjects in the dataset were
    asked to present 6 fingers to the sensor twice, making up separate tries. The
    six fingers are the left and right ring, middle and index fingers. Therefore,
    the database contains 60x6 = 360 unique fingers.

    Files in the database have a strict naming convention and are organized in
    directories following their subject identifier like so:
    ``0003/0003_5_2_120509-141536``. The fields can be interpreted as
    ``<subject-id>/<subject-id>_<finger-name>_<trial>_<date>-<hour>``. The subject
    identifier is written as a 4-digit number with leading zeroes, varying from 1
    to 60. The finger name is one of the following:

      * **1**: Left ring
      * **2**: Left middle
      * **3**: Left index
      * **4**: Right index
      * **5**: Right middle
      * **6**: Right ring

    The trial identifiers can vary between 1 and 4. The first two tries were
    captured during the first session while the last two, on the second session.
    Given the difference in the images between trials on the same day, we assume
    users were asked to remove the finger from the device and re-position it
    afterwards.

    **Annotations**

    We provide region-of-interest (RoI) **hand-made** annotations for all images in
    this dataset. The annotations mark the place where the finger is on the image,
    excluding the background. The annotation file is a text file with one
    annotation per line in the format ``(y, x)``, respecting Bob's image encoding
    convention. The interconnection of these points in a polygon forms the RoI.

    .. warning::

      To use the annotations, you need to provide the roi files.
      Once you have it downloaded, please run the following command to set the path for Bob

        .. code-block:: sh

            bob config set bob.bio.vein.utfvp.roi [ANNOTATION PATH]


    **Protocols**

    There are 15 protocols implemented in this package:

     * 1vsall
     * nom
     * nomLeftRing
     * nomLeftMiddle
     * nomLeftIndex
     * nomRightIndex
     * nomRightMiddle
     * nomRightRing
     * full
     * fullLeftRing
     * fullLeftMiddle
     * fullLeftIndex
     * fullRightIndex
     * fullRightMiddle
     * fullRightRing

    **"nom" Protocols**

    "nom" means "normal operation mode". In this set of protocols, images from
    different clients are separated in different sets that can be used for system
    training, validation and evaluation:

    * Fingers from clients in the range [1, 10] are used on the training set
    * Fingers from clients in the range [11, 28] are used on the development (or validation) set
    * Fingers from clients in the range [29, 60] are used in the evaluation (or test) set

    Data from the first session (both trials) can be used for enrolling the finger
    while data on the last session (both trials) should be used exclusively for
    probing the finger. In the way setup by this database interface, each of the
    samples is returned as a separate enrollment model. If a single score per
    finger is required, the user must manipulate the final score listings and fuse
    results themselves.

    Matching happens exhaustively between all probes and models. The variants named
    "nomLeftRing", for example, contain the data filtered by finger name as per the
    listings above. For example, "Left Ring" means all files named
    ``*/*_1_*_*-*.png``. Therefore, the equivalent protocol contains only 1/6 of
    the files of its complete ``nom`` version.


    **"full" Protocols**


    "full" protocols are meant to match current practices in fingervein reporting
    in which most published material don't use a separate evaluation set. All data
    is placed on the development (or validation) set. In these protocols, all
    images are used both for enrolling and probing for fingers. It is, of course,
    a biased setup. Matching happens exhaustively between all samples in the
    development set.


    The variants named "fullLeftRing", for example, contain the data filtered by
    finger name as per the listings above. For example, "Left Ring" means all files
    named ``*/*_1_*_*-*.png``. Therefore, the equivalent protocol contains only 1/6
    of the files of its complete ``full`` version.


    **"1vsall" Protocol**

    The "1vsall" protocol is meant as a cross-validation protocol. All data from
    the dataset is split into training and development (or validation). No samples
    are allocated for a separate evaluation (or test) set. The training set is
    composed of all samples of fingers ``0001_1`` (left ring finger of subject 1),
    ``0002_2`` (left middle finger of subject 2), ``0003_3`` (left index finger of
    subject 3), ``0004_4`` (right index finger of subject 4), ``0005_5`` (right
    middle finger of subject 5), ``0006_6`` (right ring finger of subject 6),
    ``0007_1`` (left ring finger of subject 7), ``0008_2`` (left middle finger of
    subject 8) and so on, until subject 35 (inclusive). There are 140 images in
    total on this set.

    All other 1300 samples from the dataset are used as a development (or
    validation) set. Each sample generates a single model and is used as a probe
    for all other models. Matching happens exhaustively, but with the same image
    that generated the model being matched. So, there are 1299 probes per model.

    """

    def __init__(self, protocol):
        # Downloading model if not exists
        urls = UtfvpDatabase.urls()
        filename = get_file(
            "utfvp.tar.gz",
            urls,
            file_hash="526045842fcee46eec3415bfc8ac34d3",
        )

        super().__init__(
            name="utfvp",
            dataset_protocol_path=filename,
            protocol=protocol,
            csv_to_sample_loader=make_pipeline(
                CSVToSampleLoaderBiometrics(
                    data_loader=bob.io.base.load,
                    dataset_original_directory=rc.get(
                        "bob.bio.vein.utfvp.directory", ""
                    ),
                    extension="",
                    reference_id_equal_subject_id=False,
                ),
                ROIAnnotation(roi_path=rc.get("bob.bio.vein.utfvp.roi", "")),
            ),
            score_all_vs_all=True,
        )

    @staticmethod
    def protocols():
        # TODO: Until we have (if we have) a function that dumps the protocols, let's use this one.
        return [
            "nom",
            "full",
            "1vsall",
            "nomLeftRing",
            "nomRightRing",
            "nomLeftMiddle",
            "nomRightMiddle",
            "nomLeftIndex",
            "nomRightIndex",
            "fullLeftRing",
            "fullRightRing",
            "fullLeftMiddle",
            "fullRightMiddle",
            "fullLeftIndex",
            "fullRightIndex",
        ]

    @staticmethod
    def urls():
        return [
            "https://www.idiap.ch/software/bob/databases/latest/utfvp-557bfdd2.tar.gz",
            "http://www.idiap.ch/software/bob/databases/latest/utfvp-557bfdd2.tar.gz",
        ]
