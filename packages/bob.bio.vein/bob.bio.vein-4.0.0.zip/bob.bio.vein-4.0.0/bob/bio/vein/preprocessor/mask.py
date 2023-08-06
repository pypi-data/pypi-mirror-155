#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

"""Base utilities for mask processing"""

import math

import numpy
import scipy.ndimage

from .utils import poly_to_mask


class Padder(object):
    """A class that pads the input image returning a new object


    Parameters:

      padding_width (:py:obj:`int`, optional): How much padding (in pixels) to
        add around the borders of the input image. We normally always keep this
        value on its default (5 pixels). This parameter is always used before
        normalizing the finger orientation.

      padding_constant (:py:obj:`int`, optional): What is the value of the pixels
        added to the padding. This number should be a value between 0 and 255.
        (From Pedro Tome: for UTFVP (high-quality samples), use 0. For the VERA
        Fingervein database (low-quality samples), use 51 (that corresponds to
        0.2 in a float image with values between 0 and 1). This parameter is
        always used before normalizing the finger orientation.

    """

    def __init__(self, padding_width=5, padding_constant=51):

        self.padding_width = padding_width
        self.padding_constant = padding_constant

    def __call__(self, image):
        """Inputs an image, returns a padded (larger) image

        Parameters:

          image (numpy.ndarray): A 2D numpy array of type ``uint8`` with the
            input image


        Returns:

          numpy.ndarray: A 2D numpy array of the same type as the input, but with
          the extra padding

        """

        return numpy.pad(
            image,
            self.padding_width,
            "constant",
            constant_values=self.padding_constant,
        )


class Masker(object):
    """This is the base class for all maskers

    It defines the minimum requirements for all derived masker classes.


    """

    def __init__(self):
        pass

    def __call__(self, image):
        """Overwrite this method to implement your masking method


        Parameters:

          image (numpy.ndarray): A 2D numpy array of type ``uint8`` with the
            input image


        Returns:

          numpy.ndarray: A 2D numpy array of type boolean with the caculated
          mask. ``True`` values correspond to regions where the finger is
          situated

        """

        raise NotImplementedError("You must implement the __call__ slot")


class FixedMask(Masker):
    """Implements masking using a fixed suppression of border pixels

    The defaults mask no lines from the image and returns a mask of the same size
    of the original image where all values are ``True``.


    .. note::

       Before choosing values, note you're responsible for knowing what is the
       orientation of images fed into this masker.


    Parameters:

      top (:py:class:`int`, optional): Number of lines to suppress from the top
        of the image. The top of the image corresponds to ``y = 0``.

      bottom (:py:class:`int`, optional): Number of lines to suppress from the
        bottom of the image. The bottom of the image corresponds to ``y =
        height``.

      left (:py:class:`int`, optional): Number of lines to suppress from the left
        of the image. The left of the image corresponds to ``x = 0``.

      right (:py:class:`int`, optional): Number of lines to suppress from the
        right of the image. The right of the image corresponds to ``x = width``.

    """

    def __init__(self, top=0, bottom=0, left=0, right=0):
        self.top = top
        self.bottom = bottom
        self.left = left
        self.right = right

    def __call__(self, image):
        """Returns a big mask


        Parameters:

          image (numpy.ndarray): A 2D numpy array of type ``uint8`` with the
            input image


        Returns:

          numpy.ndarray: A 2D numpy array of type boolean with the caculated
          mask. ``True`` values correspond to regions where the finger is
          situated


        """

        retval = numpy.zeros(image.shape, dtype="bool")
        h, w = image.shape
        retval[self.top : h - self.bottom, self.left : w - self.right] = True
        return retval


class NoMask(FixedMask):
    """Convenience: same as FixedMask()"""

    def __init__(self):
        super(NoMask, self).__init__(0, 0, 0, 0)


class AnnotatedRoIMask(Masker):
    """Devises the mask from the annotated RoI"""

    def __init__(self):
        pass

    def __call__(self, image):
        """Returns a mask extrapolated from RoI annotations


        Parameters:

          image (bob.bio.vein.database.AnnotatedArray): A 2D numpy array of type
            ``uint8`` with the input image containing an attribute called
            ``metadata`` (a python dictionary). The ``metadata`` object just
            contain a key called ``roi`` containing the annotated points


        Returns:

          numpy.ndarray: A 2D numpy array of type boolean with the caculated
          mask. ``True`` values correspond to regions where the finger is
          situated


        """

        return poly_to_mask(image.shape, image.metadata["roi"])


class KonoMask(Masker):
    """Estimates the finger region given an input NIR image using Kono et al.

    This method is based on the work of M. Kono, H. Ueki and S.  Umemura.
    Near-infrared finger vein patterns for personal identification, Applied
    Optics, Vol. 41, Issue 35, pp. 7429-7436 (2002).


    Parameters:

      sigma (:py:obj:`float`, optional): The standard deviation of the gaussian
        blur filter to apply for low-passing the input image (background
        extraction). Defaults to ``5``.

      padder (:py:class:`Padder`, optional): If passed, will pad the image before
        evaluating the mask. The returned value will have the padding removed and
        is, therefore, of the exact size of the input image.

    """

    def __init__(self, sigma=5, padder=Padder()):

        self.sigma = sigma
        self.padder = padder

    def __call__(self, image):
        """Inputs an image, returns a mask (numpy boolean array)

        Parameters:

          image (numpy.ndarray): A 2D numpy array of type ``uint8`` with the
            input image


        Returns:

          numpy.ndarray: A 2D numpy array of type boolean with the caculated
          mask. ``True`` values correspond to regions where the finger is
          situated

        """

        image = image if self.padder is None else self.padder(image)
        if image.dtype == numpy.uint8:
            image = image.astype("float64") / 255.0

        img_h, img_w = image.shape

        # Determine lower half starting point
        if numpy.mod(img_h, 2) == 0:
            half_img_h = img_h / 2 + 1
        else:
            half_img_h = numpy.ceil(img_h / 2)

        # Construct filter kernel
        winsize = numpy.ceil(4 * self.sigma)

        x = numpy.arange(-winsize, winsize + 1)
        y = numpy.arange(-winsize, winsize + 1)
        X, Y = numpy.meshgrid(x, y)

        hy = (-Y / (2 * math.pi * self.sigma**4)) * numpy.exp(
            -(X**2 + Y**2) / (2 * self.sigma**2)
        )

        # Filter the image with the directional kernel
        fy = scipy.ndimage.convolve(image, hy, mode="nearest")

        # Upper part of filtred image
        img_filt_up = fy[0:half_img_h, :]
        y_up = img_filt_up.argmax(axis=0)

        # Lower part of filtred image
        img_filt_lo = fy[half_img_h - 1 :, :]
        y_lo = img_filt_lo.argmin(axis=0)

        # Fill region between upper and lower edges
        finger_mask = numpy.ndarray(image.shape, bool)
        finger_mask[:, :] = False

        for i in range(0, img_w):
            finger_mask[
                y_up[i] : y_lo[i] + image.shape[0] - half_img_h + 2, i
            ] = True

        if not self.padder:
            return finger_mask
        else:
            w = self.padder.padding_width
            return finger_mask[w:-w, w:-w]


class LeeMask(Masker):
    """Estimates the finger region given an input NIR image using Lee et al.

    This method is based on the work of Finger vein recognition using
    minutia-based alignment and local binary pattern-based feature extraction,
    E.C. Lee, H.C. Lee and K.R. Park, International Journal of Imaging Systems
    and Technology, Volume 19, Issue 3, September 2009, Pages 175--178, doi:
    10.1002/ima.20193

    This code is based on the Matlab implementation by Bram Ton, available at:

    https://nl.mathworks.com/matlabcentral/fileexchange/35752-finger-region-localisation/content/lee_region.m

    In this method, we calculate the mask of the finger independently for each
    column of the input image. Firstly, the image is convolved with a [1,-1]
    filter of size ``(self.filter_height, self.filter_width)``. Then, the upper and
    lower parts of the resulting filtered image are separated. The location of
    the maxima in the upper part is located. The same goes for the location of
    the minima in the lower part. The mask is then calculated, per column, by
    considering it starts in the point where the maxima is in the upper part and
    goes up to the point where the minima is detected on the lower part.


    Parameters:

      filter_height (:py:obj:`int`, optional): Height of contour mask in pixels,
        must be an even number

      filter_width (:py:obj:`int`, optional): Width of the contour mask in pixels

    """

    def __init__(self, filter_height=4, filter_width=40, padder=Padder()):
        self.filter_height = filter_height
        self.filter_width = filter_width
        self.padder = padder

    def __call__(self, image):
        """Inputs an image, returns a mask (numpy boolean array)

        Parameters:

          image (numpy.ndarray): A 2D numpy array of type ``uint8`` with the
            input image


        Returns:

          numpy.ndarray: A 2D numpy array of type boolean with the caculated
          mask. ``True`` values correspond to regions where the finger is
          situated

        """

        image = image if self.padder is None else self.padder(image)
        if image.dtype == numpy.uint8:
            image = image.astype("float64") / 255.0

        img_h, img_w = image.shape

        # Determine lower half starting point
        half_img_h = int(img_h / 2)

        # Construct mask for filtering
        mask = numpy.ones(
            (self.filter_height, self.filter_width), dtype="float64"
        )
        mask[int(self.filter_height / 2.0) :, :] = -1.0

        img_filt = scipy.ndimage.convolve(image, mask, mode="nearest")

        # Upper part of filtered image
        img_filt_up = img_filt[:half_img_h, :]
        y_up = img_filt_up.argmax(axis=0)

        # Lower part of filtered image
        img_filt_lo = img_filt[half_img_h:, :]
        y_lo = img_filt_lo.argmin(axis=0)

        # Translation: for all columns of the input image, set to True all pixels
        # of the mask from index where the maxima occurred in the upper part until
        # the index where the minima occurred in the lower part.
        finger_mask = numpy.zeros(image.shape, dtype="bool")
        for i in range(img_filt.shape[1]):
            finger_mask[
                y_up[i] : (y_lo[i] + img_filt_lo.shape[0] + 1), i
            ] = True

        if not self.padder:
            return finger_mask
        else:
            w = self.padder.padding_width
            return finger_mask[w:-w, w:-w]


class TomesLeeMask(Masker):
    """Estimates the finger region given an input NIR image using Lee et al.

    This method is based on the work of Finger vein recognition using
    minutia-based alignment and local binary pattern-based feature extraction,
    E.C. Lee, H.C. Lee and K.R. Park, International Journal of Imaging Systems
    and Technology, Volume 19, Issue 3, September 2009, Pages 175--178, doi:
    10.1002/ima.20193

    This code is a variant of the Matlab implementation by Bram Ton, available
    at:

    https://nl.mathworks.com/matlabcentral/fileexchange/35752-finger-region-localisation/content/lee_region.m

    In this variant from Pedro Tome, the technique of filtering the image with
    a horizontal filter is also applied on the vertical axis. The objective is to
    find better limits on the horizontal axis in case finger images show the
    finger tip. If that is not your case, you may use the original variant
    :py:class:`LeeMask` above.


    Parameters:

      filter_height (:py:obj:`int`, optional): Height of contour mask in pixels,
        must be an even number

      filter_width (:py:obj:`int`, optional): Width of the contour mask in pixels

    """

    def __init__(self, filter_height=4, filter_width=40, padder=Padder()):
        self.filter_height = filter_height
        self.filter_width = filter_width
        self.padder = padder

    def __call__(self, image):
        """Inputs an image, returns a mask (numpy boolean array)

        Parameters:

          image (numpy.ndarray): A 2D numpy array of type ``uint8`` with the
            input image


        Returns:

          numpy.ndarray: A 2D numpy array of type boolean with the caculated
          mask. ``True`` values correspond to regions where the finger is
          situated

        """

        image = image if self.padder is None else self.padder(image)
        if image.dtype == numpy.uint8:
            image = image.astype("float64") / 255.0

        img_h, img_w = image.shape

        # Determine lower half starting point
        half_img_h = img_h / 2
        half_img_w = img_w / 2

        # Construct mask for filtering (up-bottom direction)
        mask = numpy.ones(
            (self.filter_height, self.filter_width), dtype="float64"
        )
        mask[int(self.filter_height / 2.0) :, :] = -1.0

        img_filt = scipy.ndimage.convolve(image, mask, mode="nearest")

        # Upper part of filtred image
        img_filt_up = img_filt[: int(half_img_h), :]
        y_up = img_filt_up.argmax(axis=0)

        # Lower part of filtred image
        img_filt_lo = img_filt[int(half_img_h) :, :]
        y_lo = img_filt_lo.argmin(axis=0)

        img_filt = scipy.ndimage.convolve(image, mask.T, mode="nearest")

        # Left part of filtered image
        img_filt_lf = img_filt[:, : int(half_img_w)]
        y_lf = img_filt_lf.argmax(axis=1)

        # Right part of filtred image
        img_filt_rg = img_filt[:, int(half_img_w) :]
        y_rg = img_filt_rg.argmin(axis=1)

        finger_mask = numpy.zeros(image.shape, dtype="bool")

        for i in range(0, y_up.size):
            finger_mask[y_up[i] : y_lo[i] + img_filt_lo.shape[0] + 1, i] = True

        # Left region
        for i in range(0, y_lf.size):
            finger_mask[i, 0 : y_lf[i] + 1] = False

        # Right region has always the finger ending, crop the padding with the
        # meadian
        finger_mask[:, int(numpy.median(y_rg) + img_filt_rg.shape[1]) :] = False

        if not self.padder:
            return finger_mask
        else:
            w = self.padder.padding_width
            return finger_mask[w:-w, w:-w]
