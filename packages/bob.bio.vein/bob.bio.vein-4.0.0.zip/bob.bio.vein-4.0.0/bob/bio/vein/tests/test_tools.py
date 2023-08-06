#!/usr/bin/env python
# vim: set fileencoding=utf-8 :


"""Unit tests against references extracted from

Matlab code from Bram Ton available on the matlab central website:

https://www.mathworks.com/matlabcentral/fileexchange/35754-wide-line-detector

This code implements the detector described in [HDLTL10] (see the references in
the generated sphinx documentation)
"""

import os

import h5py
import numpy
import pkg_resources

import bob.io.base

from ..preprocessor import utils as preprocessor_utils


def F(parts):
    """Returns the test file path"""

    return pkg_resources.resource_filename(__name__, os.path.join(*parts))


def test_cropping():

    # tests if the cropping stage at preprocessors works as planned

    from ..preprocessor.crop import FixedCrop, NoCrop

    shape = (20, 17)
    test_image = numpy.random.randint(0, 1000, size=shape, dtype=int)

    dont_crop = NoCrop()
    cropped = dont_crop(test_image)
    assert test_image.shape == cropped.shape
    (test_image - cropped).sum() == 0

    top = 5
    bottom = 2
    left = 3
    right = 7
    fixed_crop = FixedCrop(top, bottom, left, right)
    cropped = fixed_crop(test_image)
    assert cropped.shape == (
        shape[0] - (top + bottom),
        shape[1] - (left + right),
    )
    assert (test_image[top:-bottom, left:-right] - cropped).sum() == 0

    # tests metadata survives after cropping (and it is corrected)
    from ..database import AnnotatedArray

    annotations = [
        (top - 2, left + 2),  # slightly above and to the right
        (top + 3, shape[1] - (right + 1) + 3),  # slightly down and to the right
        (shape[0] - (bottom + 1) + 4, shape[1] - (right + 1) - 2),
        (shape[0] - (bottom + 1) + 1, left),
    ]
    annotated_image = AnnotatedArray(test_image, metadata=dict(roi=annotations))
    assert hasattr(annotated_image, "metadata")
    cropped = fixed_crop(annotated_image)
    assert hasattr(cropped, "metadata")
    assert numpy.allclose(
        cropped.metadata["roi"],
        [
            (0, 2),
            (3, cropped.shape[1] - 1),
            (cropped.shape[0] - 1, 4),
            (cropped.shape[0] - 1, 0),
        ],
    )


def test_masking():

    # tests if the masking stage at preprocessors work as planned

    from ..database import AnnotatedArray
    from ..preprocessor.mask import AnnotatedRoIMask, FixedMask, NoMask

    shape = (17, 20)
    test_image = numpy.random.randint(0, 1000, size=shape, dtype=int)

    masker = NoMask()
    mask = masker(test_image)
    assert mask.dtype == numpy.dtype("bool")
    assert mask.shape == test_image.shape
    assert mask.sum() == numpy.prod(shape)

    top = 4
    bottom = 2
    left = 3
    right = 1
    masker = FixedMask(top, bottom, left, right)
    mask = masker(test_image)
    assert mask.dtype == numpy.dtype("bool")
    assert mask.sum() == (shape[0] - (top + bottom)) * (
        shape[1] - (left + right)
    )
    assert mask[top:-bottom, left:-right].sum() == mask.sum()

    # this matches the previous "fixed" mask - notice we consider the pixels
    # under the polygon line to be **part** of the RoI (mask position == True)
    shape = (10, 10)
    test_image = numpy.random.randint(0, 1000, size=shape, dtype=int)
    annotations = [
        (top, left),
        (top, shape[1] - (right + 1)),
        (shape[0] - (bottom + 1), shape[1] - (right + 1)),
        (shape[0] - (bottom + 1), left),
    ]
    image = AnnotatedArray(test_image, metadata=dict(roi=annotations))
    masker = AnnotatedRoIMask()
    mask = masker(image)
    assert mask.dtype == numpy.dtype("bool")
    assert mask.sum() == (shape[0] - (top + bottom)) * (
        shape[1] - (left + right)
    )
    assert mask[top:-bottom, left:-right].sum() == mask.sum()


def test_preprocessor():

    # tests the whole preprocessing mechanism, compares to matlab source

    input_filename = F(("preprocessors", "0019_3_1_120509-160517.png"))
    output_img_filename = F(
        ("preprocessors", "0019_3_1_120509-160517_img_lee_huang.mat.hdf5")
    )
    output_fvr_filename = F(
        ("preprocessors", "0019_3_1_120509-160517_fvr_lee_huang.mat.hdf5")
    )

    img = bob.io.base.load(input_filename)

    from ..preprocessor import (
        HuangNormalization,
        LeeMask,
        NoCrop,
        NoFilter,
        Preprocessor,
    )

    processor = Preprocessor(
        NoCrop(),
        LeeMask(filter_height=40, filter_width=4),
        HuangNormalization(padding_width=0, padding_constant=0),
        NoFilter(),
    )
    preproc, mask = processor(img)
    # preprocessor_utils.show_mask_over_image(preproc, mask)

    mask_ref = bob.io.base.load(output_fvr_filename).astype("bool")
    preproc_ref = bob.io.base.load(output_img_filename)
    # convert range 0,255 and dtype to uint8
    preproc_ref = numpy.round(preproc_ref * 255).astype("uint8")

    assert numpy.mean(numpy.abs(mask ^ mask_ref)) < 1e-2

    # Very loose comparison!
    # preprocessor_utils.show_image(numpy.abs(preproc.astype('int16') - preproc_ref.astype('int16')).astype('uint8'))
    assert numpy.mean(numpy.abs(preproc - preproc_ref)) < 1.3e2


def test_max_curvature():

    # Maximum Curvature method against Matlab reference

    image = bob.io.base.load(F(("extractors", "image.hdf5")))
    image = image.T
    image = image.astype("float64") / 255.0
    mask = bob.io.base.load(F(("extractors", "mask.hdf5")))
    mask = mask.T
    mask = mask.astype("bool")

    vt_ref = numpy.array(
        h5py.File(F(("extractors", "mc_vt_matlab.hdf5")))["Vt"]
    )
    vt_ref = vt_ref.T
    g_ref = numpy.array(h5py.File(F(("extractors", "mc_g_matlab.hdf5")))["G"])
    g_ref = g_ref.T

    bin_ref = numpy.array(
        h5py.File(F(("extractors", "mc_bin_matlab.hdf5")))["binarised"]
    )
    bin_ref = bin_ref.T

    # Apply Python implementation
    from ..extractor.MaximumCurvature import MaximumCurvature

    MC = MaximumCurvature(3)  # value used to create references

    kappa = MC.detect_valleys(image, mask)
    Vt = MC.eval_vein_probabilities(kappa)
    Cd = MC.connect_centres(Vt)
    G = numpy.amax(Cd, axis=2)
    bina = MC.binarise(G)

    assert numpy.allclose(Vt, vt_ref, 1e-3, 1e-4), (
        "Vt differs from reference by %s" % numpy.abs(Vt - vt_ref).sum()
    )
    # Note: due to Matlab implementation bug, can only compare in a limited
    # range with a 3-pixel around frame
    assert numpy.allclose(G[2:-3, 2:-3], g_ref[2:-3, 2:-3]), (
        "G differs from reference by %s" % numpy.abs(G - g_ref).sum()
    )
    # We require no more than 30 pixels (from a total of 63'840) are different
    # between ours and the matlab implementation
    assert numpy.abs(bin_ref - bina).sum() < 30, (
        "Binarized image differs from reference by %s"
        % numpy.abs(bin_ref - bina).sum()
    )


def test_max_curvature_HE():
    # Maximum Curvature method when Histogram Equalization post-processing is applied to the preprocessed vein image

    # Read in input image
    input_img_filename = F(("preprocessors", "0019_3_1_120509-160517.png"))
    input_img = bob.io.base.load(input_img_filename)

    # Preprocess the data and apply Histogram Equalization postprocessing (same parameters as in maximum_curvature.py configuration file + postprocessing)
    from ..preprocessor import (
        HistogramEqualization,
        HuangNormalization,
        LeeMask,
        NoCrop,
        Preprocessor,
    )

    processor = Preprocessor(
        NoCrop(),
        LeeMask(filter_height=40, filter_width=4),
        HuangNormalization(padding_width=0, padding_constant=0),
        HistogramEqualization(),
    )
    preproc_data = processor(input_img)

    # Extract features from preprocessed and histogram equalized data using MC extractor (same parameters as in maximum_curvature.py configuration file)
    from ..extractor.MaximumCurvature import MaximumCurvature

    MC = MaximumCurvature(sigma=5)
    MC(preproc_data)
    # preprocessor_utils.show_image((255.*extr_data).astype('uint8'))


def test_repeated_line_tracking():

    # Repeated Line Tracking method against Matlab reference

    input_img_filename = F(("extractors", "miurarlt_input_img.mat.hdf5"))
    input_fvr_filename = F(("extractors", "miurarlt_input_fvr.mat.hdf5"))
    output_filename = F(("extractors", "miurarlt_output.mat.hdf5"))

    # Load inputs
    input_img = bob.io.base.load(input_img_filename)
    input_fvr = bob.io.base.load(input_fvr_filename)

    # Apply Python implementation
    from ..extractor.RepeatedLineTracking import RepeatedLineTracking

    RLT = RepeatedLineTracking(3000, 1, 21, False)
    output_img = RLT((input_img, input_fvr))

    # Load Matlab reference
    output_img_ref = bob.io.base.load(output_filename)

    # Compare output of python's implementation to matlab reference
    # (loose comparison!)
    assert numpy.mean(numpy.abs(output_img - output_img_ref)) < 0.5


def test_repeated_line_tracking_HE():
    # Repeated Line Tracking method when Histogram Equalization post-processing is applied to the preprocessed vein image

    # Read in input image
    input_img_filename = F(("preprocessors", "0019_3_1_120509-160517.png"))
    input_img = bob.io.base.load(input_img_filename)

    # Preprocess the data and apply Histogram Equalization postprocessing (same parameters as in repeated_line_tracking.py configuration file + postprocessing)
    from ..preprocessor import (
        HistogramEqualization,
        HuangNormalization,
        LeeMask,
        NoCrop,
        Preprocessor,
    )

    processor = Preprocessor(
        NoCrop(),
        LeeMask(filter_height=40, filter_width=4),
        HuangNormalization(padding_width=0, padding_constant=0),
        HistogramEqualization(),
    )
    preproc_data = processor(input_img)

    # Extract features from preprocessed and histogram equalized data using RLT extractor (same parameters as in repeated_line_tracking.py configuration file)
    from ..extractor.RepeatedLineTracking import RepeatedLineTracking

    # Maximum number of iterations
    NUMBER_ITERATIONS = 3000
    # Distance between tracking point and cross section of profile
    DISTANCE_R = 1
    # Width of profile
    PROFILE_WIDTH = 21
    RLT = RepeatedLineTracking(
        iterations=NUMBER_ITERATIONS,
        r=DISTANCE_R,
        profile_w=PROFILE_WIDTH,
        seed=0,
    )
    RLT(preproc_data)


def test_wide_line_detector():

    # Wide Line Detector method against Matlab reference

    input_img_filename = F(("extractors", "huangwl_input_img.mat.hdf5"))
    input_fvr_filename = F(("extractors", "huangwl_input_fvr.mat.hdf5"))
    output_filename = F(("extractors", "huangwl_output.mat.hdf5"))

    # Load inputs
    input_img = bob.io.base.load(input_img_filename)
    input_fvr = bob.io.base.load(input_fvr_filename)

    # Apply Python implementation
    from ..extractor.WideLineDetector import WideLineDetector

    WL = WideLineDetector(5, 1, 41, False)
    output_img = WL((input_img, input_fvr))

    # Load Matlab reference
    output_img_ref = bob.io.base.load(output_filename)

    # Compare output of python's implementation to matlab reference
    assert numpy.allclose(output_img, output_img_ref)


def test_wide_line_detector_HE():
    # Wide Line Detector method when Histogram Equalization post-processing is applied to the preprocessed vein image

    # Read in input image
    input_img_filename = F(("preprocessors", "0019_3_1_120509-160517.png"))
    input_img = bob.io.base.load(input_img_filename)

    # Preprocess the data and apply Histogram Equalization postprocessing (same parameters as in wide_line_detector.py configuration file + postprocessing)
    from ..preprocessor import (
        HistogramEqualization,
        HuangNormalization,
        LeeMask,
        NoCrop,
        Preprocessor,
    )

    processor = Preprocessor(
        NoCrop(),
        LeeMask(filter_height=40, filter_width=4),
        HuangNormalization(padding_width=0, padding_constant=0),
        HistogramEqualization(),
    )
    preproc_data = processor(input_img)

    # Extract features from preprocessed and histogram equalized data using WLD extractor (same parameters as in wide_line_detector.py configuration file)
    from ..extractor.WideLineDetector import WideLineDetector

    # Radius of the circular neighbourhood region
    RADIUS_NEIGHBOURHOOD_REGION = 5
    NEIGHBOURHOOD_THRESHOLD = 1
    # Sum of neigbourhood threshold
    SUM_NEIGHBOURHOOD = 41
    RESCALE = True
    WLD = WideLineDetector(
        radius=RADIUS_NEIGHBOURHOOD_REGION,
        threshold=NEIGHBOURHOOD_THRESHOLD,
        g=SUM_NEIGHBOURHOOD,
        rescale=RESCALE,
    )
    WLD(preproc_data)


def test_miura_match():

    # Match Ratio method against Matlab reference

    template_filename = F(("algorithms", "0001_2_1_120509-135338.mat.hdf5"))
    probe_gen_filename = F(("algorithms", "0001_2_2_120509-135558.mat.hdf5"))
    probe_imp_filename = F(("algorithms", "0003_2_1_120509-141255.mat.hdf5"))

    template_vein = bob.io.base.load(template_filename)
    probe_gen_vein = bob.io.base.load(probe_gen_filename)
    probe_imp_vein = bob.io.base.load(probe_imp_filename)

    from ..algorithm.MiuraMatch import MiuraMatch

    MM = MiuraMatch(ch=18, cw=28)
    score_gen = MM.score(template_vein, probe_gen_vein)

    assert numpy.isclose(score_gen, 0.382689335394127)

    score_imp = MM.score(template_vein, probe_imp_vein)
    assert numpy.isclose(score_imp, 0.172906739278421)


def test_correlate():

    # Match Ratio method against Matlab reference

    template_filename = F(("algorithms", "0001_2_1_120509-135338.mat.hdf5"))
    probe_gen_filename = F(("algorithms", "0001_2_2_120509-135558.mat.hdf5"))
    # probe_imp_filename = F(("algorithms", "0003_2_1_120509-141255.mat.hdf5"))

    template_vein = bob.io.base.load(template_filename)
    probe_gen_vein = bob.io.base.load(probe_gen_filename)
    # probe_imp_vein = bob.io.base.load(probe_imp_filename)

    from ..algorithm.Correlate import Correlate

    C = Correlate()
    C.score(template_vein, probe_gen_vein)

    # we don't check here - no templates


def test_assert_points():

    # Tests that point assertion works as expected
    area = (10, 5)
    inside = [(0, 0), (3, 2), (9, 4)]
    preprocessor_utils.assert_points(area, inside)  # should not raise

    def _check_outside(point):
        # should raise, otherwise it is an error
        try:
            preprocessor_utils.assert_points(area, [point])
        except AssertionError as e:
            assert str(point) in str(e)
        else:
            raise AssertionError(
                "Did not assert %s is outside of %s" % (point, area)
            )

    outside = [(-1, 0), (10, 0), (0, 5), (10, 5), (15, 12)]
    for k in outside:
        _check_outside(k)


def test_fix_points():

    # Tests that point clipping works as expected
    area = (10, 5)
    inside = [(0, 0), (3, 2), (9, 4)]
    fixed = preprocessor_utils.fix_points(area, inside)
    assert numpy.array_equal(inside, fixed), "%r != %r" % (inside, fixed)

    fixed = preprocessor_utils.fix_points(area, [(-1, 0)])
    assert numpy.array_equal(fixed, [(0, 0)])

    fixed = preprocessor_utils.fix_points(area, [(10, 0)])
    assert numpy.array_equal(fixed, [(9, 0)])

    fixed = preprocessor_utils.fix_points(area, [(0, 5)])
    assert numpy.array_equal(fixed, [(0, 4)])

    fixed = preprocessor_utils.fix_points(area, [(10, 5)])
    assert numpy.array_equal(fixed, [(9, 4)])

    fixed = preprocessor_utils.fix_points(area, [(15, 12)])
    assert numpy.array_equal(fixed, [(9, 4)])


def test_poly_to_mask():

    # Tests we can generate a mask out of a polygon correctly
    area = (10, 9)  # 10 rows, 9 columns
    polygon = [(2, 2), (2, 7), (7, 7), (7, 2)]  # square shape, (y, x) format
    mask = preprocessor_utils.poly_to_mask(area, polygon)
    assert mask.dtype == bool

    # This should be the output:
    expected = numpy.array(
        [
            [False, False, False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False, False, False],
            [False, False, True, True, True, True, True, True, False],
            [False, False, True, True, True, True, True, True, False],
            [False, False, True, True, True, True, True, True, False],
            [False, False, True, True, True, True, True, True, False],
            [False, False, True, True, True, True, True, True, False],
            [False, False, True, True, True, True, True, True, False],
            [False, False, False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False, False, False],
        ]
    )
    assert numpy.array_equal(mask, expected)

    polygon = [(3, 2), (5, 7), (8, 7), (7, 3)]  # trapezoid, (y, x) format
    mask = preprocessor_utils.poly_to_mask(area, polygon)
    assert mask.dtype == bool

    # This should be the output:
    expected = numpy.array(
        [
            [False, False, False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False, False, False],
            [False, False, True, False, False, False, False, False, False],
            [False, False, True, True, True, False, False, False, False],
            [False, False, False, True, True, True, True, True, False],
            [False, False, False, True, True, True, True, True, False],
            [False, False, False, True, True, True, True, True, False],
            [False, False, False, False, False, False, False, True, False],
            [False, False, False, False, False, False, False, False, False],
        ]
    )
    assert numpy.array_equal(mask, expected)


def test_mask_to_image():

    # Tests we can correctly convert a boolean array into an image
    # that makes sense according to the data types
    sample = numpy.array([False, True])
    assert sample.dtype == bool

    def _check_uint(n):
        conv = preprocessor_utils.mask_to_image(sample, "uint%d" % n)
        assert conv.dtype == getattr(numpy, "uint%d" % n)
        target = [0, (2**n) - 1]
        assert numpy.array_equal(conv, target), "%r != %r" % (conv, target)

    _check_uint(8)
    _check_uint(16)
    _check_uint(32)
    _check_uint(64)

    def _check_float(n):
        conv = preprocessor_utils.mask_to_image(sample, "float%d" % n)
        assert conv.dtype == getattr(numpy, "float%d" % n)
        assert numpy.array_equal(conv, [0, 1.0]), "%r != %r" % (conv, [0, 1.0])

    _check_float(32)
    _check_float(64)

    # This should be unsupported
    try:
        preprocessor_utils.mask_to_image(sample, "int16")
    except TypeError as e:
        assert "int16" in str(e)
    else:
        raise AssertionError("Conversion to int16 did not trigger a TypeError")


def test_jaccard_index():

    # Tests to verify the Jaccard index calculation is accurate
    a = numpy.array(
        [
            [False, False],
            [True, True],
        ]
    )

    b = numpy.array(
        [
            [True, True],
            [True, False],
        ]
    )

    assert preprocessor_utils.jaccard_index(a, b) == 1.0 / 4.0
    assert preprocessor_utils.jaccard_index(a, a) == 1.0
    assert preprocessor_utils.jaccard_index(b, b) == 1.0
    assert (
        preprocessor_utils.jaccard_index(a, numpy.ones(a.shape, dtype=bool))
        == 2.0 / 4.0
    )
    assert (
        preprocessor_utils.jaccard_index(a, numpy.zeros(a.shape, dtype=bool))
        == 0.0
    )
    assert (
        preprocessor_utils.jaccard_index(b, numpy.ones(b.shape, dtype=bool))
        == 3.0 / 4.0
    )
    assert (
        preprocessor_utils.jaccard_index(b, numpy.zeros(b.shape, dtype=bool))
        == 0.0
    )


def test_intersection_ratio():

    # Tests to verify the intersection ratio calculation is accurate
    a = numpy.array(
        [
            [False, False],
            [True, True],
        ]
    )

    b = numpy.array(
        [
            [True, False],
            [True, False],
        ]
    )

    assert preprocessor_utils.intersect_ratio(a, b) == 1.0 / 2.0
    assert preprocessor_utils.intersect_ratio(a, a) == 1.0
    assert preprocessor_utils.intersect_ratio(b, b) == 1.0
    assert (
        preprocessor_utils.intersect_ratio(a, numpy.ones(a.shape, dtype=bool))
        == 1.0
    )
    assert (
        preprocessor_utils.intersect_ratio(a, numpy.zeros(a.shape, dtype=bool))
        == 0
    )
    assert (
        preprocessor_utils.intersect_ratio(b, numpy.ones(b.shape, dtype=bool))
        == 1.0
    )
    assert (
        preprocessor_utils.intersect_ratio(b, numpy.zeros(b.shape, dtype=bool))
        == 0
    )

    assert preprocessor_utils.intersect_ratio_of_complement(a, b) == 1.0 / 2.0
    assert preprocessor_utils.intersect_ratio_of_complement(a, a) == 0.0
    assert preprocessor_utils.intersect_ratio_of_complement(b, b) == 0.0
    assert (
        preprocessor_utils.intersect_ratio_of_complement(
            a, numpy.ones(a.shape, dtype=bool)
        )
        == 1.0
    )
    assert (
        preprocessor_utils.intersect_ratio_of_complement(
            a, numpy.zeros(a.shape, dtype=bool)
        )
        == 0
    )
    assert (
        preprocessor_utils.intersect_ratio_of_complement(
            b, numpy.ones(b.shape, dtype=bool)
        )
        == 1.0
    )
    assert (
        preprocessor_utils.intersect_ratio_of_complement(
            b, numpy.zeros(b.shape, dtype=bool)
        )
        == 0
    )


def test_hamming_distance():

    from ..algorithm.HammingDistance import HammingDistance

    HD = HammingDistance()

    # Tests on simple binary arrays:
    # 1.) Maximum HD (1.0):
    model_1 = numpy.array([0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0])
    probe_1 = numpy.array([[1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1]])
    score_max = HD.compare([model_1], [probe_1])[0, 0]
    assert score_max == 1.0
    # 2.) Minimum HD (0.0):
    model_2 = numpy.array([0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1])
    probe_2 = numpy.array([[0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1]])
    score_min = HD.compare([model_2], [probe_2])[0, 0]
    assert score_min == 0.0
    # 3.) HD of exactly half (0.5)
    model_3 = numpy.array([0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0])
    probe_3 = numpy.array([[0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1]])
    score_half = HD.compare([model_3], [probe_3])[0, 0]
    assert score_half == 0.5
