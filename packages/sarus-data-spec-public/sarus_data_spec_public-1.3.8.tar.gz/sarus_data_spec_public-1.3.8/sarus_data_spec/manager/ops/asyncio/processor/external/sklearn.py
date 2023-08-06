from __future__ import annotations

from typing import Any, cast

try:
    from sklearn import (
        cluster,
        decomposition,
        ensemble,
        metrics,
        model_selection,
        preprocessing,
        svm,
    )
except ModuleNotFoundError:
    pass  # error message in typing.py

import sarus_data_spec.typing as st

from .utils import one_parent_ops, pandas_or_value


async def sk_fit(  # to be renamed ?
    scalar: st.Scalar, *args: Any, **kwargs: Any
) -> svm.SVC:
    (ds_model, X, y), _ = scalar.parents()
    model = await cast(st.Scalar, ds_model).async_value()
    assert isinstance(model, svm.SVC)
    X = await pandas_or_value(X)
    y = await pandas_or_value(y)
    fitted_model = model.fit(X, y, *args, **kwargs)
    return fitted_model


@one_parent_ops
async def sk_scale(val: Any, *args: Any, **kwargs: Any) -> Any:
    return preprocessing.scale(val, *args, **kwargs)


async def sk_onehot(
    scalar: st.Scalar, *args: Any, **kwargs: Any
) -> preprocessing.OneHotEncoder:
    (ds_model, X), _ = scalar.parents()
    model = await cast(st.Scalar, ds_model).async_value()
    assert isinstance(model, preprocessing.OneHotEncoder)
    X = await pandas_or_value(X)
    fitted_model = model.fit(X, *args, **kwargs)
    return fitted_model


async def sk_pca(
    scalar: st.Scalar, *args: Any, **kwargs: Any
) -> decomposition.PCA:
    (ds_model, X), _ = scalar.parents()
    model = await cast(st.Scalar, ds_model).async_value()
    assert isinstance(model, decomposition.PCA)
    X = await pandas_or_value(X)
    fitted_model = model.fit(X, *args, **kwargs)
    return fitted_model


# cluster
async def sk_affinity_propagation(
    scalar: st.Scalar, *args: Any, **kwargs: Any
) -> cluster.AffinityPropagation:
    (ds_model, X), _ = scalar.parents()
    model = await cast(st.Scalar, ds_model).async_value()
    assert isinstance(model, cluster.AffinityPropagation)
    X = await pandas_or_value(X)
    fitted_model = model.fit(X, *args, **kwargs)
    return fitted_model


async def sk_agglomerative_clustering(
    scalar: st.Scalar, *args: Any, **kwargs: Any
) -> cluster.AgglomerativeClustering:
    (ds_model, X), _ = scalar.parents()
    model = await cast(st.Scalar, ds_model).async_value()
    assert isinstance(model, cluster.AgglomerativeClustering)
    X = await pandas_or_value(X)
    fitted_model = model.fit(X, *args, **kwargs)
    return fitted_model


async def sk_birch(
    scalar: st.Scalar, *args: Any, **kwargs: Any
) -> cluster.Birch:
    (ds_model, X), _ = scalar.parents()
    model = await cast(st.Scalar, ds_model).async_value()
    assert isinstance(model, cluster.Birch)
    X = await pandas_or_value(X)
    fitted_model = model.fit(X, *args, **kwargs)
    return fitted_model


async def sk_dbscan(
    scalar: st.Scalar, *args: Any, **kwargs: Any
) -> cluster.DBSCAN:
    (ds_model, X), _ = scalar.parents()
    model = await cast(st.Scalar, ds_model).async_value()
    assert isinstance(model, cluster.DBSCAN)
    X = await pandas_or_value(X)
    fitted_model = model.fit(X, *args, **kwargs)
    return fitted_model


async def sk_feature_agglomeration(
    scalar: st.Scalar, *args: Any, **kwargs: Any
) -> cluster.FeatureAgglomeration:
    (ds_model, X), _ = scalar.parents()
    model = await cast(st.Scalar, ds_model).async_value()
    assert isinstance(model, cluster.FeatureAgglomeration)
    X = await pandas_or_value(X)
    fitted_model = model.fit(X, *args, **kwargs)
    return fitted_model


async def sk_kmeans(
    scalar: st.Scalar, *args: Any, **kwargs: Any
) -> cluster.KMeans:
    (ds_model, X), _ = scalar.parents()
    model = await cast(st.Scalar, ds_model).async_value()
    assert isinstance(model, cluster.KMeans)
    X = await pandas_or_value(X)
    fitted_model = model.fit(X, *args, **kwargs)
    return fitted_model


async def sk_minibatch_kmeans(
    scalar: st.Scalar, *args: Any, **kwargs: Any
) -> cluster.MiniBatchKMeans:
    (ds_model, X), _ = scalar.parents()
    model = await cast(st.Scalar, ds_model).async_value()
    assert isinstance(model, cluster.MiniBatchKMeans)
    X = await pandas_or_value(X)
    fitted_model = model.fit(X, *args, **kwargs)
    return fitted_model


async def sk_mean_shift(
    scalar: st.Scalar, *args: Any, **kwargs: Any
) -> cluster.MeanShift:
    (ds_model, X), _ = scalar.parents()
    model = await cast(st.Scalar, ds_model).async_value()
    assert isinstance(model, cluster.MeanShift)
    X = await pandas_or_value(X)
    fitted_model = model.fit(X, *args, **kwargs)
    return fitted_model


async def sk_optics(
    scalar: st.Scalar, *args: Any, **kwargs: Any
) -> cluster.OPTICS:
    (ds_model, X), _ = scalar.parents()
    model = await cast(st.Scalar, ds_model).async_value()
    assert isinstance(model, cluster.OPTICS)
    X = await pandas_or_value(X)
    fitted_model = model.fit(X, *args, **kwargs)
    return fitted_model


async def sk_spectral_clustering(
    scalar: st.Scalar, *args: Any, **kwargs: Any
) -> cluster.SpectralClustering:
    (ds_model, X), _ = scalar.parents()
    model = await cast(st.Scalar, ds_model).async_value()
    assert isinstance(model, cluster.SpectralClustering)
    X = await pandas_or_value(X)
    fitted_model = model.fit(X, *args, **kwargs)
    return fitted_model


async def sk_spectral_biclustering(
    scalar: st.Scalar, *args: Any, **kwargs: Any
) -> cluster.SpectralBiclustering:
    (ds_model, X), _ = scalar.parents()
    model = await cast(st.Scalar, ds_model).async_value()
    assert isinstance(model, cluster.SpectralBiclustering)
    X = await pandas_or_value(X)
    fitted_model = model.fit(X, *args, **kwargs)
    return fitted_model


async def sk_spectral_coclustering(
    scalar: st.Scalar, *args: Any, **kwargs: Any
) -> cluster.SpectralCoclustering:
    (ds_model, X), _ = scalar.parents()
    model = await cast(st.Scalar, ds_model).async_value()
    assert isinstance(model, cluster.SpectralCoclustering)
    X = await pandas_or_value(X)
    fitted_model = model.fit(X, *args, **kwargs)
    return fitted_model


# ensemble
async def sk_adaboost_classifier(
    scalar: st.Scalar, *args: Any, **kwargs: Any
) -> ensemble.AdaBoostClassifier:
    (ds_model, X, y), _ = scalar.parents()
    model = await cast(st.Scalar, ds_model).async_value()
    assert isinstance(model, ensemble.AdaBoostClassifier)
    X = await pandas_or_value(X)
    y = await pandas_or_value(y)
    fitted_model = model.fit(X, y, *args, **kwargs)
    return fitted_model


async def sk_adaboost_regressor(
    scalar: st.Scalar, *args: Any, **kwargs: Any
) -> ensemble.AdaBoostRegressor:
    (ds_model, X, y), _ = scalar.parents()
    model = await cast(st.Scalar, ds_model).async_value()
    assert isinstance(model, ensemble.AdaBoostRegressor)
    X = await pandas_or_value(X)
    y = await pandas_or_value(y)
    fitted_model = model.fit(X, y, *args, **kwargs)
    return fitted_model


async def sk_bagging_classifier(
    scalar: st.Scalar, *args: Any, **kwargs: Any
) -> ensemble.BaggingClassifier:
    (ds_model, X, y), _ = scalar.parents()
    model = await cast(st.Scalar, ds_model).async_value()
    assert isinstance(model, ensemble.BaggingClassifier)
    X = await pandas_or_value(X)
    y = await pandas_or_value(y)
    fitted_model = model.fit(X, y, *args, **kwargs)
    return fitted_model


async def sk_bagging_regressor(
    scalar: st.Scalar, *args: Any, **kwargs: Any
) -> ensemble.BaggingRegressor:
    (ds_model, X, y), _ = scalar.parents()
    model = await cast(st.Scalar, ds_model).async_value()
    assert isinstance(model, ensemble.BaggingRegressor)
    X = await pandas_or_value(X)
    y = await pandas_or_value(y)
    fitted_model = model.fit(X, y, *args, **kwargs)
    return fitted_model


async def sk_extra_trees_classifier(
    scalar: st.Scalar, *args: Any, **kwargs: Any
) -> ensemble.ExtraTreesClassifier:
    (ds_model, X, y), _ = scalar.parents()
    model = await cast(st.Scalar, ds_model).async_value()
    assert isinstance(model, ensemble.ExtraTreesClassifier)
    X = await pandas_or_value(X)
    y = await pandas_or_value(y)
    fitted_model = model.fit(X, y, *args, **kwargs)
    return fitted_model


async def sk_extra_trees_regressor(
    scalar: st.Scalar, *args: Any, **kwargs: Any
) -> ensemble.ExtraTreesRegressor:
    (ds_model, X, y), _ = scalar.parents()
    model = await cast(st.Scalar, ds_model).async_value()
    assert isinstance(model, ensemble.ExtraTreesRegressor)
    X = await pandas_or_value(X)
    y = await pandas_or_value(y)
    fitted_model = model.fit(X, y, *args, **kwargs)
    return fitted_model


async def sk_gradient_boosting_classifier(
    scalar: st.Scalar, *args: Any, **kwargs: Any
) -> ensemble.GradientBoostingClassifier:
    (ds_model, X, y), _ = scalar.parents()
    model = await cast(st.Scalar, ds_model).async_value()
    assert isinstance(model, ensemble.GradientBoostingClassifier)
    X = await pandas_or_value(X)
    y = await pandas_or_value(y)
    fitted_model = model.fit(X, y, *args, **kwargs)
    return fitted_model


async def sk_gradient_boosting_regressor(
    scalar: st.Scalar, *args: Any, **kwargs: Any
) -> ensemble.GradientBoostingRegressor:
    (ds_model, X, y), _ = scalar.parents()
    model = await cast(st.Scalar, ds_model).async_value()
    assert isinstance(model, ensemble.GradientBoostingRegressor)
    X = await pandas_or_value(X)
    y = await pandas_or_value(y)
    fitted_model = model.fit(X, y, *args, **kwargs)
    return fitted_model


async def sk_isolation_forest(
    scalar: st.Scalar, *args: Any, **kwargs: Any
) -> ensemble.IsolationForest:
    (ds_model, X, y), _ = scalar.parents()
    model = await cast(st.Scalar, ds_model).async_value()
    assert isinstance(model, ensemble.IsolationForest)
    X = await pandas_or_value(X)
    y = await pandas_or_value(y)
    fitted_model = model.fit(X, y, *args, **kwargs)
    return fitted_model


async def sk_random_forest_classifier(
    scalar: st.Scalar, *args: Any, **kwargs: Any
) -> ensemble.RandomForestClassifier:
    (ds_model, X, y), _ = scalar.parents()
    model = await cast(st.Scalar, ds_model).async_value()
    assert isinstance(model, ensemble.RandomForestClassifier)
    X = await pandas_or_value(X)
    y = await pandas_or_value(y)
    fitted_model = model.fit(X, y, *args, **kwargs)
    return fitted_model


async def sk_random_forest_regressor(
    scalar: st.Scalar, *args: Any, **kwargs: Any
) -> ensemble.RandomForestRegressor:
    (ds_model, X, y), _ = scalar.parents()
    model = await cast(st.Scalar, ds_model).async_value()
    assert isinstance(model, ensemble.RandomForestRegressor)
    X = await pandas_or_value(X)
    y = await pandas_or_value(y)
    fitted_model = model.fit(X, y, *args, **kwargs)
    return fitted_model


async def sk_random_trees_embedding(
    scalar: st.Scalar, *args: Any, **kwargs: Any
) -> ensemble.RandomTreesEmbedding:
    (ds_model, X, y), _ = scalar.parents()
    model = await cast(st.Scalar, ds_model).async_value()
    assert isinstance(model, ensemble.RandomTreesEmbedding)
    X = await pandas_or_value(X)
    y = await pandas_or_value(y)
    fitted_model = model.fit(X, y, *args, **kwargs)
    return fitted_model


async def sk_stacking_classifier(
    scalar: st.Scalar, *args: Any, **kwargs: Any
) -> ensemble.StackingClassifier:
    (ds_model, X, y), _ = scalar.parents()
    model = await cast(st.Scalar, ds_model).async_value()
    assert isinstance(model, ensemble.StackingClassifier)
    X = await pandas_or_value(X)
    y = await pandas_or_value(y)
    fitted_model = model.fit(X, y, *args, **kwargs)
    return fitted_model


async def sk_stacking_regressor(
    scalar: st.Scalar, *args: Any, **kwargs: Any
) -> ensemble.StackingRegressor:
    (ds_model, X, y), _ = scalar.parents()
    model = await cast(st.Scalar, ds_model).async_value()
    assert isinstance(model, ensemble.StackingRegressor)
    X = await pandas_or_value(X)
    y = await pandas_or_value(y)
    fitted_model = model.fit(X, y, *args, **kwargs)
    return fitted_model


async def sk_voting_classifier(
    scalar: st.Scalar, *args: Any, **kwargs: Any
) -> ensemble.VotingClassifier:
    (ds_model, X, y), _ = scalar.parents()
    model = await cast(st.Scalar, ds_model).async_value()
    assert isinstance(model, ensemble.VotingClassifier)
    X = await pandas_or_value(X)
    y = await pandas_or_value(y)
    fitted_model = model.fit(X, y, *args, **kwargs)
    return fitted_model


async def sk_voting_regressor(
    scalar: st.Scalar, *args: Any, **kwargs: Any
) -> ensemble.VotingRegressor:
    (ds_model, X, y), _ = scalar.parents()
    model = await cast(st.Scalar, ds_model).async_value()
    assert isinstance(model, ensemble.VotingRegressor)
    X = await pandas_or_value(X)
    y = await pandas_or_value(y)
    fitted_model = model.fit(X, y, *args, **kwargs)
    return fitted_model


async def sk_hist_gradient_boosting_classifier(
    scalar: st.Scalar, *args: Any, **kwargs: Any
) -> ensemble.HistGradientBoostingClassifier:
    (ds_model, X, y), _ = scalar.parents()
    model = await cast(st.Scalar, ds_model).async_value()
    assert isinstance(model, ensemble.HistGradientBoostingClassifier)
    X = await pandas_or_value(X)
    y = await pandas_or_value(y)
    fitted_model = model.fit(X, y, *args, **kwargs)
    return fitted_model


async def sk_hist_gradient_boosting_regressor(
    scalar: st.Scalar, *args: Any, **kwargs: Any
) -> ensemble.HistGradientBoostingRegressor:
    (ds_model, X, y), _ = scalar.parents()
    model = await cast(st.Scalar, ds_model).async_value()
    assert isinstance(model, ensemble.HistGradientBoostingRegressor)
    X = await pandas_or_value(X)
    y = await pandas_or_value(y)
    fitted_model = model.fit(X, y, *args, **kwargs)
    return fitted_model


async def sk_cross_val_score(
    scalar: st.Scalar,
    *args: Any,
    **kwargs: Any,
) -> Any:
    (ds_model, X, y), _ = scalar.parents()
    model = await cast(st.Scalar, ds_model).async_value()
    X = await pandas_or_value(X)
    y = await pandas_or_value(y)
    return model_selection.cross_val_score(model, X, y, *args, **kwargs)


async def sk_train_test_split(
    scalar: st.Scalar,
    *args: Any,
    **kwargs: Any,
) -> Any:
    (X, y), _ = scalar.parents()
    X = await pandas_or_value(X)
    y = await pandas_or_value(y)
    return model_selection.train_test_split(X, y, *args, **kwargs)


async def sk_repeated_stratified_kfold(
    scalar: st.Scalar,
    *args: Any,
    **kwargs: Any,
) -> Any:
    (ds_model, X), _ = scalar.parents()
    model = await cast(st.Scalar, ds_model).async_value()
    assert isinstance(model, model_selection.RepeatedStratifiedKFold)
    X = await pandas_or_value(X)
    fitted_model = model.fit(X, *args, **kwargs)
    return fitted_model


# metrics
async def sk_accuracy_score(
    scalar: st.Scalar,
    *args: Any,
    **kwargs: Any,
) -> Any:
    (y_true, y_pred), _ = scalar.parents()
    y_true = await pandas_or_value(y_true)
    y_pred = await pandas_or_value(y_pred)
    return metrics.accuracy_score(y_true, y_pred, *args, **kwargs)


async def sk_average_precision_score(
    scalar: st.Scalar,
    *args: Any,
    **kwargs: Any,
) -> Any:
    (y_true, y_pred), _ = scalar.parents()
    y_true = await pandas_or_value(y_true)
    y_pred = await pandas_or_value(y_pred)
    return metrics.average_precision_score(y_true, y_pred, *args, **kwargs)


async def sk_classification_report(
    scalar: st.Scalar,
    *args: Any,
    **kwargs: Any,
) -> Any:
    (y_true, y_pred), _ = scalar.parents()
    y_true = await pandas_or_value(y_true)
    y_pred = await pandas_or_value(y_pred)
    return metrics.classification_report(y_true, y_pred, *args, **kwargs)


async def sk_confusion_matrix(
    scalar: st.Scalar,
    *args: Any,
    **kwargs: Any,
) -> Any:
    (y_true, y_pred), _ = scalar.parents()
    y_true = await pandas_or_value(y_true)
    y_pred = await pandas_or_value(y_pred)
    return metrics.confusion_matrix(y_true, y_pred, *args, **kwargs)


async def sk_f1_score(
    scalar: st.Scalar,
    *args: Any,
    **kwargs: Any,
) -> Any:
    (y_true, y_pred), _ = scalar.parents()
    y_true = await pandas_or_value(y_true)
    y_pred = await pandas_or_value(y_pred)
    return metrics.f1_score(y_true, y_pred, *args, **kwargs)


async def sk_plot_confusion_matrix(
    scalar: st.Scalar,
    *args: Any,
    **kwargs: Any,
) -> Any:
    (ds_model, X, y_true), _ = scalar.parents()
    model = await cast(st.Scalar, ds_model).async_value()
    X = await pandas_or_value(X)
    y_true = await pandas_or_value(y_true)
    return metrics.plot_confusion_matrix(model, X, y_true, *args, **kwargs)


async def sk_precision_recall_curve(
    scalar: st.Scalar,
    *args: Any,
    **kwargs: Any,
) -> Any:
    (y_true, y_scores), _ = scalar.parents()
    y_true = await pandas_or_value(y_true)
    y_scores = await pandas_or_value(y_scores)
    return metrics.precision_recall_curve(y_true, y_scores, *args, **kwargs)


async def sk_precision_score(
    scalar: st.Scalar,
    *args: Any,
    **kwargs: Any,
) -> Any:
    (y_true, y_pred), _ = scalar.parents()
    y_true = await pandas_or_value(y_true)
    y_pred = await pandas_or_value(y_pred)
    return metrics.precision_score(y_true, y_pred, *args, **kwargs)


async def sk_recall_score(
    scalar: st.Scalar,
    *args: Any,
    **kwargs: Any,
) -> Any:
    (y_true, y_pred), _ = scalar.parents()
    y_true = await pandas_or_value(y_true)
    y_pred = await pandas_or_value(y_pred)
    return metrics.recall_score(y_true, y_pred, *args, **kwargs)


async def sk_roc_auc_score(
    scalar: st.Scalar,
    *args: Any,
    **kwargs: Any,
) -> Any:
    (y_true, y_pred), _ = scalar.parents()
    y_true = await pandas_or_value(y_true)
    y_pred = await pandas_or_value(y_pred)
    return metrics.roc_auc_score(y_true, y_pred, *args, **kwargs)


async def sk_roc_curve(
    scalar: st.Scalar,
    *args: Any,
    **kwargs: Any,
) -> Any:
    (y_true, y_scores), _ = scalar.parents()
    y_true = await pandas_or_value(y_true)
    y_scores = await pandas_or_value(y_scores)
    return metrics.roc_curve(y_true, y_scores, *args, **kwargs)


async def sk_random_forest_classifier_predict(
    scalar: st.Scalar,
    *args: Any,
    **kwargs: Any,
) -> Any:
    (ds_model, X), _ = scalar.parents()
    model = await cast(st.Scalar, ds_model).async_value()
    assert isinstance(model, ensemble.RandomForestClassifier)
    X = await pandas_or_value(X)
    y_pred = model.predict(X, *args, **kwargs)
    return y_pred


async def sk_label_encoder_fit_transform(
    scalar: st.Scalar,
    *args: Any,
    **kwargs: Any,
) -> Any:
    (ds_model, X), _ = scalar.parents()
    model = await cast(st.Scalar, ds_model).async_value()
    assert isinstance(model, preprocessing.LabelEncoder)
    X = await pandas_or_value(X)
    X_transformed = model.fit_transform(X, *args, **kwargs)
    return X_transformed
