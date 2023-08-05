from __future__ import annotations

from typing import cast

import sarus_data_spec.protobuf as sp
import sarus_data_spec.typing as st
from sarus_data_spec.scalar import model
from sarus_data_spec.transform import external
from sarus_data_spec.variant_constraint import variant_constraint

from sarus.dataspec_wrapper import DataSpecWrapper
from sarus.typing import DataSpecVariant

try:
    import sklearn.svm as svm
except ModuleNotFoundError:
    pass  # error message in sarus_data_spec.typing


class SVC(DataSpecWrapper):
    def __init__(
        self,
        *,
        C=1.0,
        kernel="rbf",
        degree=3,
        gamma="scale",
        coef0=0.0,
        shrinking=True,
        probability=False,
        tol=1e-3,
        cache_size=200,
        class_weight=None,
        verbose=False,
        max_iter=-1,
        decision_function_shape="ovr",
        break_ties=False,
        random_state=None,
        _dataspec=None,
    ):
        if _dataspec is None:
            _dataspec = model(
                model_class=sp.Scalar.Model.ModelClass.SK_SVC,
                kernel=kernel,
                degree=degree,
                gamma=gamma,
                coef0=coef0,
                tol=tol,
                C=C,
                shrinking=shrinking,
                probability=probability,
                cache_size=cache_size,
                class_weight=class_weight,
                verbose=verbose,
                max_iter=max_iter,
                decision_function_shape=decision_function_shape,
                break_ties=break_ties,
                random_state=random_state,
            )
            variant_constraint(st.ConstraintKind.PUBLIC, _dataspec)

        super().__init__(dataspec=_dataspec)

    def fit(self, X, y, sample_weight=None):
        all_dataspec = True
        if not isinstance(X, DataSpecWrapper):
            print("`X` is not a Sarus object, fitting on synthetic data.")
            all_dataspec = False
        if not isinstance(y, DataSpecWrapper):
            print("`y` is not a Sarus object, fitting on synthetic data.")
            all_dataspec = False

        if all_dataspec:
            new_scalar = external(
                sp.Transform.ExternalOp.SK_FIT, sample_weight=sample_weight
            )(
                self._dataspec,
                X._dataspec,
                y._dataspec,
            )
            return SVC(_dataspec=new_scalar)
        else:
            model_value = self.value()
            model_value.fit(X, y, sample_weight=sample_weight)
            return model_value

    def value(self) -> svm.SVC:
        """Return value of synthetic variant."""
        syn_dataspec = self.dataspec(kind=DataSpecVariant.ALTERNATIVE)
        if syn_dataspec.prototype() == sp.Dataset:
            raise TypeError("A Dataset cannot be a sklearn.svm.SVC.")
        else:
            scalar = cast(st.Scalar, syn_dataspec)
            return cast(svm.SVC, scalar.value())
