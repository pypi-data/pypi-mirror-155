"""Helper functions to compute hierarchical evaluation metrics."""
import numpy as np
from sklearn.utils import check_array


def precision(y_true: np.ndarray, y_pred: np.ndarray):
    r"""
    Compute precision score for hierarchical classification.

    :math:`hP = \displaystyle{\frac{\sum_{i}| \alpha_i \cap \beta_i |}{\sum_{i}| \alpha_i |}}`,
    where :math:`\alpha_i` is the set consisting of the most specific classes predicted
    for test example :math:`i` and all their ancestor classes, while :math:`\beta_i` is the
    set containing the true most specific classes of test example :math:`i` and all
    their ancestors, with summations computed over all test examples.

    Parameters
    ----------
    y_true : np.array of shape (n_samples, n_levels)
        Ground truth (correct) labels.
    y_pred : np.array of shape (n_samples, n_levels)
        Predicted labels, as returned by a classifier.
    Returns
    -------
    precision : float
        What proportion of positive identifications was actually correct?
    """
    assert len(y_true) == len(y_pred)
    y_true = check_array(y_true, dtype=None)
    y_pred = check_array(y_pred, dtype=None)
    sum_intersection = 0
    sum_prediction_and_ancestors = 0
    for ground_truth, prediction in zip(y_true, y_pred):
        sum_intersection = sum_intersection + len(
            set(ground_truth).intersection(set(prediction))
        )
        sum_prediction_and_ancestors = sum_prediction_and_ancestors + len(
            set(prediction)
        )
    precision = sum_intersection / sum_prediction_and_ancestors
    return precision


def recall(y_true: np.ndarray, y_pred: np.ndarray):
    r"""
    Compute recall score for hierarchical classification.

    :math:`\displaystyle{hR = \frac{\sum_i|\alpha_i \cap \beta_i|}{\sum_i|\beta_i|}}`,
    where :math:`\alpha_i` is the set consisting of the most specific classes predicted
    for test example :math:`i` and all their ancestor classes, while :math:`\beta_i` is the
    set containing the true most specific classes of test example :math:`i` and all
    their ancestors, with summations computed over all test examples.

    Parameters
    ----------
    y_true : np.array of shape (n_samples, n_levels)
        Ground truth (correct) labels.
    y_pred : np.array of shape (n_samples, n_levels)
        Predicted labels, as returned by a classifier.
    Returns
    -------
    recall : float
        What proportion of actual positives was identified correctly?
    """
    assert len(y_true) == len(y_pred)
    y_true = check_array(y_true, dtype=None)
    y_pred = check_array(y_pred, dtype=None)
    sum_intersection = 0
    sum_prediction_and_ancestors = 0
    for ground_truth, prediction in zip(y_true, y_pred):
        sum_intersection = sum_intersection + len(
            set(ground_truth).intersection(set(prediction))
        )
        sum_prediction_and_ancestors = sum_prediction_and_ancestors + len(
            set(ground_truth)
        )
    recall = sum_intersection / sum_prediction_and_ancestors
    return recall


def f1(y_true: np.ndarray, y_pred: np.ndarray):
    r"""
    Compute f1 score for hierarchical classification.

    :math:`\displaystyle{hF = \frac{2 \times hP \times hR}{hP + hR}}`,
    where :math:`hP` is the hierarchical precision and :math:`hR` is the hierarchical recall.

    Parameters
    ----------
    y_true : np.array of shape (n_samples, n_levels)
        Ground truth (correct) labels.
    y_pred : np.array of shape (n_samples, n_levels)
        Predicted labels, as returned by a classifier.
    Returns
    -------
    f1 : float
        Weighted average of the precision and recall
    """
    assert len(y_true) == len(y_pred)
    y_true = check_array(y_true, dtype=None)
    y_pred = check_array(y_pred, dtype=None)
    prec = precision(y_true, y_pred)
    rec = recall(y_true, y_pred)
    f1 = 2 * prec * rec / (prec + rec)
    return f1
