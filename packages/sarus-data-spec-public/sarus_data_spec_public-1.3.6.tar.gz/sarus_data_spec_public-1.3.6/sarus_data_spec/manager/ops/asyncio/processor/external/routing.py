from typing import Any, AsyncIterator
import pickle as pkl

import pandas as pd
import pyarrow as pa

from sarus_data_spec.manager.asyncio.utils import async_iter
import sarus_data_spec.protobuf as sp
import sarus_data_spec.typing as st

from .numpy import np_mean, np_std
from .pandas import (
    pd_abs,
    pd_agg,
    pd_any,
    pd_apply,
    pd_concat,
    pd_corr,
    pd_count,
    pd_describe,
    pd_drop,
    pd_droplevel,
    pd_eq,
    pd_fillna,
    pd_get_dummies,
    pd_join,
    pd_kurtosis,
    pd_loc,
    pd_mad,
    pd_mean,
    pd_median,
    pd_quantile,
    pd_rename,
    pd_round,
    pd_select_dtypes,
    pd_skew,
    pd_sort_values,
    pd_std,
    pd_sum,
    pd_to_dict,
    pd_transpose,
    pd_unique,
    pd_value_counts,
)
from .pandas_profiling import pd_profile_report
from .sklearn import (
    sk_accuracy_score,
    sk_adaboost_classifier,
    sk_adaboost_regressor,
    sk_affinity_propagation,
    sk_agglomerative_clustering,
    sk_average_precision_score,
    sk_bagging_classifier,
    sk_bagging_regressor,
    sk_birch,
    sk_classification_report,
    sk_confusion_matrix,
    sk_cross_val_score,
    sk_dbscan,
    sk_extra_trees_classifier,
    sk_extra_trees_regressor,
    sk_f1_score,
    sk_feature_agglomeration,
    sk_fit,
    sk_gradient_boosting_classifier,
    sk_gradient_boosting_regressor,
    sk_hist_gradient_boosting_classifier,
    sk_hist_gradient_boosting_regressor,
    sk_isolation_forest,
    sk_kmeans,
    sk_label_encoder_fit_transform,
    sk_mean_shift,
    sk_minibatch_kmeans,
    sk_onehot,
    sk_optics,
    sk_pca,
    sk_plot_confusion_matrix,
    sk_precision_recall_curve,
    sk_precision_score,
    sk_random_forest_classifier,
    sk_random_forest_classifier_predict,
    sk_random_forest_regressor,
    sk_random_trees_embedding,
    sk_recall_score,
    sk_repeated_stratified_kfold,
    sk_roc_auc_score,
    sk_roc_curve,
    sk_scale,
    sk_spectral_biclustering,
    sk_spectral_clustering,
    sk_spectral_coclustering,
    sk_stacking_classifier,
    sk_stacking_regressor,
    sk_train_test_split,
    sk_voting_classifier,
    sk_voting_regressor,
)
from .std import (
    _abs,
    _and,
    _or,
    _round,
    add,
    div,
    getitem,
    greater_equal,
    greater_than,
    invert,
    length,
    lower_equal,
    lower_than,
    modulo,
    mul,
    neg,
    not_equal,
    pos,
    sub,
)
from .xgboost import xgb_classifier, xgb_classifier_predict


async def arrow_external(
    dataset: st.Dataset, batch_size: int
) -> AsyncIterator[pa.RecordBatch]:
    """Call external and convert the result to a RecordBatch iterator.

    We consider that external ops results are Datasets. For now, we consider
    that pandas.DataFrame are Datasets. For instance, the pd.loc operation only
    selects a subset of a Dataset and so is a Dataset.

    We call the implementation of `external` which returns arbitrary values,
    check that the result is indeed a DataFrame and convert it to a RecordBatch
    iterator.
    """
    val = await external(dataset)
    if isinstance(val, pd.DataFrame):
        return async_iter(
            pa.Table.from_pandas(val).to_batches(max_chunksize=batch_size)
        )

    else:
        raise TypeError(f"Cannot convert {type(val)} to Arrow batches.")


async def external(dataspec: st.DataSpec) -> Any:
    """Route an externally transformed Dataspec to its implementation."""
    transform_spec = dataspec.transform().protobuf().spec
    external_op = sp.Transform.ExternalOp.Name(transform_spec.external.op)
    implemented_ops = {
        "ADD": add,
        "MUL": mul,
        "SUB": sub,
        "DIV": div,
        "INVERT": invert,
        "GETITEM": getitem,
        "LEN": length,
        "GT": greater_than,
        "GE": greater_equal,
        "LT": lower_than,
        "LE": lower_equal,
        "NE": not_equal,
        "MOD": modulo,
        "ROUND": _round,
        "AND": _and,
        "OR": _or,
        "ABS": _abs,
        "POS": pos,
        "NEG": neg,
        "PD_LOC": pd_loc,
        "PD_EQ": pd_eq,
        "PD_MEAN": pd_mean,
        "PD_STD": pd_std,
        "PD_ANY": pd_any,
        "PD_DESCRIBE": pd_describe,
        "PD_SELECT_DTYPES": pd_select_dtypes,
        "NP_MEAN": np_mean,
        "NP_STD": np_std,
        "PD_PROFILE_REPORT": pd_profile_report,
        "SK_FIT": sk_fit,
        "SK_SCALE": sk_scale,
        'PD_QUANTILE': pd_quantile,
        'PD_SUM': pd_sum,
        'PD_FILLNA': pd_fillna,
        'PD_ROUND': pd_round,
        'PD_RENAME': pd_rename,
        'PD_COUNT': pd_count,
        'PD_TRANSPOSE': pd_transpose,
        'PD_UNIQUE': pd_unique,
        'PD_VALUE_COUNTS': pd_value_counts,
        'PD_TO_DICT': pd_to_dict,
        'PD_APPLY': pd_apply,
        'PD_MEDIAN': pd_median,
        'PD_ABS': pd_abs,
        'PD_MAD': pd_mad,
        'PD_SKEW': pd_skew,
        'PD_KURTOSIS': pd_kurtosis,
        'PD_AGG': pd_agg,
        'PD_DROPLEVEL': pd_droplevel,
        'PD_SORT_VALUES': pd_sort_values,
        'PD_DROP': pd_drop,
        'PD_CORR': pd_corr,
        "SK_ONEHOT": sk_onehot,
        "SK_PCA": sk_pca,
        # cluster
        "SK_AFFINITY_PROPAGATION": sk_affinity_propagation,
        "SK_AGGLOMERATIVE_CLUSTERING": sk_agglomerative_clustering,
        "SK_BIRCH": sk_birch,
        "SK_DBSCAN": sk_dbscan,
        "SK_FEATURE_AGGLOMERATION": sk_feature_agglomeration,
        "SK_KMEANS": sk_kmeans,
        "SK_MINIBATCH_KMEANS": sk_minibatch_kmeans,
        "SK_MEAN_SHIFT": sk_mean_shift,
        "SK_OPTICS": sk_optics,
        "SK_SPECTRAL_CLUSTERING": sk_spectral_clustering,
        "SK_SPECTRAL_BICLUSTERING": sk_spectral_biclustering,
        "SK_SPECTRAL_COCLUSTERING": sk_spectral_coclustering,
        # ensemble
        "SK_ADABOOST_CLASSIFIER": sk_adaboost_classifier,
        "SK_ADABOOST_REGRESSOR": sk_adaboost_regressor,
        "SK_BAGGING_CLASSIFIER": sk_bagging_classifier,
        "SK_BAGGING_REGRESSOR": sk_bagging_regressor,
        "SK_EXTRA_TREES_CLASSIFIER": sk_extra_trees_classifier,
        "SK_EXTRA_TREES_REGRESSOR": sk_extra_trees_regressor,
        "SK_GRADIENT_BOOSTING_CLASSIFIER": sk_gradient_boosting_classifier,
        "SK_GRADIENT_BOOSTING_REGRESSOR": sk_gradient_boosting_regressor,
        "SK_ISOLATION_FOREST": sk_isolation_forest,
        "SK_RANDOM_FOREST_CLASSIFIER": sk_random_forest_classifier,
        "SK_RANDOM_FOREST_REGRESSOR": sk_random_forest_regressor,
        "SK_RANDOM_TREES_EMBEDDING": sk_random_trees_embedding,
        "SK_STACKING_CLASSIFIER": sk_stacking_classifier,
        "SK_STACKING_REGRESSOR": sk_stacking_regressor,
        "SK_VOTING_CLASSIFIER": sk_voting_classifier,
        "SK_VOTING_REGRESSOR": sk_voting_regressor,
        "SK_HIST_GRADIENT_BOOSTING_CLASSIFIER": sk_hist_gradient_boosting_classifier,
        "SK_HIST_GRADIENT_BOOSTING_REGRESSOR": sk_hist_gradient_boosting_regressor,
        # model selection
        "SK_CROSS_VAL_SCORE": sk_cross_val_score,
        "SK_TRAIN_TEST_SPLIT": sk_train_test_split,
        "SK_REPEATED_STRATIFIED_KFOLD": sk_repeated_stratified_kfold,
        # xgb
        "XGB_CLASSIFIER": xgb_classifier,
        "XGB_CLASSIFIER_PREDICT": xgb_classifier_predict,
        # pandas 2
        "PD_GET_DUMMIES": pd_get_dummies,
        "PD_JOIN": pd_join,
        "PD_CONCAT": pd_concat,
        # metrics
        "SK_ACCURACY_SCORE": sk_accuracy_score,
        "SK_AVERAGE_PRECISION_SCORE": sk_average_precision_score,
        "SK_CLASSIFICATION_REPORT": sk_classification_report,
        "SK_CONFUSION_MATRIX": sk_confusion_matrix,
        "SK_F1_SCORE": sk_f1_score,
        "SK_PLOT_CONFUSION_MATRIX": sk_plot_confusion_matrix,
        "SK_PRECISION_RECALL_CURVE": sk_precision_recall_curve,
        "SK_PRECISION_SCORE": sk_precision_score,
        "SK_RECALL_SCORE": sk_recall_score,
        "SK_ROC_AUC_SCORE": sk_roc_auc_score,
        "SK_ROC_CURVE": sk_roc_curve,
        # ensemble predict
        "SK_RANDOM_FOREST_CLASSIFIER_PREDICT": sk_random_forest_classifier_predict,
        "SK_LABEL_ENCODER_FIT_TRANSFORM": sk_label_encoder_fit_transform,
    }
    if external_op not in implemented_ops:
        raise NotImplementedError(
            f"{external_op} not in {list(implemented_ops.keys())}"
        )

    args = pkl.loads(transform_spec.external.arguments)
    kwargs = pkl.loads(transform_spec.external.named_arguments)
    func = implemented_ops[external_op]
    return await func(dataspec, *args, **kwargs)  # type: ignore
