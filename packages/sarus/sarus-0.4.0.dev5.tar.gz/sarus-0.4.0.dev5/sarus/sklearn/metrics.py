from typing import Any, cast

import numpy as np
import sarus_data_spec.protobuf as sp
import sarus_data_spec.typing as st
from sarus_data_spec.context import global_context
from sarus_data_spec.scalar import model
from sarus_data_spec.transform import external
from sarus_data_spec.variant_constraint import variant_constraint

from sarus.context.typing import LocalSDKContext
from sarus.dataspec_wrapper import DataSpecWrapper
from sarus.typing import DataSpecVariant

try:
    import sklearn.metrics as sk_metrics
except ModuleNotFoundError:
    pass  # error message in sarus_data_spec.typing


def accuracy_score(y_true: Any, y_pred, *args, **kwargs):
    if isinstance(y_true, DataSpecWrapper) and isinstance(
        y_pred, DataSpecWrapper
    ):
        new_dataspec = external(
            sp.Transform.ExternalOp.SK_ACCURACY_SCORE, *args, **kwargs
        )(y_true._dataspec, y_pred._dataspec)
        context: LocalSDKContext = global_context()
        return context.wrapper_factory().create(new_dataspec)
    else:
        return sk_metrics.accuracy_score(y_true, y_pred, *args, **kwargs)


def average_precision_score(y_true: Any, y_pred, *args, **kwargs):
    if isinstance(y_true, DataSpecWrapper) and isinstance(
        y_pred, DataSpecWrapper
    ):
        new_dataspec = external(
            sp.Transform.ExternalOp.SK_AVERAGE_PRECISION_SCORE, *args, **kwargs
        )(y_true._dataspec, y_pred._dataspec)
        context: LocalSDKContext = global_context()
        return context.wrapper_factory().create(new_dataspec)
    else:
        return sk_metrics.average_precision_score(
            y_true, y_pred, *args, **kwargs
        )


def classification_report(y_true: Any, y_pred, *args, **kwargs):
    if isinstance(y_true, DataSpecWrapper) and isinstance(
        y_pred, DataSpecWrapper
    ):
        new_dataspec = external(
            sp.Transform.ExternalOp.SK_CLASSIFICATION_REPORT, *args, **kwargs
        )(y_true._dataspec, y_pred._dataspec)
        context: LocalSDKContext = global_context()
        return context.wrapper_factory().create(new_dataspec)
    else:
        return sk_metrics.classification_report(
            y_true, y_pred, *args, **kwargs
        )


def confusion_matrix(y_true: Any, y_pred, *args, **kwargs):
    if isinstance(y_true, DataSpecWrapper) and isinstance(
        y_pred, DataSpecWrapper
    ):
        new_dataspec = external(
            sp.Transform.ExternalOp.SK_CONFUSION_MATRIX, *args, **kwargs
        )(y_true._dataspec, y_pred._dataspec)
        context: LocalSDKContext = global_context()
        return context.wrapper_factory().create(new_dataspec)
    else:
        return sk_metrics.confusion_matrix(y_true, y_pred, *args, **kwargs)


def f1_score(y_true: Any, y_pred, *args, **kwargs):
    if isinstance(y_true, DataSpecWrapper) and isinstance(
        y_pred, DataSpecWrapper
    ):
        new_dataspec = external(
            sp.Transform.ExternalOp.SK_F1_SCORE, *args, **kwargs
        )(y_true._dataspec, y_pred._dataspec)
        context: LocalSDKContext = global_context()
        return context.wrapper_factory().create(new_dataspec)
    else:
        return sk_metrics.f1_score(y_true, y_pred, *args, **kwargs)


def plot_confusion_matrix(estimator: Any, X, y_true, *args, **kwargs):
    if isinstance(y_true, DataSpecWrapper):
        new_dataspec = external(
            sp.Transform.ExternalOp.SK_PLOT_CONFUSION_MATRIX, *args, **kwargs
        )(estimator, X._dataspec, y_true._dataspec)
        context: LocalSDKContext = global_context()
        return context.wrapper_factory().create(new_dataspec)
    else:
        return sk_metrics.plot_confusion_matrix(
            estimator, X, y_true, *args, **kwargs
        )


def precision_recall_curve(y_true: Any, probas_pred, *args, **kwargs):
    if isinstance(y_true, DataSpecWrapper) and isinstance(
        probas_pred, DataSpecWrapper
    ):
        new_dataspec = external(
            sp.Transform.ExternalOp.SK_PRECISION_RECALL_CURVE, *args, **kwargs
        )(y_true._dataspec, probas_pred._dataspec)
        context: LocalSDKContext = global_context()
        return context.wrapper_factory().create(new_dataspec)
    else:
        return sk_metrics.precision_recall_curve(
            y_true, probas_pred, *args, **kwargs
        )


def precision_score(y_true: Any, y_pred, *args, **kwargs):
    if isinstance(y_true, DataSpecWrapper) and isinstance(
        y_pred, DataSpecWrapper
    ):
        new_dataspec = external(
            sp.Transform.ExternalOp.SK_PRECISION_SCORE, *args, **kwargs
        )(y_true._dataspec, y_pred._dataspec)
        context: LocalSDKContext = global_context()
        return context.wrapper_factory().create(new_dataspec)
    else:
        return sk_metrics.precision_score(y_true, y_pred, *args, **kwargs)


def recall_score(y_true: Any, y_pred, *args, **kwargs):
    if isinstance(y_true, DataSpecWrapper) and isinstance(
        y_pred, DataSpecWrapper
    ):
        new_dataspec = external(
            sp.Transform.ExternalOp.SK_RECALL_SCORE, *args, **kwargs
        )(y_true._dataspec, y_pred._dataspec)
        context: LocalSDKContext = global_context()
        return context.wrapper_factory().create(new_dataspec)
    else:
        return sk_metrics.recall_score(y_true, y_pred, *args, **kwargs)


def roc_auc_score(y_true: Any, y_pred, *args, **kwargs):
    if isinstance(y_true, DataSpecWrapper) and isinstance(
        y_pred, DataSpecWrapper
    ):
        new_dataspec = external(
            sp.Transform.ExternalOp.SK_ROC_AUC_SCORE, *args, **kwargs
        )(y_true._dataspec, y_pred._dataspec)
        context: LocalSDKContext = global_context()
        return context.wrapper_factory().create(new_dataspec)
    else:
        return sk_metrics.roc_auc_score(y_true, y_pred, *args, **kwargs)


def roc_curve(y_true: Any, y_score, *args, **kwargs):
    if isinstance(y_true, DataSpecWrapper) and isinstance(
        y_score, DataSpecWrapper
    ):
        new_dataspec = external(
            sp.Transform.ExternalOp.SK_ROC_CURVE, *args, **kwargs
        )(y_true._dataspec, y_score._dataspec)
        context: LocalSDKContext = global_context()
        return context.wrapper_factory().create(new_dataspec)
    else:
        return sk_metrics.roc_curve(y_true, y_score, *args, **kwargs)
