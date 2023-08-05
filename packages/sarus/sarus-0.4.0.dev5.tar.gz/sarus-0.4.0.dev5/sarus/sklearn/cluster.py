from __future__ import annotations

from typing import cast

import numpy as np
import sarus_data_spec.protobuf as sp
import sarus_data_spec.typing as st
from sarus_data_spec.scalar import model
from sarus_data_spec.transform import external
from sarus_data_spec.variant_constraint import variant_constraint

from sarus.dataspec_wrapper import DataSpecWrapper
from sarus.typing import DataSpecVariant

try:
    import sklearn.cluster as cluster
except ModuleNotFoundError:
    pass  # error message in sarus_data_spec.typing


class AffinityPropagation(DataSpecWrapper):
    def __init__(
        self,
        *,
        damping=0.5,
        max_iter=200,
        convergence_iter=15,
        copy=True,
        preference=None,
        affinity="euclidean",
        verbose=False,
        random_state="warn",
        _dataspec=None,
    ):
        if _dataspec is None:
            _dataspec = model(
                model_class=sp.Scalar.Model.ModelClass.SK_AFFINITY_PROPAGATION,
                damping=0.5,
                max_iter=max_iter,
                convergence_iter=convergence_iter,
                copy=copy,
                preference=preference,
                affinity=affinity,
                verbose=verbose,
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
                sp.Transform.ExternalOp.SK_AFFINITY_PROPAGATION
            )(
                self._dataspec,
                X._dataspec,
            )
            return AffinityPropagation(_dataspec=new_scalar)
        else:
            model_value = self.value()
            model_value.fit(X, y)
            return model_value

    def value(self) -> cluster.AffinityPropagation:
        """Return value of synthetic variant."""
        syn_dataspec = self.dataspec(kind=DataSpecVariant.ALTERNATIVE)
        if syn_dataspec.prototype() == sp.Dataset:
            raise TypeError("A Dataset cannot be a sklearn.decomposition.PCA.")
        else:
            scalar = cast(st.Scalar, syn_dataspec)
            return cast(cluster.AffinityPropagation, scalar.value())


class AgglomerativeClustering(DataSpecWrapper):
    def __init__(
        self,
        n_clusters=2,
        *,
        affinity="euclidean",
        memory=None,
        connectivity=None,
        compute_full_tree="auto",
        linkage="ward",
        distance_threshold=None,
        _dataspec=None,
    ):
        if _dataspec is None:
            _dataspec = model(
                model_class=sp.Scalar.Model.ModelClass.SK_AGGLOMERATIVE_CLUSTERING,
                n_clusters=n_clusters,
                affinity=affinity,
                memory=memory,
                connectivity=connectivity,
                compute_full_tree=compute_full_tree,
                linkage=linkage,
                distance_threshold=distance_threshold,
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
                sp.Transform.ExternalOp.SK_AGGLOMERATIVE_CLUSTERING
            )(
                self._dataspec,
                X._dataspec,
            )
            return AgglomerativeClustering(_dataspec=new_scalar)
        else:
            model_value = self.value()
            model_value.fit(X, y)
            return model_value

    def value(self) -> cluster.AgglomerativeClustering:
        """Return value of synthetic variant."""
        syn_dataspec = self.dataspec(kind=DataSpecVariant.ALTERNATIVE)
        if syn_dataspec.prototype() == sp.Dataset:
            raise TypeError("A Dataset cannot be a sklearn.decomposition.PCA.")
        else:
            scalar = cast(st.Scalar, syn_dataspec)
            return cast(cluster.AgglomerativeClustering, scalar.value())


class Birch(DataSpecWrapper):
    def __init__(
        self,
        *,
        threshold=0.5,
        branching_factor=50,
        n_clusters=3,
        compute_labels=True,
        copy=True,
        _dataspec=None,
    ):
        if _dataspec is None:
            _dataspec = model(
                model_class=sp.Scalar.Model.ModelClass.SK_BIRCH,
                threshold=threshold,
                branching_factor=branching_factor,
                n_clusters=n_clusters,
                compute_labels=compute_labels,
                copy=copy,
            )
            variant_constraint(st.ConstraintKind.PUBLIC, _dataspec)

        super().__init__(dataspec=_dataspec)

    def fit(self, X, y=None):
        all_dataspec = True
        if not isinstance(X, DataSpecWrapper):
            print("`X` is not a Sarus object, fitting on synthetic data.")
            all_dataspec = False

        if all_dataspec:
            new_scalar = external(sp.Transform.ExternalOp.SK_BIRCH)(
                self._dataspec,
                X._dataspec,
            )
            return Birch(_dataspec=new_scalar)
        else:
            model_value = self.value()
            model_value.fit(X, y)
            return model_value

    def value(self) -> cluster.Birch:
        """Return value of synthetic variant."""
        syn_dataspec = self.dataspec(kind=DataSpecVariant.ALTERNATIVE)
        if syn_dataspec.prototype() == sp.Dataset:
            raise TypeError("A Dataset cannot be a sklearn.decomposition.PCA.")
        else:
            scalar = cast(st.Scalar, syn_dataspec)
            return cast(cluster.Birch, scalar.value())


class DBSCAN(DataSpecWrapper):
    def __init__(
        self,
        eps=0.5,
        *,
        min_samples=5,
        metric="euclidean",
        metric_params=None,
        algorithm="auto",
        leaf_size=30,
        p=None,
        n_jobs=None,
        _dataspec=None,
    ):
        if _dataspec is None:
            _dataspec = model(
                model_class=sp.Scalar.Model.ModelClass.SK_DBSCAN,
                eps=eps,
                min_samples=min_samples,
                metric=metric,
                metric_params=metric_params,
                algorithm=algorithm,
                leaf_size=leaf_size,
                p=p,
                n_jobs=n_jobs,
            )
            variant_constraint(st.ConstraintKind.PUBLIC, _dataspec)

        super().__init__(dataspec=_dataspec)

    def fit(self, X, y=None):
        all_dataspec = True
        if not isinstance(X, DataSpecWrapper):
            print("`X` is not a Sarus object, fitting on synthetic data.")
            all_dataspec = False

        if all_dataspec:
            new_scalar = external(sp.Transform.ExternalOp.SK_DBSCAN)(
                self._dataspec,
                X._dataspec,
            )
            return DBSCAN(_dataspec=new_scalar)
        else:
            model_value = self.value()
            model_value.fit(X, y)
            return model_value

    def value(self) -> cluster.DBSCAN:
        """Return value of synthetic variant."""
        syn_dataspec = self.dataspec(kind=DataSpecVariant.ALTERNATIVE)
        if syn_dataspec.prototype() == sp.Dataset:
            raise TypeError("A Dataset cannot be a sklearn.decomposition.PCA.")
        else:
            scalar = cast(st.Scalar, syn_dataspec)
            return cast(cluster.DBSCAN, scalar.value())


class FeatureAgglomeration(DataSpecWrapper):
    def __init__(
        self,
        n_clusters=2,
        *,
        affinity="euclidean",
        memory=None,
        connectivity=None,
        compute_full_tree="auto",
        linkage="ward",
        ooling_func=np.mean,
        distance_threshold=None,
        _dataspec=None,
    ):
        if _dataspec is None:
            _dataspec = model(
                model_class=sp.Scalar.Model.ModelClass.SK_AFFINITY_PROPAGATION,
                n_clusters=n_clusters,
                affinity=affinity,
                memory=memory,
                connectivity=Noconnectivityne,
                compute_full_tree=compute_full_tree,
                linkage=linkage,
                ooling_func=ooling_func,
                distance_threshold=distance_threshold,
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
                sp.Transform.ExternalOp.SK_FEATURE_AGGLOMERATION
            )(
                self._dataspec,
                X._dataspec,
            )
            return FeatureAgglomeration(_dataspec=new_scalar)
        else:
            model_value = self.value()
            model_value.fit(X, y)
            return model_value

    def value(self) -> cluster.FeatureAgglomeration:
        """Return value of synthetic variant."""
        syn_dataspec = self.dataspec(kind=DataSpecVariant.ALTERNATIVE)
        if syn_dataspec.prototype() == sp.Dataset:
            raise TypeError("A Dataset cannot be a sklearn.decomposition.PCA.")
        else:
            scalar = cast(st.Scalar, syn_dataspec)
            return cast(cluster.FeatureAgglomeration, scalar.value())


class KMeans(DataSpecWrapper):
    def __init__(
        self,
        n_clusters=8,
        *,
        init="k-means++",
        n_init=10,
        max_iter=300,
        tol=0.0001,
        precompute_distances="deprecated",
        verbose=0,
        random_state=None,
        copy_x=True,
        n_jobs="deprecated",
        algorithm="auto",
        _dataspec=None,
    ):
        if _dataspec is None:
            _dataspec = model(
                model_class=sp.Scalar.Model.ModelClass.SK_AFFINITY_PROPAGATION,
                n_clusters=n_clusters,
                init=init,
                n_init=n_init,
                max_iter=max_iter,
                tol=tol,
                precompute_distances=precompute_distances,
                verbose=verbose,
                random_state=random_state,
                copy_x=copy_x,
                n_jobs=n_jobs,
                algorithm=algorithm,
            )
            variant_constraint(st.ConstraintKind.PUBLIC, _dataspec)

        super().__init__(dataspec=_dataspec)

    def fit(self, X, y=None):
        all_dataspec = True
        if not isinstance(X, DataSpecWrapper):
            print("`X` is not a Sarus object, fitting on synthetic data.")
            all_dataspec = False

        if all_dataspec:
            new_scalar = external(sp.Transform.ExternalOp.SK_KMEANS)(
                self._dataspec,
                X._dataspec,
            )
            return KMeans(_dataspec=new_scalar)
        else:
            model_value = self.value()
            model_value.fit(X, y)
            return model_value

    def value(self) -> cluster.KMeans:
        """Return value of synthetic variant."""
        syn_dataspec = self.dataspec(kind=DataSpecVariant.ALTERNATIVE)
        if syn_dataspec.prototype() == sp.Dataset:
            raise TypeError("A Dataset cannot be a sklearn.decomposition.PCA.")
        else:
            scalar = cast(st.Scalar, syn_dataspec)
            return cast(cluster.KMeans, scalar.value())


class MiniBatchKMeans(DataSpecWrapper):
    def __init__(
        self,
        n_clusters=8,
        *,
        init="k-means++",
        max_iter=100,
        batch_size=100,
        verbose=0,
        compute_labels=True,
        random_state=None,
        tol=0.0,
        max_no_improvement=10,
        init_size=None,
        n_init=3,
        reassignment_ratio=0.01,
        _dataspec=None,
    ):
        if _dataspec is None:
            _dataspec = model(
                model_class=sp.Scalar.Model.ModelClass.SK_MINIBATCH_KMEANS,
                n_clusters=n_clusters,
                init=init,
                max_iter=max_iter,
                batch_size=batch_size,
                verbose=verbose,
                compute_labels=compute_labels,
                random_state=random_state,
                tol=tol,
                max_no_improvement=max_no_improvement,
                init_size=init_size,
                n_init=n_init,
                reassignment_ratio=reassignment_ratio,
            )
            variant_constraint(st.ConstraintKind.PUBLIC, _dataspec)

        super().__init__(dataspec=_dataspec)

    def fit(self, X, y=None):
        all_dataspec = True
        if not isinstance(X, DataSpecWrapper):
            print("`X` is not a Sarus object, fitting on synthetic data.")
            all_dataspec = False

        if all_dataspec:
            new_scalar = external(sp.Transform.ExternalOp.SK_MINIBATCH_KMEANS)(
                self._dataspec,
                X._dataspec,
            )
            return MiniBatchKMeans(_dataspec=new_scalar)
        else:
            model_value = self.value()
            model_value.fit(X, y)
            return model_value

    def value(self) -> cluster.MiniBatchKMeans:
        """Return value of synthetic variant."""
        syn_dataspec = self.dataspec(kind=DataSpecVariant.ALTERNATIVE)
        if syn_dataspec.prototype() == sp.Dataset:
            raise TypeError("A Dataset cannot be a sklearn.decomposition.PCA.")
        else:
            scalar = cast(st.Scalar, syn_dataspec)
            return cast(cluster.MiniBatchKMeans, scalar.value())


class MeanShift(DataSpecWrapper):
    def __init__(
        self,
        *,
        bandwidth=None,
        seeds=None,
        bin_seeding=False,
        min_bin_freq=1,
        cluster_all=True,
        n_jobs=None,
        max_iter=300,
        _dataspec=None,
    ):
        if _dataspec is None:
            _dataspec = model(
                model_class=sp.Scalar.Model.ModelClass.SK_MEAN_SHIFT,
                bandwidth=bandwidth,
                seeds=seeds,
                bin_seeding=bin_seeding,
                min_bin_freq=min_bin_freq,
                cluster_all=cluster_all,
                n_jobs=n_jobs,
                max_iter=max_iter,
            )
            variant_constraint(st.ConstraintKind.PUBLIC, _dataspec)

        super().__init__(dataspec=_dataspec)

    def fit(self, X, y=None):
        all_dataspec = True
        if not isinstance(X, DataSpecWrapper):
            print("`X` is not a Sarus object, fitting on synthetic data.")
            all_dataspec = False

        if all_dataspec:
            new_scalar = external(sp.Transform.ExternalOp.SK_MEAN_SHIFT)(
                self._dataspec,
                X._dataspec,
            )
            return MeanShift(_dataspec=new_scalar)
        else:
            model_value = self.value()
            model_value.fit(X, y)
            return model_value

    def value(self) -> cluster.MeanShift:
        """Return value of synthetic variant."""
        syn_dataspec = self.dataspec(kind=DataSpecVariant.ALTERNATIVE)
        if syn_dataspec.prototype() == sp.Dataset:
            raise TypeError("A Dataset cannot be a sklearn.decomposition.PCA.")
        else:
            scalar = cast(st.Scalar, syn_dataspec)
            return cast(cluster.MeanShift, scalar.value())


class OPTICS(DataSpecWrapper):
    def __init__(
        self,
        *,
        min_samples=5,
        max_eps=np.inf,
        metric="minkowski",
        p=2,
        metric_params=None,
        cluster_method="xi",
        eps=None,
        xi=0.05,
        predecessor_correction=True,
        min_cluster_size=None,
        algorithm="auto",
        leaf_size=30,
        n_jobs=None,
        _dataspec=None,
    ):
        if _dataspec is None:
            _dataspec = model(
                model_class=sp.Scalar.Model.ModelClass.SK_OPTICS,
                min_samples=min_samples,
                max_eps=max_eps,
                metric=metric,
                p=p,
                metric_params=metric_params,
                cluster_method=cluster_method,
                eps=eps,
                xi=xi,
                predecessor_correction=predecessor_correction,
                min_cluster_size=min_cluster_size,
                algorithm=algorithm,
                leaf_size=leaf_size,
                n_jobs=n_jobs,
            )
            variant_constraint(st.ConstraintKind.PUBLIC, _dataspec)

        super().__init__(dataspec=_dataspec)

    def fit(self, X, y=None):
        all_dataspec = True
        if not isinstance(X, DataSpecWrapper):
            print("`X` is not a Sarus object, fitting on synthetic data.")
            all_dataspec = False

        if all_dataspec:
            new_scalar = external(sp.Transform.ExternalOp.SK_OPTICS)(
                self._dataspec,
                X._dataspec,
            )
            return OPTICS(_dataspec=new_scalar)
        else:
            model_value = self.value()
            model_value.fit(X, y)
            return model_value

    def value(self) -> cluster.OPTICS:
        """Return value of synthetic variant."""
        syn_dataspec = self.dataspec(kind=DataSpecVariant.ALTERNATIVE)
        if syn_dataspec.prototype() == sp.Dataset:
            raise TypeError("A Dataset cannot be a sklearn.decomposition.PCA.")
        else:
            scalar = cast(st.Scalar, syn_dataspec)
            return cast(cluster.OPTICS, scalar.value())


class SpectralClustering(DataSpecWrapper):
    def __init__(
        self,
        n_clusters=8,
        *,
        eigen_solver=None,
        n_components=None,
        random_state=None,
        n_init=10,
        gamma=1.0,
        affinity="rbf",
        n_neighbors=10,
        eigen_tol=0.0,
        assign_labels="kmeans",
        degree=3,
        coef0=1,
        kernel_params=None,
        n_jobs=None,
        _dataspec=None,
    ):
        if _dataspec is None:
            _dataspec = model(
                model_class=sp.Scalar.Model.ModelClass.SK_SPECTRAL_CLUSTERING,
                n_clusters=n_clusters,
                eigen_solver=eigen_solver,
                n_components=n_components,
                random_state=random_state,
                n_init=n_init,
                gamma=gamma,
                affinity=affinity,
                n_neighbors=n_neighbors,
                eigen_tol=eigen_tol,
                assign_labels=assign_labels,
                degree=degree,
                coef0=coef0,
                kernel_params=kernel_params,
                n_jobs=n_jobs,
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
                sp.Transform.ExternalOp.SK_SPECTRAL_CLUSTERING
            )(
                self._dataspec,
                X._dataspec,
            )
            return SpectralClustering(_dataspec=new_scalar)
        else:
            model_value = self.value()
            model_value.fit(X, y)
            return model_value

    def value(self) -> cluster.SpectralClustering:
        """Return value of synthetic variant."""
        syn_dataspec = self.dataspec(kind=DataSpecVariant.ALTERNATIVE)
        if syn_dataspec.prototype() == sp.Dataset:
            raise TypeError("A Dataset cannot be a sklearn.decomposition.PCA.")
        else:
            scalar = cast(st.Scalar, syn_dataspec)
            return cast(cluster.SpectralClustering, scalar.value())


class SpectralBiclustering(DataSpecWrapper):
    def __init__(
        self,
        n_clusters=3,
        *,
        method="bistochastic",
        n_components=6,
        n_best=3,
        svd_method="randomized",
        n_svd_vecs=None,
        mini_batch=False,
        init="k-means++",
        n_init=10,
        n_jobs="deprecated",
        random_state=None,
        _dataspec=None,
    ):
        if _dataspec is None:
            _dataspec = model(
                model_class=sp.Scalar.Model.ModelClass.SK_SPECTRAL_BICLUSTERING,
                n_clusters=n_clusters,
                method=method,
                n_components=n_components,
                n_best=n_best,
                svd_method=svd_method,
                n_svd_vecs=n_svd_vecs,
                mini_batch=mini_batch,
                init=init,
                n_init=n_init,
                n_jobs=n_jobs,
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
                sp.Transform.ExternalOp.SK_SPECTRAL_BICLUSTERING
            )(
                self._dataspec,
                X._dataspec,
            )
            return SpectralBiclustering(_dataspec=new_scalar)
        else:
            model_value = self.value()
            model_value.fit(X, y)
            return model_value

    def value(self) -> cluster.SpectralBiclustering:
        """Return value of synthetic variant."""
        syn_dataspec = self.dataspec(kind=DataSpecVariant.ALTERNATIVE)
        if syn_dataspec.prototype() == sp.Dataset:
            raise TypeError("A Dataset cannot be a sklearn.decomposition.PCA.")
        else:
            scalar = cast(st.Scalar, syn_dataspec)
            return cast(cluster.SpectralBiclustering, scalar.value())


class SpectralCoclustering(DataSpecWrapper):
    def __init__(
        self,
        n_clusters=3,
        *,
        svd_method="randomized",
        n_svd_vecs=None,
        mini_batch=False,
        init="k-means++",
        n_init=10,
        n_jobs="deprecated",
        random_state=None,
        _dataspec=None,
    ):
        if _dataspec is None:
            _dataspec = model(
                model_class=sp.Scalar.Model.ModelClass.SK_AFFINITY_PROPAGATION,
                n_clusters=n_clusters,
                svd_method=svd_method,
                n_svd_vecs=n_svd_vecs,
                mini_batch=mini_batch,
                init=init,
                n_init=n_init,
                n_jobs=n_jobs,
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
                sp.Transform.ExternalOp.SK_SPECTRAL_COCLUSTERING
            )(
                self._dataspec,
                X._dataspec,
            )
            return SpectralCoclustering(_dataspec=new_scalar)
        else:
            model_value = self.value()
            model_value.fit(X, y)
            return model_value

    def value(self) -> cluster.SpectralCoclustering:
        """Return value of synthetic variant."""
        syn_dataspec = self.dataspec(kind=DataSpecVariant.ALTERNATIVE)
        if syn_dataspec.prototype() == sp.Dataset:
            raise TypeError("A Dataset cannot be a sklearn.decomposition.PCA.")
        else:
            scalar = cast(st.Scalar, syn_dataspec)
            return cast(cluster.SpectralCoclustering, scalar.value())
