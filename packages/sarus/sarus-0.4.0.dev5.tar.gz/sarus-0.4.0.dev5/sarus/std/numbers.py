from typing import Any, cast

import sarus_data_spec.protobuf as sp
import sarus_data_spec.typing as st
from sarus_data_spec.context import global_context
from sarus_data_spec.transform import external

from sarus.context.typing import LocalSDKContext
from sarus.dataspec_wrapper import DataSpecWrapper
from sarus.typing import DataSpecVariant


class Int(DataSpecWrapper):
    def value(self) -> int:
        """Return value of the alternative variant."""
        dataspec = self.dataspec(kind=DataSpecVariant.ALTERNATIVE)
        assert dataspec.prototype() == sp.Scalar
        scalar = cast(st.Scalar, dataspec)
        return cast(int, scalar.value())


class Float(DataSpecWrapper):
    def value(self) -> float:
        """Return value of the alternative variant."""
        dataspec = self.dataspec(kind=DataSpecVariant.ALTERNATIVE)
        assert dataspec.prototype() == sp.Scalar
        scalar = cast(st.Scalar, dataspec)
        return cast(float, scalar.value())


class List(DataSpecWrapper):
    def value(self) -> list:
        """Return value of the alternative variant."""
        dataspec = self.dataspec(kind=DataSpecVariant.ALTERNATIVE)
        assert dataspec.prototype() == sp.Scalar
        scalar = cast(st.Scalar, dataspec)
        return cast(list, scalar.value())

    def __getitem__(self, key) -> Any:
        new_dataspec = external(sp.Transform.ExternalOp.GETITEM, key)(
            self.dataspec()
        )
        context: LocalSDKContext = global_context()
        return context.wrapper_factory().create(new_dataspec)
