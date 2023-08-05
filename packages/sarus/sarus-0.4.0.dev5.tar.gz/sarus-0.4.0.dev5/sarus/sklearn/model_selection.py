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
    import sklearn.model_selection as sk_model_selection
except ModuleNotFoundError:
    pass  # error message in sarus_data_spec.typing


def cross_val_score(estimator: Any, X: Any, y: Any, *args, **kwargs):
    if isinstance(X, DataSpecWrapper):
        new_dataspec = external(
            sp.Transform.ExternalOp.SK_CROSS_VAL_SCORE, *args, **kwargs
        )(estimator._dataspec, X._dataspec, y._dataspec)
        context: LocalSDKContext = global_context()
        return context.wrapper_factory().create(new_dataspec)
    else:
        print("`X` is not a Sarus object, fitting on synthetic data.")
        return sk_model_selection.cross_val_score(
            estimator, X, *args, **kwargs
        )


def train_test_split(X: Any, y: Any, *args, **kwargs):
    """TODO: Should we return a list of Sarus object or a Sarus List ?"""
    if isinstance(X, DataSpecWrapper):
        result = external(
            sp.Transform.ExternalOp.SK_TRAIN_TEST_SPLIT, *args, **kwargs
        )(X._dataspec, y._dataspec)
        context: LocalSDKContext = global_context()
        # TODO should be a list
        return context.wrapper_factory().create(result)
    else:
        print("`X` is not a Sarus object, fitting on synthetic data.")
        return sk_model_selection.train_test_split(X, y, *args, **kwargs)


class RepeatedStratifiedKFold(DataSpecWrapper):
    def __init__(
        self,
        *,
        n_splits=5,
        n_repeats=10,
        random_state=None,
        _dataspec=None,
    ):
        if _dataspec is None:
            _dataspec = model(
                model_class=sp.Scalar.Model.ModelClass.SK_REPEATED_STRATIFIED_KFOLD,
                n_splits=n_splits,
                n_repeats=n_repeats,
                random_state=random_state,
            )
            variant_constraint(st.ConstraintKind.PUBLIC, _dataspec)

        super().__init__(dataspec=_dataspec)

    def split(self, X, y):
        all_dataspec = True
        if not isinstance(X, DataSpecWrapper):
            print("`X` is not a Sarus object, fitting on synthetic data.")
            all_dataspec = False
        if not isinstance(y, DataSpecWrapper):
            print("`y` is not a Sarus object, fitting on synthetic data.")
            all_dataspec = False

        if all_dataspec:
            new_scalar = external(
                sp.Transform.ExternalOp.SK_REPEATED_STRATIFIED_KFOLD
            )(
                self._dataspec,
                X._dataspec,
                y._dataspec,
            )
            return RepeatedStratifiedKFold(_dataspec=new_scalar)
        else:
            model_value = self.value()
            model_value.split(X, y)
            return model_value

    def value(self) -> sk_model_selection.RepeatedStratifiedKFold:
        """Return value of synthetic variant."""
        syn_dataspec = self.dataspec(kind=DataSpecVariant.ALTERNATIVE)
        if syn_dataspec.prototype() == sp.Dataset:
            raise TypeError(
                "A Dataset cannot be a sklearn.preprocessing.OneHotEncoder."
            )
        else:
            scalar = cast(st.Scalar, syn_dataspec)
            return cast(
                sk_model_selection.RepeatedStratifiedKFold, scalar.value()
            )
