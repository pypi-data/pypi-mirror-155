from __future__ import annotations

from typing import cast

import numpy as np
import sarus_data_spec.protobuf as sp
import sarus_data_spec.typing as st
from sarus_data_spec.context import global_context
from sarus_data_spec.transform import external

from sarus.context.typing import LocalSDKContext
from sarus.dataspec_wrapper import DataSpecWrapper
from sarus.typing import DataSpecVariant


class ndarray(DataSpecWrapper):
    def value(self) -> np.ndarray:
        """Return value of the alternative variant."""
        dataspec = self.dataspec(kind=DataSpecVariant.ALTERNATIVE)
        assert dataspec.prototype() == sp.Scalar
        scalar = cast(st.Scalar, dataspec)
        return cast(np.ndarray, scalar.value())

    def mean(self, *args, **kwargs):
        new_dataspec = external(
            sp.Transform.ExternalOp.NP_MEAN,
            *args,
            **kwargs,
        )(self.dataspec(DataSpecVariant.USER_DEFINED))
        context: LocalSDKContext = global_context()
        return context.wrapper_factory().create(new_dataspec)

    def std(self, *args, **kwargs) -> ndarray:
        new_dataspec = external(
            sp.Transform.ExternalOp.NP_STD,
            *args,
            **kwargs,
        )(self.dataspec(DataSpecVariant.USER_DEFINED))
        context: LocalSDKContext = global_context()
        return context.wrapper_factory().create(new_dataspec)


def mean(a: DataSpecWrapper, *args, **kwargs) -> ndarray:
    new_dataspec = external(
        sp.Transform.ExternalOp.NP_MEAN,
        *args,
        **kwargs,
    )(a.dataspec(DataSpecVariant.USER_DEFINED))
    context: LocalSDKContext = global_context()
    return context.wrapper_factory().create(new_dataspec)


def std(a: DataSpecWrapper, *args, **kwargs) -> ndarray:
    new_dataspec = external(
        sp.Transform.ExternalOp.NP_STD,
        *args,
        **kwargs,
    )(a.dataspec(DataSpecVariant.USER_DEFINED))
    context: LocalSDKContext = global_context()
    return context.wrapper_factory().create(new_dataspec)
