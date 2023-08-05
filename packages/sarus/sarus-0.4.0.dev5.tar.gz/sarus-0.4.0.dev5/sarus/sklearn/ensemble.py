from __future__ import annotations

from typing import cast

import numpy as np
import sarus_data_spec.protobuf as sp
import sarus_data_spec.typing as st
from sarus_data_spec.scalar import model
from sarus_data_spec.transform import external
from sarus_data_spec.variant_constraint import variant_constraint

from sarus.dataspec_wrapper import DataSpecWrapper
from sarus.numpy.array import ndarray
from sarus.typing import DataSpecVariant

try:
    import sklearn.ensemble as ensemble
except ModuleNotFoundError:
    pass  # error message in sarus_data_spec.typing


class AdaBoostClassifier(DataSpecWrapper):
    def __init__(
        self,
        base_estimator=None,
        *,
        n_estimators=50,
        learning_rate=1.0,
        algorithm="SAMME.R",
        random_state=None,
        _dataspec=None,
    ):
        if _dataspec is None:
            _dataspec = model(
                model_class=sp.Scalar.Model.ModelClass.SK_ADABOOST_CLASSIFIER,
                base_estimator=base_estimator,
                n_estimators=n_estimators,
                learning_rate=learning_rate,
                algorithm=algorithm,
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
            new_scalar = external(
                sp.Transform.ExternalOp.SK_ADABOOST_CLASSIFIER
            )(
                self._dataspec,
                X._dataspec,
                y._dataspec,
            )
            return AdaBoostClassifier(_dataspec=new_scalar)
        else:
            model_value = self.value()
            model_value.fit(X, y)
            return model_value

    def value(self) -> ensemble.AdaBoostClassifier:
        """Return value of synthetic variant."""
        syn_dataspec = self.dataspec(kind=DataSpecVariant.ALTERNATIVE)
        if syn_dataspec.prototype() == sp.Dataset:
            raise TypeError("A Dataset cannot be a sklearn.decomposition.PCA.")
        else:
            scalar = cast(st.Scalar, syn_dataspec)
            return cast(ensemble.AdaBoostClassifier, scalar.value())


class AdaBoostRegressor(DataSpecWrapper):
    def __init__(
        self,
        base_estimator=None,
        *,
        n_estimators=50,
        learning_rate=1.0,
        loss="linear",
        random_state=None,
        _dataspec=None,
    ):
        if _dataspec is None:
            _dataspec = model(
                model_class=sp.Scalar.Model.ModelClass.SK_ADABOOST_REGRESSOR,
                base_estimator=base_estimator,
                n_estimators=n_estimators,
                learning_rate=learning_rate,
                loss=loss,
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
            new_scalar = external(
                sp.Transform.ExternalOp.SK_ADABOOST_REGRESSOR
            )(
                self._dataspec,
                X._dataspec,
                y._dataspec,
            )
            return AdaBoostClassifier(_dataspec=new_scalar)
        else:
            model_value = self.value()
            model_value.fit(X, y)
            return model_value

    def value(self) -> ensemble.AdaBoostRegressor:
        """Return value of synthetic variant."""
        syn_dataspec = self.dataspec(kind=DataSpecVariant.ALTERNATIVE)
        if syn_dataspec.prototype() == sp.Dataset:
            raise TypeError("A Dataset cannot be a sklearn.decomposition.PCA.")
        else:
            scalar = cast(st.Scalar, syn_dataspec)
            return cast(ensemble.AdaBoostRegressor, scalar.value())


class BaggingClassifier(DataSpecWrapper):
    def __init__(
        self,
        base_estimator=None,
        n_estimators=10,
        *,
        max_samples=1.0,
        max_features=1.0,
        bootstrap=True,
        bootstrap_features=False,
        oob_score=False,
        warm_start=False,
        n_jobs=None,
        random_state=None,
        verbose=0,
        _dataspec=None,
    ):
        if _dataspec is None:
            _dataspec = model(
                model_class=sp.Scalar.Model.ModelClass.SK_BAGGING_CLASSIFIER,
                base_estimator=base_estimator,
                n_estimators=n_estimators,
                max_samples=max_samples,
                max_features=max_features,
                bootstrap=bootstrap,
                bootstrap_features=bootstrap_features,
                oob_score=oob_score,
                warm_start=warm_start,
                n_jobs=n_jobs,
                random_state=random_state,
                verbose=verbose,
            )
            variant_constraint(st.ConstraintKind.PUBLIC, _dataspec)

        super().__init__(dataspec=_dataspec)

    def fit(self, X, y=None):
        all_dataspec = True
        if not isinstance(X, DataSpecWrapper):
            print("`X` is not a Sarus object, fitting on synthetic data.")
            all_dataspec = False

        if all_dataspec:
            new_scalar = external(
                sp.Transform.ExternalOp.SK_BAGGING_CLASSIFIER
            )(
                self._dataspec,
                X._dataspec,
                y._dataspec,
            )
            return BaggingClassifier(_dataspec=new_scalar)
        else:
            model_value = self.value()
            model_value.fit(X, y)
            return model_value

    def value(self) -> ensemble.BaggingClassifier:
        """Return value of synthetic variant."""
        syn_dataspec = self.dataspec(kind=DataSpecVariant.ALTERNATIVE)
        if syn_dataspec.prototype() == sp.Dataset:
            raise TypeError("A Dataset cannot be a sklearn.decomposition.PCA.")
        else:
            scalar = cast(st.Scalar, syn_dataspec)
            return cast(ensemble.BaggingClassifier, scalar.value())


class BaggingRegressor(DataSpecWrapper):
    def __init__(
        self,
        base_estimator=None,
        *,
        n_estimators=50,
        learning_rate=1.0,
        loss="linear",
        random_state=None,
        _dataspec=None,
    ):
        if _dataspec is None:
            _dataspec = model(
                model_class=sp.Scalar.Model.ModelClass.SK_BAGGING_REGRESSOR,
                base_estimator=base_estimator,
                n_estimators=n_estimators,
                max_samples=max_samples,
                max_features=max_features,
                bootstrap=bootstrap,
                bootstrap_features=bootstrap_features,
                oob_score=oob_score,
                warm_start=warm_start,
                n_jobs=n_jobs,
                random_state=random_state,
                verbose=verbose,
            )
            variant_constraint(st.ConstraintKind.PUBLIC, _dataspec)

        super().__init__(dataspec=_dataspec)

    def fit(self, X, y=None):
        all_dataspec = True
        if not isinstance(X, DataSpecWrapper):
            print("`X` is not a Sarus object, fitting on synthetic data.")
            all_dataspec = False

        if all_dataspec:
            new_scalar = external(
                sp.Transform.ExternalOp.SK_BAGGING_REGRESSOR
            )(
                self._dataspec,
                X._dataspec,
                y._dataspec,
            )
            return BaggingRegressor(_dataspec=new_scalar)
        else:
            model_value = self.value()
            model_value.fit(X, y)
            return model_value

    def value(self) -> ensemble.BaggingRegressor:
        """Return value of synthetic variant."""
        syn_dataspec = self.dataspec(kind=DataSpecVariant.ALTERNATIVE)
        if syn_dataspec.prototype() == sp.Dataset:
            raise TypeError("A Dataset cannot be a sklearn.decomposition.PCA.")
        else:
            scalar = cast(st.Scalar, syn_dataspec)
            return cast(ensemble.BaggingRegressor, scalar.value())


class ExtraTreesClassifier(DataSpecWrapper):
    def __init__(
        self,
        n_estimators=100,
        *,
        criterion="gini",
        max_depth=None,
        min_samples_split=2,
        min_samples_leaf=1,
        min_weight_fraction_leaf=0.0,
        max_features="sqrt",
        max_leaf_nodes=None,
        min_impurity_decrease=0.0,
        bootstrap=False,
        oob_score=False,
        n_jobs=None,
        random_state=None,
        verbose=0,
        warm_start=False,
        class_weight=None,
        ccp_alpha=0.0,
        max_samples=None,
        _dataspec=None,
    ):
        if _dataspec is None:
            _dataspec = model(
                model_class=sp.Scalar.Model.ModelClass.SK_EXTRA_TREES_CLASSIFIER,
                n_estimators=n_estimators,
                criterion=criterion,
                max_depth=max_depth,
                min_samples_split=min_samples_split,
                min_samples_leaf=min_samples_leaf,
                min_weight_fraction_leaf=min_weight_fraction_leaf,
                max_features=max_features,
                max_leaf_nodes=max_leaf_nodes,
                min_impurity_decrease=min_impurity_decrease,
                bootstrap=bootstrap,
                oob_score=oob_score,
                n_jobs=n_jobs,
                random_state=random_state,
                verbose=verbose,
                warm_start=warm_start,
                class_weight=class_weight,
                ccp_alpha=ccp_alpha,
                max_samples=max_samples,
            )
            variant_constraint(st.ConstraintKind.PUBLIC, _dataspec)

        super().__init__(dataspec=_dataspec)

    def fit(self, X, y=None):
        all_dataspec = True
        if not isinstance(X, DataSpecWrapper):
            print("`X` is not a Sarus object, fitting on synthetic data.")
            all_dataspec = False

        if all_dataspec:
            new_scalar = external(
                sp.Transform.ExternalOp.SK_EXTRA_TREES_CLASSIFIER
            )(
                self._dataspec,
                X._dataspec,
                y._dataspec,
            )
            return ExtraTreesClassifier(_dataspec=new_scalar)
        else:
            model_value = self.value()
            model_value.fit(X, y)
            return model_value

    def value(self) -> ensemble.ExtraTreesClassifier:
        """Return value of synthetic variant."""
        syn_dataspec = self.dataspec(kind=DataSpecVariant.ALTERNATIVE)
        if syn_dataspec.prototype() == sp.Dataset:
            raise TypeError("A Dataset cannot be a sklearn.decomposition.PCA.")
        else:
            scalar = cast(st.Scalar, syn_dataspec)
            return cast(ensemble.ExtraTreesClassifier, scalar.value())


class ExtraTreesRegressor(DataSpecWrapper):
    def __init__(
        self,
        n_estimators=100,
        *,
        criterion="squared_error",
        max_depth=None,
        min_samples_split=2,
        min_samples_leaf=1,
        min_weight_fraction_leaf=0.0,
        max_features=1.0,
        max_leaf_nodes=None,
        min_impurity_decrease=0.0,
        bootstrap=False,
        oob_score=False,
        n_jobs=None,
        random_state=None,
        verbose=0,
        warm_start=False,
        ccp_alpha=0.0,
        max_samples=None,
        _dataspec=None,
    ):
        if _dataspec is None:
            _dataspec = model(
                model_class=sp.Scalar.Model.ModelClass.SK_EXTRA_TREES_REGRESSOR,
                n_estimators=n_estimators,
                criterion=criterion,
                max_depth=max_depth,
                min_samples_split=min_samples_split,
                min_samples_leaf=min_samples_leaf,
                min_weight_fraction_leaf=min_weight_fraction_leaf,
                max_features=max_features,
                max_leaf_nodes=max_leaf_nodes,
                min_impurity_decrease=min_impurity_decrease,
                bootstrap=bootstrap,
                oob_score=oob_score,
                n_jobs=n_jobs,
                random_state=random_state,
                verbose=verbose,
                warm_start=warm_start,
                ccp_alpha=ccp_alpha,
                max_samples=max_samples,
            )
            variant_constraint(st.ConstraintKind.PUBLIC, _dataspec)

        super().__init__(dataspec=_dataspec)

    def fit(self, X, y=None):
        all_dataspec = True
        if not isinstance(X, DataSpecWrapper):
            print("`X` is not a Sarus object, fitting on synthetic data.")
            all_dataspec = False

        if all_dataspec:
            new_scalar = external(
                sp.Transform.ExternalOp.SK_EXTRA_TREES_REGRESSOR
            )(
                self._dataspec,
                X._dataspec,
                y._dataspec,
            )
            return ExtraTreesRegressor(_dataspec=new_scalar)
        else:
            model_value = self.value()
            model_value.fit(X, y)
            return model_value

    def value(self) -> ensemble.ExtraTreesRegressor:
        """Return value of synthetic variant."""
        syn_dataspec = self.dataspec(kind=DataSpecVariant.ALTERNATIVE)
        if syn_dataspec.prototype() == sp.Dataset:
            raise TypeError("A Dataset cannot be a sklearn.decomposition.PCA.")
        else:
            scalar = cast(st.Scalar, syn_dataspec)
            return cast(ensemble.ExtraTreesRegressor, scalar.value())


class GradientBoostingClassifier(DataSpecWrapper):
    def __init__(
        self,
        *,
        loss="log_loss",
        learning_rate=0.1,
        n_estimators=100,
        subsample=1.0,
        criterion="friedman_mse",
        min_samples_split=2,
        min_samples_leaf=1,
        min_weight_fraction_leaf=0.0,
        max_depth=3,
        min_impurity_decrease=0.0,
        init=None,
        random_state=None,
        max_features=None,
        verbose=0,
        max_leaf_nodes=None,
        warm_start=False,
        validation_fraction=0.1,
        n_iter_no_change=None,
        tol=0.0001,
        ccp_alpha=0.0,
        _dataspec=None,
    ):
        if _dataspec is None:
            _dataspec = model(
                model_class=sp.Scalar.Model.ModelClass.SK_GRADIENT_BOOSTING_CLASSIFIER,
                loss=loss,
                learning_rate=learning_rate,
                n_estimators=n_estimators,
                subsample=subsample,
                criterion=criterion,
                min_samples_split=min_samples_split,
                min_samples_leaf=min_samples_leaf,
                min_weight_fraction_leaf=min_weight_fraction_leaf,
                max_depth=max_depth,
                min_impurity_decrease=min_impurity_decrease,
                init=init,
                random_state=random_state,
                max_features=max_features,
                verbose=verbose,
                max_leaf_nodes=max_leaf_nodes,
                warm_start=warm_start,
                validation_fraction=validation_fraction,
                n_iter_no_change=n_iter_no_change,
                tol=tol,
                ccp_alpha=ccp_alpha,
            )
            variant_constraint(st.ConstraintKind.PUBLIC, _dataspec)

        super().__init__(dataspec=_dataspec)

    def fit(self, X, y=None):
        all_dataspec = True
        if not isinstance(X, DataSpecWrapper):
            print("`X` is not a Sarus object, fitting on synthetic data.")
            all_dataspec = False

        if all_dataspec:
            new_scalar = external(
                sp.Transform.ExternalOp.SK_GRADIENT_BOOSTING_CLASSIFIER
            )(
                self._dataspec,
                X._dataspec,
                y._dataspec,
            )
            return GradientBoostingClassifier(_dataspec=new_scalar)
        else:
            model_value = self.value()
            model_value.fit(X, y)
            return model_value

    def value(self) -> ensemble.GradientBoostingClassifier:
        """Return value of synthetic variant."""
        syn_dataspec = self.dataspec(kind=DataSpecVariant.ALTERNATIVE)
        if syn_dataspec.prototype() == sp.Dataset:
            raise TypeError("A Dataset cannot be a sklearn.decomposition.PCA.")
        else:
            scalar = cast(st.Scalar, syn_dataspec)
            return cast(ensemble.GradientBoostingClassifier, scalar.value())


class GradientBoostingRegressor(DataSpecWrapper):
    def __init__(
        self,
        *,
        loss="squared_error",
        learning_rate=0.1,
        n_estimators=100,
        subsample=1.0,
        criterion="friedman_mse",
        min_samples_split=2,
        min_samples_leaf=1,
        min_weight_fraction_leaf=0.0,
        max_depth=3,
        min_impurity_decrease=0.0,
        init=None,
        random_state=None,
        max_features=None,
        alpha=0.9,
        verbose=0,
        max_leaf_nodes=None,
        warm_start=False,
        validation_fraction=0.1,
        n_iter_no_change=None,
        tol=0.0001,
        ccp_alpha=0.0,
        _dataspec=None,
    ):
        if _dataspec is None:
            _dataspec = model(
                model_class=sp.Scalar.Model.ModelClass.SK_GRADIENT_BOOSTING_REGRESSOR,
                loss=loss,
                learning_rate=learning_rate,
                n_estimators=n_estimators,
                subsample=subsample,
                criterion=criterion,
                min_samples_split=min_samples_split,
                min_samples_leaf=min_samples_leaf,
                min_weight_fraction_leaf=min_weight_fraction_leaf,
                max_depth=max_depth,
                min_impurity_decrease=min_impurity_decrease,
                init=init,
                random_state=random_state,
                max_features=max_features,
                verbose=verbose,
                max_leaf_nodes=max_leaf_nodes,
                warm_start=warm_start,
                validation_fraction=validation_fraction,
                n_iter_no_change=n_iter_no_change,
                tol=tol,
                ccp_alpha=ccp_alpha,
            )
            variant_constraint(st.ConstraintKind.PUBLIC, _dataspec)

        super().__init__(dataspec=_dataspec)

    def fit(self, X, y=None):
        all_dataspec = True
        if not isinstance(X, DataSpecWrapper):
            print("`X` is not a Sarus object, fitting on synthetic data.")
            all_dataspec = False

        if all_dataspec:
            new_scalar = external(
                sp.Transform.ExternalOp.SK_GRADIENT_BOOSTING_REGRESSOR
            )(
                self._dataspec,
                X._dataspec,
                y._dataspec,
            )
            return GradientBoostingRegressor(_dataspec=new_scalar)
        else:
            model_value = self.value()
            model_value.fit(X, y)
            return model_value

    def value(self) -> ensemble.GradientBoostingRegressor:
        """Return value of synthetic variant."""
        syn_dataspec = self.dataspec(kind=DataSpecVariant.ALTERNATIVE)
        if syn_dataspec.prototype() == sp.Dataset:
            raise TypeError("A Dataset cannot be a sklearn.decomposition.PCA.")
        else:
            scalar = cast(st.Scalar, syn_dataspec)
            return cast(ensemble.GradientBoostingRegressor, scalar.value())


class IsolationForest(DataSpecWrapper):
    def __init__(
        self,
        *,
        n_estimators=100,
        max_samples="auto",
        contamination="auto",
        max_features=1.0,
        bootstrap=False,
        n_jobs=None,
        random_state=None,
        verbose=0,
        warm_start=False,
        _dataspec=None,
    ):
        if _dataspec is None:
            _dataspec = model(
                model_class=sp.Scalar.Model.ModelClass.SK_ISOLATION_FOREST,
                n_estimators=n_estimators,
                max_samples=max_samples,
                contamination=contamination,
                max_features=max_features,
                bootstrap=bootstrap,
                n_jobs=n_jobs,
                random_state=random_state,
                verbose=verbose,
                warm_start=warm_start,
            )
            variant_constraint(st.ConstraintKind.PUBLIC, _dataspec)

        super().__init__(dataspec=_dataspec)

    def fit(self, X, y=None):
        all_dataspec = True
        if not isinstance(X, DataSpecWrapper):
            print("`X` is not a Sarus object, fitting on synthetic data.")
            all_dataspec = False

        if all_dataspec:
            new_scalar = external(sp.Transform.ExternalOp.SK_ISOLATION_FOREST)(
                self._dataspec,
                X._dataspec,
                y._dataspec,
            )
            return IsolationForest(_dataspec=new_scalar)
        else:
            model_value = self.value()
            model_value.fit(X, y)
            return model_value

    def value(self) -> ensemble.IsolationForest:
        """Return value of synthetic variant."""
        syn_dataspec = self.dataspec(kind=DataSpecVariant.ALTERNATIVE)
        if syn_dataspec.prototype() == sp.Dataset:
            raise TypeError("A Dataset cannot be a sklearn.decomposition.PCA.")
        else:
            scalar = cast(st.Scalar, syn_dataspec)
            return cast(ensemble.IsolationForest, scalar.value())


class RandomForestClassifier(DataSpecWrapper):
    def __init__(
        self,
        n_estimators=100,
        *,
        criterion="gini",
        max_depth=None,
        min_samples_split=2,
        min_samples_leaf=1,
        min_weight_fraction_leaf=0.0,
        max_features="sqrt",
        max_leaf_nodes=None,
        min_impurity_decrease=0.0,
        bootstrap=True,
        oob_score=False,
        n_jobs=None,
        random_state=None,
        verbose=0,
        warm_start=False,
        class_weight=None,
        ccp_alpha=0.0,
        max_samples=None,
        _dataspec=None,
    ):
        if _dataspec is None:
            _dataspec = model(
                model_class=sp.Scalar.Model.ModelClass.SK_RANDOM_FOREST_CLASSIFIER,
                n_estimators=n_estimators,
                criterion=criterion,
                max_depth=max_depth,
                min_samples_split=min_samples_split,
                min_samples_leaf=min_samples_leaf,
                min_weight_fraction_leaf=min_weight_fraction_leaf,
                max_features=max_features,
                max_leaf_nodes=max_leaf_nodes,
                min_impurity_decrease=min_impurity_decrease,
                bootstrap=bootstrap,
                oob_score=oob_score,
                n_jobs=n_jobs,
                random_state=random_state,
                verbose=verbose,
                warm_start=warm_start,
                class_weight=class_weight,
                ccp_alpha=ccp_alpha,
                max_samples=max_samples,
            )
            variant_constraint(st.ConstraintKind.PUBLIC, _dataspec)

        super().__init__(dataspec=_dataspec)

    def fit(self, X, y=None):
        all_dataspec = True
        if not isinstance(X, DataSpecWrapper):
            print("`X` is not a Sarus object, fitting on synthetic data.")
            all_dataspec = False

        if all_dataspec:
            new_scalar = external(
                sp.Transform.ExternalOp.SK_RANDOM_FOREST_CLASSIFIER
            )(
                self._dataspec,
                X._dataspec,
                y._dataspec,
            )
            return RandomForestClassifier(_dataspec=new_scalar)
        else:
            model_value = self.value()
            model_value.fit(X, y)
            return model_value

    def predict(self, X):
        all_dataspec = True
        if not isinstance(X, DataSpecWrapper):
            print("`X` is not a Sarus object, fitting on synthetic data.")
            all_dataspec = False

        if all_dataspec:
            new_scalar = external(
                sp.Transform.ExternalOp.SK_RANDOM_FOREST_CLASSIFIER_PREDICT
            )(
                self._dataspec,
                X._dataspec,
            )
            return ndarray(dataspec=new_scalar)
        else:
            model_value = self.value()
            return model_value.predict(X)

    def value(self) -> ensemble.RandomForestClassifier:
        """Return value of synthetic variant."""
        syn_dataspec = self.dataspec(kind=DataSpecVariant.ALTERNATIVE)
        if syn_dataspec.prototype() == sp.Dataset:
            raise TypeError("A Dataset cannot be a sklearn.decomposition.PCA.")
        else:
            scalar = cast(st.Scalar, syn_dataspec)
            return cast(ensemble.RandomForestClassifier, scalar.value())


class RandomForestRegressor(DataSpecWrapper):
    def __init__(
        self,
        n_estimators=100,
        *,
        criterion="squared_error",
        max_depth=None,
        min_samples_split=2,
        min_samples_leaf=1,
        min_weight_fraction_leaf=0.0,
        max_features=1.0,
        max_leaf_nodes=None,
        min_impurity_decrease=0.0,
        bootstrap=False,
        oob_score=False,
        n_jobs=None,
        random_state=None,
        verbose=0,
        warm_start=False,
        ccp_alpha=0.0,
        max_samples=None,
        _dataspec=None,
    ):
        if _dataspec is None:
            _dataspec = model(
                model_class=sp.Scalar.Model.ModelClass.SK_RANDOM_FOREST_REGRESSOR,
                n_estimators=n_estimators,
                criterion=criterion,
                max_depth=max_depth,
                min_samples_split=min_samples_split,
                min_samples_leaf=min_samples_leaf,
                min_weight_fraction_leaf=min_weight_fraction_leaf,
                max_features=max_features,
                max_leaf_nodes=max_leaf_nodes,
                min_impurity_decrease=min_impurity_decrease,
                bootstrap=bootstrap,
                oob_score=oob_score,
                n_jobs=n_jobs,
                random_state=random_state,
                verbose=verbose,
                warm_start=warm_start,
                ccp_alpha=ccp_alpha,
                max_samples=max_samples,
            )
            variant_constraint(st.ConstraintKind.PUBLIC, _dataspec)

        super().__init__(dataspec=_dataspec)

    def fit(self, X, y=None):
        all_dataspec = True
        if not isinstance(X, DataSpecWrapper):
            print("`X` is not a Sarus object, fitting on synthetic data.")
            all_dataspec = False

        if all_dataspec:
            new_scalar = external(
                sp.Transform.ExternalOp.SK_RANDOM_FOREST_REGRESSOR
            )(
                self._dataspec,
                X._dataspec,
                y._dataspec,
            )
            return RandomForestRegressor(_dataspec=new_scalar)
        else:
            model_value = self.value()
            model_value.fit(X, y)
            return model_value

    def value(self) -> ensemble.RandomForestRegressor:
        """Return value of synthetic variant."""
        syn_dataspec = self.dataspec(kind=DataSpecVariant.ALTERNATIVE)
        if syn_dataspec.prototype() == sp.Dataset:
            raise TypeError("A Dataset cannot be a sklearn.decomposition.PCA.")
        else:
            scalar = cast(st.Scalar, syn_dataspec)
            return cast(ensemble.RandomForestRegressor, scalar.value())


class RandomTreesEmbedding(DataSpecWrapper):
    def __init__(
        self,
        n_estimators=100,
        *,
        max_depth=5,
        min_samples_split=2,
        min_samples_leaf=1,
        min_weight_fraction_leaf=0.0,
        max_leaf_nodes=None,
        min_impurity_decrease=0.0,
        sparse_output=True,
        n_jobs=None,
        random_state=None,
        verbose=0,
        warm_start=False,
        _dataspec=None,
    ):
        if _dataspec is None:
            _dataspec = model(
                model_class=sp.Scalar.Model.ModelClass.SK_RANDOM_TREES_EMBEDDING,
                n_estimators=n_estimators,
                max_depth=max_depth,
                min_samples_split=min_samples_split,
                min_samples_leaf=min_samples_leaf,
                min_weight_fraction_leaf=min_weight_fraction_leaf,
                max_leaf_nodes=max_leaf_nodes,
                min_impurity_decrease=min_impurity_decrease,
                sparse_output=sparse_output,
                n_jobs=n_jobs,
                random_state=random_state,
                verbose=verbose,
                warm_start=warm_start,
            )
            variant_constraint(st.ConstraintKind.PUBLIC, _dataspec)

        super().__init__(dataspec=_dataspec)

    def fit(self, X, y=None):
        all_dataspec = True
        if not isinstance(X, DataSpecWrapper):
            print("`X` is not a Sarus object, fitting on synthetic data.")
            all_dataspec = False

        if all_dataspec:
            new_scalar = external(
                sp.Transform.ExternalOp.SK_RANDOM_TREES_EMBEDDING
            )(
                self._dataspec,
                X._dataspec,
                y._dataspec,
            )
            return RandomTreesEmbedding(_dataspec=new_scalar)
        else:
            model_value = self.value()
            model_value.fit(X, y)
            return model_value

    def value(self) -> ensemble.RandomTreesEmbedding:
        """Return value of synthetic variant."""
        syn_dataspec = self.dataspec(kind=DataSpecVariant.ALTERNATIVE)
        if syn_dataspec.prototype() == sp.Dataset:
            raise TypeError("A Dataset cannot be a sklearn.decomposition.PCA.")
        else:
            scalar = cast(st.Scalar, syn_dataspec)
            return cast(ensemble.RandomTreesEmbedding, scalar.value())


class StackingClassifier(DataSpecWrapper):
    def __init__(
        self,
        estimators,
        final_estimator=None,
        *,
        cv=None,
        stack_method="auto",
        n_jobs=None,
        passthrough=False,
        verbose=0,
        _dataspec=None,
    ):
        if _dataspec is None:
            _dataspec = model(
                model_class=sp.Scalar.Model.ModelClass.SK_STACKING_CLASSIFIER,
                estimators=estimators,
                final_estimator=final_estimator,
                cv=cv,
                stack_method=stack_method,
                n_jobs=n_jobs,
                passthrough=passthrough,
                verbose=verbose,
            )
            variant_constraint(st.ConstraintKind.PUBLIC, _dataspec)

        super().__init__(dataspec=_dataspec)

    def fit(self, X, y=None):
        all_dataspec = True
        if not isinstance(X, DataSpecWrapper):
            print("`X` is not a Sarus object, fitting on synthetic data.")
            all_dataspec = False

        if all_dataspec:
            new_scalar = external(
                sp.Transform.ExternalOp.SK_STACKING_CLASSIFIER
            )(
                self._dataspec,
                X._dataspec,
                y._dataspec,
            )
            return StackingClassifier(_dataspec=new_scalar)
        else:
            model_value = self.value()
            model_value.fit(X, y)
            return model_value

    def value(self) -> ensemble.StackingClassifier:
        """Return value of synthetic variant."""
        syn_dataspec = self.dataspec(kind=DataSpecVariant.ALTERNATIVE)
        if syn_dataspec.prototype() == sp.Dataset:
            raise TypeError("A Dataset cannot be a sklearn.decomposition.PCA.")
        else:
            scalar = cast(st.Scalar, syn_dataspec)
            return cast(ensemble.StackingClassifier, scalar.value())


class StackingRegressor(DataSpecWrapper):
    def __init__(
        self,
        estimators,
        final_estimator=None,
        *,
        cv=None,
        stack_method="auto",
        n_jobs=None,
        passthrough=False,
        verbose=0,
        _dataspec=None,
    ):
        if _dataspec is None:
            _dataspec = model(
                model_class=sp.Scalar.Model.ModelClass.SK_STACKING_REGRESSOR,
                estimators=estimators,
                final_estimator=final_estimator,
                cv=cv,
                stack_method=stack_method,
                n_jobs=n_jobs,
                passthrough=passthrough,
                verbose=verbose,
            )
            variant_constraint(st.ConstraintKind.PUBLIC, _dataspec)

        super().__init__(dataspec=_dataspec)

    def fit(self, X, y=None):
        all_dataspec = True
        if not isinstance(X, DataSpecWrapper):
            print("`X` is not a Sarus object, fitting on synthetic data.")
            all_dataspec = False

        if all_dataspec:
            new_scalar = external(
                sp.Transform.ExternalOp.SK_STACKING_REGRESSOR
            )(
                self._dataspec,
                X._dataspec,
                y._dataspec,
            )
            return StackingRegressor(_dataspec=new_scalar)
        else:
            model_value = self.value()
            model_value.fit(X, y)
            return model_value

    def value(self) -> ensemble.StackingRegressor:
        """Return value of synthetic variant."""
        syn_dataspec = self.dataspec(kind=DataSpecVariant.ALTERNATIVE)
        if syn_dataspec.prototype() == sp.Dataset:
            raise TypeError("A Dataset cannot be a sklearn.decomposition.PCA.")
        else:
            scalar = cast(st.Scalar, syn_dataspec)
            return cast(ensemble.StackingRegressor, scalar.value())


class VotingClassifier(DataSpecWrapper):
    def __init__(
        self,
        estimators,
        *,
        voting="hard",
        weights=None,
        n_jobs=None,
        flatten_transform=True,
        verbose=False,
        _dataspec=None,
    ):
        if _dataspec is None:
            _dataspec = model(
                model_class=sp.Scalar.Model.ModelClass.SK_VOTING_CLASSIFIER,
                estimators=estimators,
                voting=voting,
                weights=weights,
                n_jobs=n_jobs,
                flatten_transform=flatten_transform,
                verbose=verbose,
            )
            variant_constraint(st.ConstraintKind.PUBLIC, _dataspec)

        super().__init__(dataspec=_dataspec)

    def fit(self, X, y=None):
        all_dataspec = True
        if not isinstance(X, DataSpecWrapper):
            print("`X` is not a Sarus object, fitting on synthetic data.")
            all_dataspec = False

        if all_dataspec:
            new_scalar = external(
                sp.Transform.ExternalOp.SK_VOTING_CLASSIFIER
            )(
                self._dataspec,
                X._dataspec,
                y._dataspec,
            )
            return VotingClassifier(_dataspec=new_scalar)
        else:
            model_value = self.value()
            model_value.fit(X, y)
            return model_value

    def value(self) -> ensemble.VotingClassifier:
        """Return value of synthetic variant."""
        syn_dataspec = self.dataspec(kind=DataSpecVariant.ALTERNATIVE)
        if syn_dataspec.prototype() == sp.Dataset:
            raise TypeError("A Dataset cannot be a sklearn.decomposition.PCA.")
        else:
            scalar = cast(st.Scalar, syn_dataspec)
            return cast(ensemble.VotingClassifier, scalar.value())


class VotingRegressor(DataSpecWrapper):
    def __init__(
        self,
        estimators,
        *,
        weights=None,
        n_jobs=None,
        verbose=False,
        _dataspec=None,
    ):
        if _dataspec is None:
            _dataspec = model(
                model_class=sp.Scalar.Model.ModelClass.SK_VOTING_REGRESSOR,
                estimators=estimators,
                weights=weights,
                n_jobs=n_jobs,
                verbose=verbose,
            )
            variant_constraint(st.ConstraintKind.PUBLIC, _dataspec)

        super().__init__(dataspec=_dataspec)

    def fit(self, X, y=None):
        all_dataspec = True
        if not isinstance(X, DataSpecWrapper):
            print("`X` is not a Sarus object, fitting on synthetic data.")
            all_dataspec = False

        if all_dataspec:
            new_scalar = external(sp.Transform.ExternalOp.SK_VOTING_REGRESSOR)(
                self._dataspec,
                X._dataspec,
                y._dataspec,
            )
            return VotingRegressor(_dataspec=new_scalar)
        else:
            model_value = self.value()
            model_value.fit(X, y)
            return model_value

    def value(self) -> ensemble.VotingRegressor:
        """Return value of synthetic variant."""
        syn_dataspec = self.dataspec(kind=DataSpecVariant.ALTERNATIVE)
        if syn_dataspec.prototype() == sp.Dataset:
            raise TypeError("A Dataset cannot be a sklearn.decomposition.PCA.")
        else:
            scalar = cast(st.Scalar, syn_dataspec)
            return cast(ensemble.VotingRegressor, scalar.value())


class HistGradientBoostingClassifier(DataSpecWrapper):
    def __init__(
        self,
        loss="log_loss",
        *,
        learning_rate=0.1,
        max_iter=100,
        max_leaf_nodes=31,
        max_depth=None,
        min_samples_leaf=20,
        l2_regularization=0.0,
        max_bins=255,
        categorical_features=None,
        monotonic_cst=None,
        warm_start=False,
        early_stopping="auto",
        scoring="loss",
        validation_fraction=0.1,
        n_iter_no_change=10,
        tol=1e-07,
        verbose=0,
        random_state=None,
        _dataspec=None,
    ):
        if _dataspec is None:
            _dataspec = model(
                model_class=sp.Scalar.Model.ModelClass.SK_HIST_GRADIENT_BOOSTING_CLASSIFIER,
                loss=loss,
                learning_rate=learning_rate,
                max_iter=max_iter,
                max_leaf_nodes=max_leaf_nodes,
                max_depth=max_depth,
                min_samples_leaf=min_samples_leaf,
                l2_regularization=0.0,
                max_bins=255,
                categorical_features=None,
                monotonic_cst=None,
                warm_start=False,
                early_stopping="auto",
                scoring="loss",
                validation_fraction=0.1,
                n_iter_no_change=10,
                tol=1e-07,
                verbose=0,
                random_state=None,
            )
            variant_constraint(st.ConstraintKind.PUBLIC, _dataspec)

        super().__init__(dataspec=_dataspec)

    def fit(self, X, y=None):
        all_dataspec = True
        if not isinstance(X, DataSpecWrapper):
            print("`X` is not a Sarus object, fitting on synthetic data.")
            all_dataspec = False

        if all_dataspec:
            new_scalar = external(
                sp.Transform.ExternalOp.SK_HIST_GRADIENT_BOOSTING_CLASSIFIER
            )(
                self._dataspec,
                X._dataspec,
                y._dataspec,
            )
            return HistGradientBoostingClassifier(_dataspec=new_scalar)
        else:
            model_value = self.value()
            model_value.fit(X, y)
            return model_value

    def value(self) -> ensemble.HistGradientBoostingClassifier:
        """Return value of synthetic variant."""
        syn_dataspec = self.dataspec(kind=DataSpecVariant.ALTERNATIVE)
        if syn_dataspec.prototype() == sp.Dataset:
            raise TypeError("A Dataset cannot be a sklearn.decomposition.PCA.")
        else:
            scalar = cast(st.Scalar, syn_dataspec)
            return cast(
                ensemble.HistGradientBoostingClassifier, scalar.value()
            )


class HistGradientBoostingRegressor(DataSpecWrapper):
    def __init__(
        self,
        estimators,
        *,
        weights=None,
        n_jobs=None,
        verbose=False,
        _dataspec=None,
    ):
        if _dataspec is None:
            _dataspec = model(
                model_class=sp.Scalar.Model.ModelClass.SK_HIST_GRADIENT_BOOSTING_REGRESSOR,
                estimators=estimators,
                weights=weights,
                n_jobs=n_jobs,
                verbose=verbose,
            )
            variant_constraint(st.ConstraintKind.PUBLIC, _dataspec)

        super().__init__(dataspec=_dataspec)

    def fit(self, X, y=None):
        all_dataspec = True
        if not isinstance(X, DataSpecWrapper):
            print("`X` is not a Sarus object, fitting on synthetic data.")
            all_dataspec = False

        if all_dataspec:
            new_scalar = external(
                sp.Transform.ExternalOp.SK_HIST_GRADIENT_BOOSTING_REGRESSOR
            )(
                self._dataspec,
                X._dataspec,
                y._dataspec,
            )
            return HistGradientBoostingRegressor(_dataspec=new_scalar)
        else:
            model_value = self.value()
            model_value.fit(X, y)
            return model_value

    def value(self) -> ensemble.HistGradientBoostingRegressor:
        """Return value of synthetic variant."""
        syn_dataspec = self.dataspec(kind=DataSpecVariant.ALTERNATIVE)
        if syn_dataspec.prototype() == sp.Dataset:
            raise TypeError("A Dataset cannot be a sklearn.decomposition.PCA.")
        else:
            scalar = cast(st.Scalar, syn_dataspec)
            return cast(ensemble.HistGradientBoostingRegressor, scalar.value())
