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
    import sklearn.decomposition as decomposition
except ModuleNotFoundError:
    pass  # error message in sarus_data_spec.typing


class PCA(DataSpecWrapper):
    def __init__(
        self,
        n_components=None,
        *,
        copy=True,
        whiten=False,
        svd_solver="auto",
        tol=0.0,
        iterated_power="auto",
        random_state=None,
        _dataspec=None,
    ):
        if _dataspec is None:
            _dataspec = model(
                model_class=sp.Scalar.Model.ModelClass.SK_SVC,
                n_components=n_components,
                copy=copy,
                whiten=whiten,
                svd_solver=svd_solver,
                tol=tol,
                iterated_power=iterated_power,
                random_state=random_state,
            )
            variant_constraint(st.ConstraintKind.PUBLIC, _dataspec)

        super().__init__(dataspec=_dataspec)

    def fit(self, X, y=None):
        all_dataspec = True
        if not isinstance(X, DataSpecWrapper):
            print("`X` is not a Sarus object, fitting on synthetic data.")
            all_dataspec = False

        if all_dataspec:
            new_scalar = external(sp.Transform.ExternalOp.SK_PCA)(
                self._dataspec,
                X._dataspec,
            )
            return PCA(_dataspec=new_scalar)
        else:
            model_value = self.value()
            model_value.fit(X, y)
            return model_value

    def value(self) -> decomposition.PCA:
        """Return value of synthetic variant."""
        syn_dataspec = self.dataspec(kind=DataSpecVariant.ALTERNATIVE)
        if syn_dataspec.prototype() == sp.Dataset:
            raise TypeError("A Dataset cannot be a sklearn.decomposition.PCA.")
        else:
            scalar = cast(st.Scalar, syn_dataspec)
            return cast(decomposition.PCA, scalar.value())
