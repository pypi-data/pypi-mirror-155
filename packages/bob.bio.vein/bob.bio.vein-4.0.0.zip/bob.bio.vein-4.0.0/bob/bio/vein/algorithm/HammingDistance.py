#!/usr/bin/env python
# vim: set fileencoding=utf-8 :


from bob.bio.base.algorithm import Distance


class HammingDistance(Distance):
    """This class calculates the Hamming distance between two binary images.

    The enrollement and scoring functions of this class are implemented by its
    base :py:class:`bob.bio.base.algorithm.Distance`.

    The input to this function should be of binary nature (boolean arrays). Each
    binary input is first flattened to form a one-dimensional vector. The
    `Hamming distance <https://en.wikipedia.org/wiki/Hamming_distance>`_ is then
    calculated between these two binary vectors.

    The current implementation uses :py:func:`scipy.spatial.distance.hamming`,
    which returns a scalar 64-bit ``float`` to represent the proportion of
    mismatching corresponding bits between the two binary vectors.

    The base class constructor parameter ``factor`` is set to ``1`` on purpose
    to ensure that calculated distances are returned as positive values rather
    than negative.
    """

    def __init__(self, **kwargs):
        super(HammingDistance, self).__init__(
            distance_function="hamming",
            factor=1,
            **kwargs,
        )
