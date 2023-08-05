from __future__ import annotations

import logging
from typing import cast

import pandas as pd
import sarus_data_spec.protobuf as sp
import sarus_data_spec.typing as st
from sarus_data_spec.context import global_context
from sarus_data_spec.transform import external

from sarus.context.typing import LocalSDKContext
from sarus.dataspec_wrapper import DataSpecVariant, DataSpecWrapper
from sarus.numpy.array import ndarray

logger = logging.getLogger(__name__)


class PandasBase(DataSpecWrapper):
    def __eq__(self, __o: object) -> DataFrame:
        if isinstance(__o, DataSpecWrapper):
            new_dataspec = external(
                sp.Transform.ExternalOp.PD_EQ,
            )(self._dataspec, __o._dataspec)
        else:
            new_dataspec = external(sp.Transform.ExternalOp.PD_EQ, __o)(
                self._dataspec
            )

        context: LocalSDKContext = global_context()
        return context.wrapper_factory().create(new_dataspec)

    def mean(self, *args, **kwargs):
        new_dataspec = external(
            sp.Transform.ExternalOp.PD_MEAN, *args, **kwargs
        )(self._dataspec)

        context: LocalSDKContext = global_context()
        return context.wrapper_factory().create(new_dataspec)

    def std(self, *args, **kwargs):
        new_dataspec = external(
            sp.Transform.ExternalOp.PD_STD, *args, **kwargs
        )(self._dataspec)
        context: LocalSDKContext = global_context()
        return context.wrapper_factory().create(new_dataspec)

    def any(self, *args, **kwargs):
        new_dataspec = external(
            sp.Transform.ExternalOp.PD_ANY, *args, **kwargs
        )(self._dataspec)
        context: LocalSDKContext = global_context()
        return context.wrapper_factory().create(new_dataspec)

    def describe(self, *args, **kwargs):
        new_dataspec = external(
            sp.Transform.ExternalOp.PD_DESCRIBE, *args, **kwargs
        )(self._dataspec)
        context: LocalSDKContext = global_context()
        return context.wrapper_factory().create(new_dataspec)

    def join(self, __o: DataSpecWrapper):
        new_dataspec = external(
            sp.Transform.ExternalOp.PD_JOIN,
        )(self._dataspec, __o._dataspec)
        context: LocalSDKContext = global_context()
        return context.wrapper_factory().create(new_dataspec)

    def quantile(self, *args, **kwargs):
        new_dataspec = external(
            sp.Transform.ExternalOp.PD_QUANTILE, *args, **kwargs
        )(self._dataspec)
        context: LocalSDKContext = global_context()
        return context.wrapper_factory().create(new_dataspec)

    def sum(self, *args, **kwargs):
        new_dataspec = external(
            sp.Transform.ExternalOp.PD_SUM, *args, **kwargs
        )(self._dataspec)
        context: LocalSDKContext = global_context()
        return context.wrapper_factory().create(new_dataspec)

    def fillna(self, *args, **kwargs):
        new_dataspec = external(
            sp.Transform.ExternalOp.PD_FILLNA, *args, **kwargs
        )(self._dataspec)
        context: LocalSDKContext = global_context()
        return context.wrapper_factory().create(new_dataspec)

    def round(self, *args, **kwargs):
        new_dataspec = external(
            sp.Transform.ExternalOp.PD_ROUND, *args, **kwargs
        )(self._dataspec)
        context: LocalSDKContext = global_context()
        return context.wrapper_factory().create(new_dataspec)

    def rename(self, *args, **kwargs):
        new_dataspec = external(
            sp.Transform.ExternalOp.PD_RENAME, *args, **kwargs
        )(self._dataspec)
        context: LocalSDKContext = global_context()
        return context.wrapper_factory().create(new_dataspec)

    def count(self, *args, **kwargs):
        new_dataspec = external(
            sp.Transform.ExternalOp.PD_COUNT, *args, **kwargs
        )(self._dataspec)
        context: LocalSDKContext = global_context()
        return context.wrapper_factory().create(new_dataspec)

    def transpose(self, *args, **kwargs):
        new_dataspec = external(
            sp.Transform.ExternalOp.PD_TRANSPOSE, *args, **kwargs
        )(self._dataspec)
        context: LocalSDKContext = global_context()
        return context.wrapper_factory().create(new_dataspec)

    def unique(self, *args, **kwargs):
        new_dataspec = external(
            sp.Transform.ExternalOp.PD_UNIQUE, *args, **kwargs
        )(self._dataspec)
        context: LocalSDKContext = global_context()
        return context.wrapper_factory().create(new_dataspec)

    def value_counts(self, *args, **kwargs):
        new_dataspec = external(
            sp.Transform.ExternalOp.PD_VALUE_COUNTS, *args, **kwargs
        )(self._dataspec)
        context: LocalSDKContext = global_context()
        return context.wrapper_factory().create(new_dataspec)

    def to_dict(self, *args, **kwargs):
        new_dataspec = external(
            sp.Transform.ExternalOp.PD_TO_DICT, *args, **kwargs
        )(self._dataspec)
        context: LocalSDKContext = global_context()
        return context.wrapper_factory().create(new_dataspec)

    def apply(self, *args, **kwargs):
        # logger.warning(
        #     "`apply` id unsafe. Will be upgraded in future versions."
        # )
        new_dataspec = external(
            sp.Transform.ExternalOp.PD_APPLY, *args, **kwargs
        )(self._dataspec)
        context: LocalSDKContext = global_context()
        return context.wrapper_factory().create(new_dataspec)

    def median(self, *args, **kwargs):
        new_dataspec = external(
            sp.Transform.ExternalOp.PD_MEDIAN, *args, **kwargs
        )(self._dataspec)
        context: LocalSDKContext = global_context()
        return context.wrapper_factory().create(new_dataspec)

    def abs(self, *args, **kwargs):
        new_dataspec = external(
            sp.Transform.ExternalOp.PD_ABS, *args, **kwargs
        )(self._dataspec)
        context: LocalSDKContext = global_context()
        return context.wrapper_factory().create(new_dataspec)

    def mad(self, *args, **kwargs):
        new_dataspec = external(
            sp.Transform.ExternalOp.PD_MAD, *args, **kwargs
        )(self._dataspec)
        context: LocalSDKContext = global_context()
        return context.wrapper_factory().create(new_dataspec)

    def skew(self, *args, **kwargs):
        new_dataspec = external(
            sp.Transform.ExternalOp.PD_SKEW, *args, **kwargs
        )(self._dataspec)
        context: LocalSDKContext = global_context()
        return context.wrapper_factory().create(new_dataspec)

    def kurtosis(self, *args, **kwargs):
        new_dataspec = external(
            sp.Transform.ExternalOp.PD_KURTOSIS, *args, **kwargs
        )(self._dataspec)
        context: LocalSDKContext = global_context()
        return context.wrapper_factory().create(new_dataspec)

    def agg(self, *args, **kwargs):
        new_dataspec = external(
            sp.Transform.ExternalOp.PD_AGG, *args, **kwargs
        )(self._dataspec)
        context: LocalSDKContext = global_context()
        return context.wrapper_factory().create(new_dataspec)

    def droplevel(self, *args, **kwargs):
        new_dataspec = external(
            sp.Transform.ExternalOp.PD_DROPLEVEL, *args, **kwargs
        )(self._dataspec)
        context: LocalSDKContext = global_context()
        return context.wrapper_factory().create(new_dataspec)

    def sort_values(self, *args, **kwargs):
        new_dataspec = external(
            sp.Transform.ExternalOp.PD_SORT_VALUES, *args, **kwargs
        )(self._dataspec)
        context: LocalSDKContext = global_context()
        return context.wrapper_factory().create(new_dataspec)

    def drop(self, *args, **kwargs):
        new_dataspec = external(
            sp.Transform.ExternalOp.PD_DROP, *args, **kwargs
        )(self._dataspec)
        context: LocalSDKContext = global_context()
        return context.wrapper_factory().create(new_dataspec)

    def corr(self, *args, **kwargs):
        new_dataspec = external(
            sp.Transform.ExternalOp.PD_CORR, *args, **kwargs
        )(self._dataspec)
        context: LocalSDKContext = global_context()
        return context.wrapper_factory().create(new_dataspec)


class DataFrame(PandasBase):
    def value(self) -> pd.DataFrame:
        """Return value of the alternative variant."""
        dataspec = self.dataspec(kind=DataSpecVariant.ALTERNATIVE)
        if dataspec.prototype() == sp.Dataset:
            dataset = cast(st.Dataset, dataspec)
            return dataset.to_pandas()
        else:
            scalar = cast(st.Scalar, dataspec)
            return cast(pd.DataFrame, scalar.value())

    @property
    def loc(self) -> _SarusLocIndexer:
        return _SarusLocIndexer(self)

    def __getattr__(self, name):
        if name in self.value().columns:
            return self.loc[:, name]

        return super().__getattr__(name=name)

    def select_dtypes(self, *args, **kwargs):
        new_dataspec = external(
            sp.Transform.ExternalOp.PD_SELECT_DTYPES, *args, **kwargs
        )(self._dataspec)
        context: LocalSDKContext = global_context()
        return context.wrapper_factory().create(new_dataspec)


class _SarusLocIndexer:
    def __init__(self, df: DataFrame) -> None:
        self.df = df

    def __getitem__(self, key) -> DataFrame:
        new_dataspec = external(sp.Transform.ExternalOp.PD_LOC, key)(
            self.df._dataspec
        )
        context: LocalSDKContext = global_context()
        return context.wrapper_factory().create(new_dataspec)


class Series(PandasBase):
    def value(self) -> pd.Series:
        """Return value of the alternative variant."""
        dataspec = self.dataspec(kind=DataSpecVariant.ALTERNATIVE)

        if dataspec.prototype() == sp.Dataset:
            dataset = cast(st.Dataset, dataspec)
            value = dataset.to_pandas()
            if isinstance(value, pd.DataFrame):
                value = value.squeeze()
            return value
        else:
            scalar = cast(st.Scalar, dataspec)
            return cast(pd.Series, scalar.value())


def get_dummies(a: DataSpecWrapper, *args, **kwargs) -> DataSpecWrapper:
    new_dataspec = external(
        sp.Transform.ExternalOp.PD_GET_DUMMIES,
        *args,
        **kwargs,
    )(a.dataspec(DataSpecVariant.USER_DEFINED))
    context: LocalSDKContext = global_context()
    return context.wrapper_factory().create(new_dataspec)


def concat(objs: DataSpecWrapper, *args, **kwargs) -> DataSpecWrapper:

    new_dataspec = external(
        sp.Transform.ExternalOp.PD_CONCAT,
        *args,
        **kwargs,
    )(
        ndarray(
            [obj.dataspec(DataSpecVariant.USER_DEFINED) for obj in objs]
        ).dataspec(DataSpecVariant.USER_DEFINED)
    )
    context: LocalSDKContext = global_context()
    return context.wrapper_factory().create(new_dataspec)
