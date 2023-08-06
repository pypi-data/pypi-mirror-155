from __future__ import annotations

from typing import Any, cast

try:
    import xgboost  # type: ignore[import]
except ModuleNotFoundError:
    pass  # error message in typing.py

import sarus_data_spec.typing as st

from .utils import pandas_or_value


async def xgb_classifier(  # to be renamed ?
    scalar: st.Scalar, *args: Any, **kwargs: Any
) -> xgboost.XGBClassifier:
    (ds_model, X, y), _ = scalar.parents()
    model = await cast(st.Scalar, ds_model).async_value()
    assert isinstance(model, xgboost.XGBClassifier)
    X = await pandas_or_value(X)
    y = await pandas_or_value(y)
    fitted_model = model.fit(X, y, *args, **kwargs)
    return fitted_model


async def xgb_classifier_predict(
    scalar: st.Scalar,
    *args: Any,
    **kwargs: Any,
) -> Any:
    (ds_model, X), _ = scalar.parents()
    model = await cast(st.Scalar, ds_model).async_value()
    assert isinstance(model, xgboost.XGBClassifier)
    X = await pandas_or_value(X)
    y_pred = model.predict(X, *args, **kwargs)
    return y_pred
