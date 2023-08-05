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
    import sklearn.preprocessing as sk_preprocessing
except ModuleNotFoundError:
    pass  # error message in sarus_data_spec.typing


def scale(X: Any, *args, **kwargs):
    if isinstance(X, DataSpecWrapper):
        new_dataspec = external(
            sp.Transform.ExternalOp.SK_SCALE, *args, **kwargs
        )(X._dataspec)
        context: LocalSDKContext = global_context()
        return context.wrapper_factory().create(new_dataspec)
    else:
        return sk_preprocessing.scale(X, *args, **kwargs)


class OneHotEncoder(DataSpecWrapper):
    def __init__(
        self,
        *,
        categories="auto",
        drop=None,
        sparse=True,
        dtype=np.float64,
        handle_unknown="error",
        _dataspec=None,
    ):
        if _dataspec is None:
            _dataspec = model(
                model_class=sp.Scalar.Model.ModelClass.SK_ONEHOT,
                categories=categories,
                drop=drop,
                sparse=sparse,
                dtype=dtype,
                handle_unknown=handle_unknown,
            )
            variant_constraint(st.ConstraintKind.PUBLIC, _dataspec)

        super().__init__(dataspec=_dataspec)

    def fit(self, X, y=None):
        all_dataspec = True
        if not isinstance(X, DataSpecWrapper):
            print("`X` is not a Sarus object, fitting on synthetic data.")
            all_dataspec = False

        if all_dataspec:
            new_scalar = external(sp.Transform.ExternalOp.SK_ONEHOT)(
                self._dataspec,
                X._dataspec,
            )
            return OneHotEncoder(_dataspec=new_scalar)
        else:
            model_value = self.value()
            model_value.fit(X, y)
            return model_value

    def value(self) -> sk_preprocessing.OneHotEncoder:
        """Return value of synthetic variant."""
        syn_dataspec = self.dataspec(kind=DataSpecVariant.ALTERNATIVE)
        if syn_dataspec.prototype() == sp.Dataset:
            raise TypeError(
                "A Dataset cannot be a sklearn.preprocessing.OneHotEncoder."
            )
        else:
            scalar = cast(st.Scalar, syn_dataspec)
            return cast(sk_preprocessing.OneHotEncoder, scalar.value())


class LabelEncoder(DataSpecWrapper):
    def __init__(
        self,
        *,
        _dataspec=None,
    ):
        if _dataspec is None:
            _dataspec = model(
                model_class=sp.Scalar.Model.ModelClass.SK_LABEL_ENCODER,
            )
            variant_constraint(st.ConstraintKind.PUBLIC, _dataspec)

        super().__init__(dataspec=_dataspec)

    def fit_transform(self, X, y=None):
        all_dataspec = True
        if not isinstance(X, DataSpecWrapper):
            print("`X` is not a Sarus object, fitting on synthetic data.")
            all_dataspec = False

        if all_dataspec:
            new_scalar = external(
                sp.Transform.ExternalOp.SK_LABEL_ENCODER_FIT_TRANSFORM
            )(
                self._dataspec,
                X._dataspec,
            )
            return LabelEncoder(_dataspec=new_scalar)
        else:
            model_value = self.value()
            model_value.fit(X, y)
            return model_value

    def value(self) -> sk_preprocessing.OneHotEncoder:
        """Return value of synthetic variant."""
        syn_dataspec = self.dataspec(kind=DataSpecVariant.ALTERNATIVE)
        if syn_dataspec.prototype() == sp.Dataset:
            raise TypeError(
                "A Dataset cannot be a sklearn.preprocessing.OneHotEncoder."
            )
        else:
            scalar = cast(st.Scalar, syn_dataspec)
            return cast(sk_preprocessing.LabelEncoder, scalar.value())
