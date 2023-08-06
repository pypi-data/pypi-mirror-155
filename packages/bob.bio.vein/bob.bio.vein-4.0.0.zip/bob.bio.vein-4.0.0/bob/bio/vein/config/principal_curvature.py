#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Tue 27 Sep 2016 16:48:16 CEST

"""Huang's Principal Curvature extractor and Miura Matching baseline

References:

1. [HDLTL10]_
2. [TV13]_
3. [TVM14]_

"""

from bob.bio.vein.preprocessor import (
    HuangNormalization,
    NoCrop,
    NoFilter,
    Preprocessor,
    TomesLeeMask,
)

legacy_preprocessor = Preprocessor(
    crop=NoCrop(),
    mask=TomesLeeMask(),
    normalize=HuangNormalization(),
    filter=NoFilter(),
)
"""Preprocessing using gray-level based finger cropping and no post-processing
"""


from bob.bio.vein.extractor import PrincipalCurvature

legacy_extractor = PrincipalCurvature()


from sklearn.pipeline import make_pipeline

from bob.bio.base.transformers import (
    ExtractorTransformer,
    PreprocessorTransformer,
)
from bob.pipelines import wrap

transformer = make_pipeline(
    wrap(["sample"], PreprocessorTransformer(legacy_preprocessor)),
    wrap(["sample"], ExtractorTransformer(legacy_extractor)),
)


from bob.bio.vein.algorithm import MiuraMatch

"""Miura-matching algorithm with specific settings for search displacement

Defaults taken from [TV13]_.
"""

import os
import tempfile

sub_directory = "pc"

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


from bob.bio.base.pipelines import PipelineSimple

biometric_algorithm = MiuraMatch(ch=18, cw=28)

pipeline = PipelineSimple(transformer, biometric_algorithm)
