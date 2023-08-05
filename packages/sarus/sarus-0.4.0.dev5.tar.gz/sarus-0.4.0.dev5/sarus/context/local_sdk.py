from typing import cast

import numpy as np
import sarus_data_spec.protobuf as sp
import xgboost
from sarus_data_spec.context.public import Public as PublicContext
from sarus_data_spec.dataset import Dataset
from sarus_data_spec.factory import Factory
from sarus_data_spec.scalar import Scalar

from sarus.manager.local_sdk import LocalSDKManager, manager
from sarus.numpy import ndarray
from sarus.pandas.dataframe import DataFrame, Series
from sarus.sklearn.cluster import (
    DBSCAN,
    OPTICS,
    AffinityPropagation,
    AgglomerativeClustering,
    Birch,
    FeatureAgglomeration,
    KMeans,
    MeanShift,
    MiniBatchKMeans,
    SpectralBiclustering,
    SpectralClustering,
    SpectralCoclustering,
)
from sarus.sklearn.decomposition import PCA
from sarus.sklearn.ensemble import (
    AdaBoostClassifier,
    AdaBoostRegressor,
    BaggingClassifier,
    BaggingRegressor,
    ExtraTreesClassifier,
    ExtraTreesRegressor,
    GradientBoostingClassifier,
    GradientBoostingRegressor,
    HistGradientBoostingClassifier,
    HistGradientBoostingRegressor,
    IsolationForest,
    RandomForestClassifier,
    RandomForestRegressor,
    RandomTreesEmbedding,
    StackingClassifier,
    StackingRegressor,
    VotingClassifier,
    VotingRegressor,
)
from sarus.sklearn.model_selection import RepeatedStratifiedKFold
from sarus.sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sarus.sklearn.svm import SVC
from sarus.std import Float, Int, List

# from sarus.storage.local import Storage
from sarus_data_spec.storage.local import Storage
from sarus.typing import Client
from sarus.wrapper_factory import DataSpecWrapperFactory
from sarus.xgboost.xgboost import XGBClassifier

try:
    from sklearn import (
        cluster,
        decomposition,
        ensemble,
        model_selection,
        preprocessing,
        svm,
    )

    HAS_SKLEARN = True
except ModuleNotFoundError:
    HAS_SKLEARN = False
    pass  # error message in sarus_data_spec.typing
import pandas as pd

from ..typing import SyncPolicy


class LocalSDKContext(PublicContext):
    """A default context"""

    def __init__(self, client: Client) -> None:
        super().__init__()
        self._storage = Storage()  # type:ignore
        self._sync_policy = SyncPolicy.SEND_ON_INIT
        self.client = client
        self._manager = manager(self.storage(), self.client)

        self._dataspec_factory = Factory()
        self.factory().register(
            sp.type_name(sp.Dataset),
            lambda protobuf: Dataset(cast(sp.Dataset, protobuf)),
        )
        self.factory().register(
            sp.type_name(sp.Scalar),
            lambda protobuf: Scalar(cast(sp.Scalar, protobuf)),
        )

        self._wrapper_factory = DataSpecWrapperFactory()
        self._wrapper_factory.register(
            python_classname=str(pd.DataFrame),
            sarus_wrapper_class=DataFrame,
        )
        self._wrapper_factory.register(
            python_classname=str(pd.Series),
            sarus_wrapper_class=Series,
        )
        self._wrapper_factory.register(
            python_classname=str(np.ndarray),
            sarus_wrapper_class=ndarray,
        )
        self._wrapper_factory.register(
            python_classname=str(int),
            sarus_wrapper_class=Int,
        )
        self._wrapper_factory.register(
            python_classname=str(float),
            sarus_wrapper_class=Float,
        )
        self._wrapper_factory.register(
            python_classname=str(list),
            sarus_wrapper_class=List,
        )
        if HAS_SKLEARN:
            self._wrapper_factory.register(
                python_classname=str(svm.SVC),
                sarus_wrapper_class=SVC,
            )
            self._wrapper_factory.register(
                python_classname=str(preprocessing.OneHotEncoder),
                sarus_wrapper_class=OneHotEncoder,
            )
            self._wrapper_factory.register(
                python_classname=str(preprocessing.LabelEncoder),
                sarus_wrapper_class=LabelEncoder,
            )
            self._wrapper_factory.register(
                python_classname=str(decomposition.PCA),
                sarus_wrapper_class=PCA,
            )

            # cluster
            self._wrapper_factory.register(
                python_classname=str(cluster.AffinityPropagation),
                sarus_wrapper_class=AffinityPropagation,
            )
            self._wrapper_factory.register(
                python_classname=str(cluster.AgglomerativeClustering),
                sarus_wrapper_class=AgglomerativeClustering,
            )
            self._wrapper_factory.register(
                python_classname=str(cluster.Birch),
                sarus_wrapper_class=Birch,
            )
            self._wrapper_factory.register(
                python_classname=str(cluster.DBSCAN),
                sarus_wrapper_class=DBSCAN,
            )
            self._wrapper_factory.register(
                python_classname=str(cluster.FeatureAgglomeration),
                sarus_wrapper_class=FeatureAgglomeration,
            )
            self._wrapper_factory.register(
                python_classname=str(cluster.KMeans),
                sarus_wrapper_class=KMeans,
            )
            self._wrapper_factory.register(
                python_classname=str(cluster.MiniBatchKMeans),
                sarus_wrapper_class=MiniBatchKMeans,
            )
            self._wrapper_factory.register(
                python_classname=str(cluster.MeanShift),
                sarus_wrapper_class=MeanShift,
            )
            self._wrapper_factory.register(
                python_classname=str(cluster.OPTICS),
                sarus_wrapper_class=OPTICS,
            )
            self._wrapper_factory.register(
                python_classname=str(cluster.SpectralClustering),
                sarus_wrapper_class=SpectralClustering,
            )
            self._wrapper_factory.register(
                python_classname=str(cluster.SpectralBiclustering),
                sarus_wrapper_class=SpectralBiclustering,
            )
            self._wrapper_factory.register(
                python_classname=str(cluster.SpectralCoclustering),
                sarus_wrapper_class=SpectralCoclustering,
            )

            # ensemble
            self._wrapper_factory.register(
                python_classname=str(ensemble.AdaBoostClassifier),
                sarus_wrapper_class=AdaBoostClassifier,
            )
            self._wrapper_factory.register(
                python_classname=str(ensemble.AdaBoostRegressor),
                sarus_wrapper_class=AdaBoostRegressor,
            )
            self._wrapper_factory.register(
                python_classname=str(ensemble.BaggingClassifier),
                sarus_wrapper_class=BaggingClassifier,
            )
            self._wrapper_factory.register(
                python_classname=str(ensemble.BaggingRegressor),
                sarus_wrapper_class=BaggingRegressor,
            )
            self._wrapper_factory.register(
                python_classname=str(ensemble.ExtraTreesClassifier),
                sarus_wrapper_class=ExtraTreesClassifier,
            )
            self._wrapper_factory.register(
                python_classname=str(ensemble.ExtraTreesRegressor),
                sarus_wrapper_class=ExtraTreesRegressor,
            )
            self._wrapper_factory.register(
                python_classname=str(ensemble.GradientBoostingClassifier),
                sarus_wrapper_class=GradientBoostingClassifier,
            )
            self._wrapper_factory.register(
                python_classname=str(ensemble.GradientBoostingRegressor),
                sarus_wrapper_class=GradientBoostingRegressor,
            )
            self._wrapper_factory.register(
                python_classname=str(ensemble.IsolationForest),
                sarus_wrapper_class=IsolationForest,
            )
            self._wrapper_factory.register(
                python_classname=str(ensemble.RandomForestClassifier),
                sarus_wrapper_class=RandomForestClassifier,
            )
            self._wrapper_factory.register(
                python_classname=str(ensemble.RandomForestRegressor),
                sarus_wrapper_class=RandomForestRegressor,
            )
            self._wrapper_factory.register(
                python_classname=str(ensemble.RandomTreesEmbedding),
                sarus_wrapper_class=RandomTreesEmbedding,
            )
            self._wrapper_factory.register(
                python_classname=str(ensemble.StackingClassifier),
                sarus_wrapper_class=StackingClassifier,
            )
            self._wrapper_factory.register(
                python_classname=str(ensemble.StackingRegressor),
                sarus_wrapper_class=StackingRegressor,
            )
            self._wrapper_factory.register(
                python_classname=str(ensemble.VotingClassifier),
                sarus_wrapper_class=VotingClassifier,
            )
            self._wrapper_factory.register(
                python_classname=str(ensemble.VotingRegressor),
                sarus_wrapper_class=VotingRegressor,
            )
            self._wrapper_factory.register(
                python_classname=str(ensemble.HistGradientBoostingClassifier),
                sarus_wrapper_class=HistGradientBoostingClassifier,
            )
            self._wrapper_factory.register(
                python_classname=str(ensemble.HistGradientBoostingRegressor),
                sarus_wrapper_class=HistGradientBoostingRegressor,
            )

            # model selection
            self._wrapper_factory.register(
                python_classname=str(model_selection.RepeatedStratifiedKFold),
                sarus_wrapper_class=RepeatedStratifiedKFold,
            )

            # xgb
            self._wrapper_factory.register(
                python_classname=str(xgboost.XGBClassifier),
                sarus_wrapper_class=XGBClassifier,
            )

    def factory(self) -> Factory:
        return self._dataspec_factory

    def wrapper_factory(self) -> DataSpecWrapperFactory:
        return self._wrapper_factory

    def storage(self) -> Storage:
        return self._storage

    def manager(self) -> LocalSDKManager:
        return self._manager

    def set_sync_policy(self, policy: SyncPolicy) -> None:
        self._sync_policy = policy

    def sync_policy(self) -> SyncPolicy:
        return self._sync_policy
