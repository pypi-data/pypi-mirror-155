import inspect
import logging
from typing import Any, Dict, Iterable, Optional, Union

import requests
import sarus_data_spec.protobuf as sp
import sarus_data_spec.typing as st
from sarus_data_spec.context import global_context
from sarus_data_spec.protobuf.utilities import dict_deserialize
from sarus_data_spec.transform import external

from sarus.context.typing import LocalSDKContext

from .typing import DataSpecVariant, DataSpecWrapper, SyncPolicy

logger = logging.getLogger(__name__)


IGNORE_WARNING = [
    "_ipython_canary_method_should_not_exist_",
]


class DataSpecWrapper:
    """This class wraps Sarus DataSpecs objects for the SDK.

    More specifically, it wraps 3 variants of the same DataSpec. These variants
    can be identified with the DataSpecVariant enum:
    - USER_DEFINED: the DataSpec as defined by the user
    - SYNTHETIC: the synthetic variant of the USER_DEFINED DataSpec
    - MOCK: a small sample of the SYNTHETIC variant

    The wrapper has a fallback behavior implemented in the __getattr__ method.
    Any attribute access attempt that is not explicitly catched by a method
    will be delegated to the SYNTHETIC dataspec's value.

    Subclasses such as sarus.pandas.DataFrame must implement the `value` method.
    """

    # This is a class variable hoding all DataSpecWrapper instances
    # This is used by the `dataspec_wrapper_symbols` method.
    instances: Dict[str, int] = dict()

    def __init__(self, dataspec: st.DataSpec) -> None:
        self._dataspec = dataspec
        self._alt_dataspec = None
        # This class only works with a LocalSDKContext
        context: LocalSDKContext = global_context()
        assert isinstance(context, LocalSDKContext)
        self._manager = context.manager()
        if context.sync_policy() == SyncPolicy.SEND_ON_INIT:
            self.send_server(execute=True)

        DataSpecWrapper.instances[dataspec.uuid()] = id(self)
        DataSpecWrapper.instances[
            self.dataspec(DataSpecVariant.SYNTHETIC).uuid()
        ] = id(self)

    def python_type(self) -> Optional[str]:
        """Return the value's Python type name.

        The LocalSDKManager registers an attribute holding the MOCK value's
        Python type (see `LocalSDKManagerinfer_output_type` method). This is
        used to instantiate the right DataSpecWrapper class e.g. instantiate a
        sarus.pandas.DataFrame if the Python value is a pandas.DataFrame.
        """
        return self._manager.python_type(self)

    def dataspec_wrapper_symbols(
        self, f_locals, f_globals
    ) -> Dict[str, Optional[str]]:
        """Returns the symbols table in the caller's namespace.

        For instance, if the data practitioner defines a DataSpecWrapper using
        the symbol X in his code (e.g. X = dataset.as_pandas()) then the symbol
        table contain the mapping between the DataSpecWrapper instances' ids
        and their symbols. This is used to make the dot representation more
        readable.
        """
        mapping = {
            id(obj): symbol
            for symbol, obj in f_locals.items()
            if isinstance(obj, DataSpecWrapper)
        }
        mapping.update(
            {
                id(obj): symbol
                for symbol, obj in f_globals.items()
                if isinstance(obj, DataSpecWrapper)
            }
        )
        symbols = dict()
        for uuid, _id in DataSpecWrapper.instances.items():
            symbols[uuid] = mapping.get(_id, None)
        return symbols

    def dot(
        self,
        kind: DataSpecVariant = DataSpecVariant.USER_DEFINED,
        remote: bool = True,
    ) -> str:
        ds = self.dataspec(kind)
        caller_frame = inspect.currentframe().f_back
        symbols = self.dataspec_wrapper_symbols(
            caller_frame.f_locals, caller_frame.f_globals
        )
        """Graphviz's dot representation of the DataSpecWrapper graph.

        Uses color codes to show statuses.

        Args:
            kind (DataSpecVariant): the DataSpec to represent.
            remote (true): Which Manager to inspect.
                If true shows the DataSpec's status on the server,
                else show the DataSpec's status locally.
        """
        return self._manager.dot(ds, symbols=symbols, remote=remote)

    def send_server(self, execute: bool = False) -> requests.Response:
        """Send the DataSpec graph to the server.

        The server sends an alternative DataSpec back which is compliant with
        the privacy policy defined for the current user.

        Args:
            execute (bool): If true, tell the server to compute the value.
        """
        dataspec = self.dataspec(kind=DataSpecVariant.USER_DEFINED)
        resp = self._manager._post_dataspec(dataspec, execute=execute)

        resp.raise_for_status()

        # Register the alternative DataSpec
        resp_dict = resp.json()
        alt_protobuf = dict_deserialize(resp_dict["alternative"])
        context: LocalSDKContext = global_context()
        self._alt_dataspec = context.factory().create(alt_protobuf)
        DataSpecWrapper.instances[self._alt_dataspec.uuid()] = id(self)

    def delete_from_server(self) -> None:
        """Delete a DataSpec from the server's storage."""
        dataspec = self.dataspec(kind=DataSpecVariant.USER_DEFINED)
        self._manager._delete_remote(dataspec.uuid())

    def delete_from_local(self) -> None:
        """Delete a DataSpec from the local storage."""
        dataspec = self.dataspec(kind=DataSpecVariant.USER_DEFINED)
        self._manager._delete_local(dataspec.uuid())

    def dataspec(
        self, kind: DataSpecVariant = DataSpecVariant.USER_DEFINED
    ) -> st.DataSpec:
        """Return one of the wrapped DataSpec object."""
        if kind == DataSpecVariant.USER_DEFINED:
            return self._dataspec
        if kind == DataSpecVariant.ALTERNATIVE:
            if self._alt_dataspec:
                return self._alt_dataspec
            else:
                # logger.warning(
                #     "Alternative DataSpec not defined."
                #     " Send DataSpec to server to get an alternative."
                # )
                return self._dataspec.variant(
                    kind=st.ConstraintKind.SYNTHETIC, public_context=[]
                )
        elif kind == DataSpecVariant.SYNTHETIC:
            return self._dataspec.variant(
                kind=st.ConstraintKind.SYNTHETIC, public_context=[]
            )
        elif kind == DataSpecVariant.MOCK:
            return self._manager.mock(self._dataspec)
        else:
            raise ValueError(f"Unknown kind {kind}")

    def value(self) -> st.DataSpecValue:
        """Return the value of synthetic DataSpec's variant."""
        raise NotImplementedError

    def __getattr__(self, name: str) -> Any:
        if name not in IGNORE_WARNING:
            logger.info(
                f"`{name}` not supported by Sarus, "
                "object has been evaluated for this method. "
                "See Sarus documentation."
            )
        return self.value().__getattribute__(name)

    def _ipython_display_(self) -> None:
        display(self.value())

    def __repr__(self) -> str:
        return self.value().__repr__()

    def __len__(self) -> int:
        return len(self.value())

    def __iter__(self) -> Iterable:
        return self.value().__iter__()

    def __bool__(self) -> bool:
        return self.value().__bool__()

    def __eq__(self, __o: object) -> bool:
        return self.value() == __o

    def __add__(self, __o: object) -> Union[DataSpecWrapper, Any]:
        """Registers a new transformed DataSpec from the ADD ops."""
        if isinstance(__o, DataSpecWrapper):
            new_dataspec = external(
                sp.Transform.ExternalOp.ADD,
            )(self._dataspec, __o._dataspec)
        else:
            new_dataspec = external(sp.Transform.ExternalOp.ADD, __o)(
                self._dataspec
            )

        context: LocalSDKContext = global_context()
        return context.wrapper_factory().create(new_dataspec)

    def __radd__(self, __o: object) -> Union[DataSpecWrapper, Any]:
        """Registers a new transformed DataSpec from the ADD ops."""
        return self.__add__(__o)

    def __sub__(self, __o: object) -> Union[DataSpecWrapper, Any]:
        """Registers a new transformed DataSpec from the SUB ops."""
        if isinstance(__o, DataSpecWrapper):
            new_dataspec = external(
                sp.Transform.ExternalOp.SUB,
            )(self._dataspec, __o._dataspec)
        else:
            new_dataspec = external(sp.Transform.ExternalOp.SUB, __o)(
                self._dataspec
            )

        context: LocalSDKContext = global_context()
        return context.wrapper_factory().create(new_dataspec)

    def __rsub__(self, __o: object) -> Union[DataSpecWrapper, Any]:
        """Registers a new transformed DataSpec from the SUB ops."""
        if isinstance(__o, DataSpecWrapper):
            new_dataspec = external(sp.Transform.ExternalOp.SUB, invert=True)(
                self._dataspec, __o._dataspec
            )
        else:
            new_dataspec = external(
                sp.Transform.ExternalOp.SUB, __o, invert=True
            )(self._dataspec)

        context: LocalSDKContext = global_context()
        return context.wrapper_factory().create(new_dataspec)

    def __mul__(self, __o: object) -> Union[DataSpecWrapper, Any]:
        """Registers a new transformed DataSpec from the MUL ops."""
        if isinstance(__o, DataSpecWrapper):
            new_dataspec = external(
                sp.Transform.ExternalOp.MUL,
            )(self._dataspec, __o._dataspec)
        else:
            new_dataspec = external(sp.Transform.ExternalOp.MUL, __o)(
                self._dataspec
            )

        context: LocalSDKContext = global_context()
        return context.wrapper_factory().create(new_dataspec)

    def __rmul__(self, __o: object) -> Union[DataSpecWrapper, Any]:
        """Registers a new transformed DataSpec from the MUL ops."""
        return self.__mul__(__o)

    def __truediv__(self, __o: object) -> Union[DataSpecWrapper, Any]:
        """Registers a new transformed DataSpec from the DIV ops."""
        if isinstance(__o, DataSpecWrapper):
            new_dataspec = external(
                sp.Transform.ExternalOp.DIV,
            )(self._dataspec, __o._dataspec)
        else:
            new_dataspec = external(sp.Transform.ExternalOp.DIV, __o)(
                self._dataspec
            )

        context: LocalSDKContext = global_context()
        return context.wrapper_factory().create(new_dataspec)

    def __rtruediv__(self, __o: object) -> Union[DataSpecWrapper, Any]:
        """Registers a new transformed DataSpec from the DIV ops."""
        if isinstance(__o, DataSpecWrapper):
            new_dataspec = external(sp.Transform.ExternalOp.DIV, invert=True)(
                self._dataspec, __o._dataspec
            )
        else:
            new_dataspec = external(
                sp.Transform.ExternalOp.DIV, __o, invert=True
            )(self._dataspec)

        context: LocalSDKContext = global_context()
        return context.wrapper_factory().create(new_dataspec)

    def __invert__(self):
        """Registers a new transformed DataSpec from the INVERT ops."""
        new_dataspec = external(sp.Transform.ExternalOp.INVERT)(self._dataspec)
        context: LocalSDKContext = global_context()
        return context.wrapper_factory().create(new_dataspec)

    def __getitem__(self, __o: object) -> Any:
        if isinstance(__o, DataSpecWrapper):
            new_dataspec = external(
                sp.Transform.ExternalOp.GETITEM,
            )(self._dataspec, __o._dataspec)
        else:
            new_dataspec = external(sp.Transform.ExternalOp.GETITEM, __o)(
                self._dataspec
            )
        context: LocalSDKContext = global_context()
        return context.wrapper_factory().create(new_dataspec)

    def __ge__(self, __o: object) -> Union[DataSpecWrapper, Any]:
        """Registers a new transformed DataSpec from the GE ops."""
        op_code = sp.Transform.ExternalOp.GE
        if isinstance(__o, DataSpecWrapper):
            new_dataspec = external(op_code)(self._dataspec, __o._dataspec)
        else:
            new_dataspec = external(op_code, __o)(self._dataspec)

        context: LocalSDKContext = global_context()
        return context.wrapper_factory().create(new_dataspec)

    def __gt__(self, __o: object) -> Union[DataSpecWrapper, Any]:
        """Registers a new transformed DataSpec from the GT ops."""
        op_code = sp.Transform.ExternalOp.GT
        if isinstance(__o, DataSpecWrapper):
            new_dataspec = external(op_code)(self._dataspec, __o._dataspec)
        else:
            new_dataspec = external(op_code, __o)(self._dataspec)

        context: LocalSDKContext = global_context()
        return context.wrapper_factory().create(new_dataspec)

    def __le__(self, __o: object) -> Union[DataSpecWrapper, Any]:
        """Registers a new transformed DataSpec from the LE ops."""
        op_code = sp.Transform.ExternalOp.LE
        if isinstance(__o, DataSpecWrapper):
            new_dataspec = external(op_code)(self._dataspec, __o._dataspec)
        else:
            new_dataspec = external(op_code, __o)(self._dataspec)

        context: LocalSDKContext = global_context()
        return context.wrapper_factory().create(new_dataspec)

    def __lt__(self, __o: object) -> Union[DataSpecWrapper, Any]:
        """Registers a new transformed DataSpec from the LT ops."""
        op_code = sp.Transform.ExternalOp.LT
        if isinstance(__o, DataSpecWrapper):
            new_dataspec = external(op_code)(self._dataspec, __o._dataspec)
        else:
            new_dataspec = external(op_code, __o)(self._dataspec)

        context: LocalSDKContext = global_context()
        return context.wrapper_factory().create(new_dataspec)

    def __ne__(self, __o: object) -> Union[DataSpecWrapper, Any]:
        """Registers a new transformed DataSpec from the NE ops."""
        op_code = sp.Transform.ExternalOp.NE
        if isinstance(__o, DataSpecWrapper):
            new_dataspec = external(op_code)(self._dataspec, __o._dataspec)
        else:
            new_dataspec = external(op_code, __o)(self._dataspec)

        context: LocalSDKContext = global_context()
        return context.wrapper_factory().create(new_dataspec)

    def __mod__(self, __o: object) -> Union[DataSpecWrapper, Any]:
        """Registers a new transformed DataSpec from the MOD ops."""
        op_code = sp.Transform.ExternalOp.MOD
        if isinstance(__o, DataSpecWrapper):
            new_dataspec = external(op_code)(self._dataspec, __o._dataspec)
        else:
            new_dataspec = external(op_code, __o)(self._dataspec)

        context: LocalSDKContext = global_context()
        return context.wrapper_factory().create(new_dataspec)

    def __rmod__(self, __o: object) -> Union[DataSpecWrapper, Any]:
        """Registers a new transformed DataSpec from the MOD ops."""
        op_code = sp.Transform.ExternalOp.MOD
        if isinstance(__o, DataSpecWrapper):
            new_dataspec = external(op_code, invert=True)(
                self._dataspec, __o._dataspec
            )
        else:
            new_dataspec = external(op_code, __o, invert=True)(self._dataspec)

        context: LocalSDKContext = global_context()
        return context.wrapper_factory().create(new_dataspec)

    def __and__(self, __o: object) -> Union[DataSpecWrapper, Any]:
        """Registers a new transformed DataSpec from the AND ops."""
        op_code = sp.Transform.ExternalOp.AND
        if isinstance(__o, DataSpecWrapper):
            new_dataspec = external(op_code)(self._dataspec, __o._dataspec)
        else:
            new_dataspec = external(op_code, __o)(self._dataspec)

        context: LocalSDKContext = global_context()
        return context.wrapper_factory().create(new_dataspec)

    def __rand__(self, __o: object) -> Union[DataSpecWrapper, Any]:
        """Registers a new transformed DataSpec from the AND ops."""
        op_code = sp.Transform.ExternalOp.AND
        if isinstance(__o, DataSpecWrapper):
            new_dataspec = external(op_code, invert=True)(
                self._dataspec, __o._dataspec
            )
        else:
            new_dataspec = external(op_code, __o, invert=True)(self._dataspec)

        context: LocalSDKContext = global_context()
        return context.wrapper_factory().create(new_dataspec)

    def __or__(self, __o: object) -> Union[DataSpecWrapper, Any]:
        """Registers a new transformed DataSpec from the OR ops."""
        op_code = sp.Transform.ExternalOp.OR
        if isinstance(__o, DataSpecWrapper):
            new_dataspec = external(op_code)(self._dataspec, __o._dataspec)
        else:
            new_dataspec = external(op_code, __o)(self._dataspec)

        context: LocalSDKContext = global_context()
        return context.wrapper_factory().create(new_dataspec)

    def __ror__(self, __o: object) -> Union[DataSpecWrapper, Any]:
        """Registers a new transformed DataSpec from the OR ops."""
        op_code = sp.Transform.ExternalOp.OR
        if isinstance(__o, DataSpecWrapper):
            new_dataspec = external(op_code, invert=True)(
                self._dataspec, __o._dataspec
            )
        else:
            new_dataspec = external(op_code, __o, invert=True)(self._dataspec)

        context: LocalSDKContext = global_context()
        return context.wrapper_factory().create(new_dataspec)

    def __abs__(self):
        """Registers a new transformed DataSpec from the ABS ops."""
        new_dataspec = external(sp.Transform.ExternalOp.ABS)(self._dataspec)
        context: LocalSDKContext = global_context()
        return context.wrapper_factory().create(new_dataspec)

    def __round__(self):
        """Registers a new transformed DataSpec from the ROUND ops."""
        new_dataspec = external(sp.Transform.ExternalOp.ROUND)(self._dataspec)
        context: LocalSDKContext = global_context()
        return context.wrapper_factory().create(new_dataspec)

    def __pos__(self):
        """Registers a new transformed DataSpec from the POS ops."""
        new_dataspec = external(sp.Transform.ExternalOp.POS)(self._dataspec)
        context: LocalSDKContext = global_context()
        return context.wrapper_factory().create(new_dataspec)

    def __neg__(self):
        """Registers a new transformed DataSpec from the NEG ops."""
        new_dataspec = external(sp.Transform.ExternalOp.NEG)(self._dataspec)
        context: LocalSDKContext = global_context()
        return context.wrapper_factory().create(new_dataspec)
