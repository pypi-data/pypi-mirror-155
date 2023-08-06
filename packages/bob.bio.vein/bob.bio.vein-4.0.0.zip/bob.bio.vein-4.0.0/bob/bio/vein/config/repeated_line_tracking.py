#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Tue 27 Sep 2016 16:48:08 CEST

"""Repeated-Line Tracking and Miura Matching baseline

References:

1. [MNM04]_
2. [TV13]_
3. [TVM14]_

"""
import os
import tempfile

from sklearn.pipeline import make_pipeline

from bob.bio.base.pipelines import PipelineSimple
from bob.bio.base.transformers import (
    ExtractorTransformer,
    PreprocessorTransformer,
)
from bob.bio.vein.algorithm import MiuraMatch
from bob.bio.vein.extractor import RepeatedLineTracking
from bob.bio.vein.preprocessor import (
    HuangNormalization,
    NoCrop,
    NoFilter,
    Preprocessor,
    TomesLeeMask,
)
from bob.pipelines import wrap

"""Baseline updated with the wrapper for the pipelines package"""

"""Sub-directory where temporary files are saved"""
sub_directory = "rlt"
default_temp = (
    os.path.join("/idiap", "temp", os.environ["USER"])
    if "USER" in os.environ
    else "~/temp"
)

if os.path.exists(default_temp):
    legacy_temp_dir = os.path.join(
        default_temp, "bob_bio_base_tmp", sub_directory
    )
else:
    # if /idiap/temp/<USER> does not exist, use /tmp/tmpxxxxxxxx
    legacy_temp_dir = tempfile.TemporaryDirectory().name

"""Preprocessing using gray-level based finger cropping and no post-processing
"""
preprocessor = PreprocessorTransformer(
    Preprocessor(
        crop=NoCrop(),
        mask=TomesLeeMask(),
        normalize=HuangNormalization(),
        filter=NoFilter(),
    )
)

"""Features are the output of repeated-line tracking, as described on [MNM04]_.

Defaults taken from [TV13]_.
"""
extractor = ExtractorTransformer(RepeatedLineTracking())

"""Miura-matching algorithm with specific settings for search displacement

Defaults taken from [TV13]_.
"""
biometric_algorithm = MiuraMatch(ch=65, cw=55)

transformer = make_pipeline(
    wrap(["sample"], preprocessor), wrap(["sample"], extractor)
)
pipeline = PipelineSimple(transformer, biometric_algorithm)
