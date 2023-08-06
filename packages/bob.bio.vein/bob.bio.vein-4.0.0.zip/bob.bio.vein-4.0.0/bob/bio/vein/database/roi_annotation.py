from pathlib import Path

from numpy import loadtxt
from sklearn.base import BaseEstimator, TransformerMixin

from bob.pipelines import DelayedSample


class ROIAnnotation(TransformerMixin, BaseEstimator):
    """
    Transformer class to read ROI annotation file for grayscale images
    """

    def __init__(self, roi_path):
        super(ROIAnnotation, self).__init__()
        self.roi_path = Path(roi_path) if roi_path else False

    def fit(self, X, y=None):
        return self

    def _more_tags(self):
        return {
            "requires_fit": False,
        }

    def transform(self, X):
        """
        If the annotation file exists, read it and add the ROI points as an attribute to the sample.
        """
        if self.roi_path and self.roi_path.exists():
            annotated_samples = []
            for x in X:
                roi_file = (self.roi_path / x.key).with_suffix(".txt")
                roi = loadtxt(roi_file, dtype="uint16")

                sample = DelayedSample.from_sample(x, roi=roi)
                annotated_samples.append(sample)

            return annotated_samples
        else:
            return X
