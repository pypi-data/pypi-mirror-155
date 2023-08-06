#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

import numpy
import scipy

from PIL import Image

from bob.bio.base.extractor import Extractor


class WideLineDetector(Extractor):
    """Wide Line Detector feature extractor

    Based on B. Huang, Y. Dai, R. Li, D. Tang and W. Li. [HDLTL10]_
    """

    def __init__(
        self,
        radius=5,  # Radius of the circular neighbourhood region
        threshold=1,  # Neigborhood threshold
        g=41,  # Sum of neigbourhood threshold
        rescale=True,
    ):

        # call base class constructor
        Extractor.__init__(
            self,
            radius=radius,
            threshold=threshold,
            g=g,
            rescale=rescale,
        )

        # block parameters
        self.radius = radius
        self.threshold = threshold
        self.g = g
        self.rescale = rescale

    def wide_line_detector(self, finger_image, mask):
        """Computes and returns the Wide Line Detector features for the given input
        fingervein image"""

        finger_image = finger_image.astype(numpy.float64)

        finger_mask = numpy.zeros(mask.shape)
        finger_mask[mask == True] = 1  # noqa: E712

        # Rescale image if required
        if self.rescale:
            scaling_factor = 0.24

            new_size = tuple(
                (numpy.array(finger_image.shape) * scaling_factor).astype(
                    numpy.int
                )
            )
            finger_image = numpy.array(
                Image.fromarray(finger_image).resize(size=new_size)
            ).T

            new_size = tuple(
                (numpy.array(finger_mask.shape) * scaling_factor).astype(
                    numpy.int
                )
            )
            finger_mask = numpy.array(
                Image.fromarray(finger_mask).resize(size=new_size)
            ).T

            # To eliminate residuals from the scalation of the binary mask
            finger_mask = scipy.ndimage.binary_dilation(
                finger_mask, structure=numpy.ones((1, 1))
            ).astype(int)

        x = numpy.arange((-1) * self.radius, self.radius + 1)
        y = numpy.arange((-1) * self.radius, self.radius + 1)
        X, Y = numpy.meshgrid(x, y)

        N = X**2 + Y**2 <= self.radius**2  # Neighbourhood mask

        img_h, img_w = finger_image.shape  # Image height and width

        veins = numpy.zeros(finger_image.shape)

        for y in range(self.radius, img_h - self.radius):
            for x in range(self.radius, img_w - self.radius):
                s = (
                    finger_image[
                        y - self.radius : y + self.radius + 1,
                        x - self.radius : x + self.radius + 1,
                    ]
                    - finger_image[y, x]
                ) <= self.threshold
                m = (s * N).sum()
                veins[y, x] = float(m <= self.g)

        # Mask the vein image with the finger region
        img_veins_bin = veins * finger_mask

        return img_veins_bin

    def __call__(self, image):
        """Reads the input image, extract the features based on Wide Line Detector
        of the fingervein image, and writes the resulting template"""
        # For debugging

        finger_image = image[0]  # Normalized image with histogram equalization
        finger_mask = image[1]

        return self.wide_line_detector(finger_image, finger_mask)
