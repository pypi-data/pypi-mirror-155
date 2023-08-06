#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

import numpy
import skimage.feature

from bob.bio.base.pipelines import BioAlgorithm


class Correlate(BioAlgorithm):
    """Correlate probe and model without cropping

    The method is based on "cross-correlation" between a model and a probe image.
    The difference between this and :py:class:`MiuraMatch` is that **no**
    cropping takes place on this implementation. We simply fill the excess
    boundary with zeros and extract the valid correlation region between the
    probe and the model using :py:func:`skimage.feature.match_template`.

    """

    def __init__(
        self,
        probes_score_fusion="max",
        enrolls_score_fusion="mean",
        **kwargs,
    ):
        super().__init__(
            probes_score_fusion=probes_score_fusion,
            enrolls_score_fusion=enrolls_score_fusion,
            **kwargs,
        )

    def create_templates(self, feature_sets, enroll):
        return feature_sets

    def compare(self, enroll_templates, probe_templates):
        # returns scores NxM where N is the number of enroll templates and M is the number of probe templates
        # enroll_templates is Nx?1xD
        # probe_templates is Mx?2xD
        scores = []
        for enroll in enroll_templates:
            scores.append([])
            for probe in probe_templates:
                s = [[self.score(e, p) for p in probe] for e in enroll]
                s = self.fuse_probe_scores(s, axis=1)
                s = self.fuse_enroll_scores(s, axis=0)
                scores[-1].append(s)
        return numpy.array(scores)

    def score(self, model, probe):
        """Computes the score between the probe and the model.

        Parameters:

          model (numpy.ndarray): The model of the user to test the probe agains

          probe (numpy.ndarray): The probe to test


        Returns:

          float: Value between 0 and 0.5, larger value means a better match

        """

        image_ = probe.astype(numpy.float64)

        R = model.astype(numpy.float64)
        Nm = skimage.feature.match_template(image_, R)

        # figures out where the maximum is on the resulting matrix
        t0, s0 = numpy.unravel_index(Nm.argmax(), Nm.shape)

        # this is our output
        score = Nm[t0, s0]

        return score
