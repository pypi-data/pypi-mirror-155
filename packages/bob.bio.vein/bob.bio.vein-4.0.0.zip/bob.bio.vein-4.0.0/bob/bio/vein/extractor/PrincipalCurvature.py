#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

import numpy

from scipy.ndimage import gaussian_filter

from bob.bio.base.extractor import Extractor


class PrincipalCurvature(Extractor):
    """MiuraMax feature extractor

    Based on [CW09]_.
    """

    def __init__(
        self,
        sigma=3,  # Gaussian standard deviation applied
        threshold=4,  # Percentage of maximum used for hard thresholding
    ):
        """NOTE: In the reference paper where the size of the finger image is 320 by 128,
        the proposed values for sigma and threshold are 3 and 4, respectively.
        However, for other resolutions it is better to change the values for sigma and
        threshold. e.g., in UTFVP dataset where the size of the finger image is 672 by 380,
        sigma=6 and threshold=4 workes better results better features.
        """
        # call base class constructor
        Extractor.__init__(
            self,
            sigma=sigma,
            threshold=threshold,
        )

        # block parameters
        self.sigma = sigma
        self.threshold = threshold

    def ut_gauss(self, img, sigma, dx, dy):
        return gaussian_filter(numpy.float64(img), sigma, order=[dx, dy])

    def principal_curvature(self, image, mask):
        """Computes and returns the Maximum Curvature features for the given input
        fingervein image"""

        finger_mask = numpy.zeros(mask.shape)
        finger_mask[mask == True] = 1  # noqa: E712

        sigma = numpy.sqrt(self.sigma**2 / 2)

        gx = self.ut_gauss(image, self.sigma, 1, 0)
        gy = self.ut_gauss(image, self.sigma, 0, 1)

        Gmag = numpy.sqrt(gx**2 + gy**2)  # Gradient magnitude

        # Apply threshold
        gamma = (self.threshold / 100) * numpy.max(Gmag)

        indices = numpy.where(Gmag < gamma)

        gx[indices] = 0
        gy[indices] = 0

        # Normalize
        Gmag[numpy.where(Gmag == 0)] = 1  # Avoid dividing by zero
        gx = gx / Gmag
        gy = gy / Gmag

        hxx = self.ut_gauss(gx, sigma, 1, 0)
        hxy = self.ut_gauss(gx, sigma, 0, 1)
        hyy = self.ut_gauss(gy, sigma, 0, 1)

        lambda1 = 0.5 * (
            hxx
            + hyy
            + numpy.sqrt(hxx**2 + hyy**2 - 2 * hxx * hyy + 4 * hxy**2)
        )
        veins = lambda1 * finger_mask

        # Normalise
        veins = veins - numpy.min(veins[:])
        veins = veins / numpy.max(veins[:])

        veins = veins * finger_mask

        # Binarise the vein image by otsu
        md = numpy.median(veins[veins > 0])
        img_veins_bin = veins > md

        return img_veins_bin.astype(numpy.float64)

    def __call__(self, image):
        """Reads the input image, extract the features based on Principal Curvature
        of the fingervein image, and writes the resulting template"""

        finger_image = image[
            0
        ]  # Normalized image with or without histogram equalization
        finger_mask = image[1]

        return self.principal_curvature(finger_image, finger_mask)
