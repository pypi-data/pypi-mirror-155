#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

import numpy

from bob.bio.base.extractor import Extractor


class NormalisedCrossCorrelation(Extractor):
    """Normalised Cross-Correlation feature extractor

    Based on [KUU02]_
    """

    def __init__(self):
        Extractor.__init__(self)

    def __call__(self, image, mask):
        """Reads the input image, extract the features based on Normalised
        Cross-Correlation of the fingervein image, and writes the resulting
        template"""

        finger_image = image  # Normalized image with histogram equalization
        finger_mask = mask

        image_vein = finger_image * finger_mask

        # TODO

        return image_vein.astype(numpy.float64)
