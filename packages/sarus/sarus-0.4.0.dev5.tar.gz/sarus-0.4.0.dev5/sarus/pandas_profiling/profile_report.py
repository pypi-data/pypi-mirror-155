import sarus_data_spec.protobuf as sp
from sarus_data_spec.transform import external

import sarus.pandas as spd
from sarus.dataspec_wrapper import DataSpecWrapper
from sarus.typing import DataSpecVariant


class ProfileReport(DataSpecWrapper):
    def __init__(self, df=None, **kwargs) -> None:
        if not isinstance(df, spd.DataFrame):
            raise TypeError(
                f"df is not an instance of sarus.pandas.DataFrame."
            )

        parent_dataspec = df.dataspec(kind=DataSpecVariant.USER_DEFINED)
        dataspec = external(
            sp.Transform.ExternalOp.PD_PROFILE_REPORT, **kwargs
        )(parent_dataspec)
        super().__init__(dataspec)

    def value(self):
        dataspec = self.dataspec(kind=DataSpecVariant.ALTERNATIVE)
        return dataspec.value()
