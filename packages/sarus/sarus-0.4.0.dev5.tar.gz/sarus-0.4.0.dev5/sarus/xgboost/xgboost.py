from __future__ import annotations

from typing import Any, Optional, cast

import sarus_data_spec.protobuf as sp
import sarus_data_spec.typing as st
from sarus_data_spec.scalar import model
from sarus_data_spec.transform import external
from sarus_data_spec.variant_constraint import variant_constraint

from sarus.dataspec_wrapper import DataSpecWrapper
from sarus.numpy.array import ndarray
from sarus.typing import DataSpecVariant

try:
    import xgboost
except ModuleNotFoundError:
    pass  # error message in sarus_data_spec.typing


class XGBClassifier(DataSpecWrapper):
    def __init__(
        self,
        *,
        objective="binary:logistic",
        use_label_encoder: Optional[bool] = None,
        _dataspec=None,
        **kwargs: Any,
    ):
        if _dataspec is None:
            _dataspec = model(
                model_class=sp.Scalar.Model.ModelClass.XGB_CLASSIFIER,
                objective=objective,
                use_label_encoder=use_label_encoder,
                **kwargs,
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
                sp.Transform.ExternalOp.XGB_CLASSIFIER,
                sample_weight=sample_weight,
            )(
                self._dataspec,
                X._dataspec,
                y._dataspec,
            )
            return XGBClassifier(_dataspec=new_scalar)
        else:
            model_value = self.value()
            model_value.fit(X, y, sample_weight=sample_weight)
            return model_value

    def predict(self, X):
        all_dataspec = True
        if not isinstance(X, DataSpecWrapper):
            print("`X` is not a Sarus object, fitting on synthetic data.")
            all_dataspec = False

        if all_dataspec:
            new_scalar = external(
                sp.Transform.ExternalOp.XGB_CLASSIFIER_PREDICT
            )(
                self._dataspec,
                X._dataspec,
            )
            return ndarray(dataspec=new_scalar)
        else:
            model_value = self.value()
            return model_value.predict(X)

    def value(self) -> xgboost.XGBClassifier:
        """Return value of synthetic variant."""
        syn_dataspec = self.dataspec(kind=DataSpecVariant.ALTERNATIVE)
        if syn_dataspec.prototype() == sp.Dataset:
            raise TypeError("A Dataset cannot be a xgboost.XGBClassifier.")
        else:
            scalar = cast(st.Scalar, syn_dataspec)
            return cast(xgboost.XGBClassifier, scalar.value())
