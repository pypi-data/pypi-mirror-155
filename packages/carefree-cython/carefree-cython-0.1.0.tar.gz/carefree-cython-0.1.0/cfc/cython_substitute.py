import math

import numpy as np

from typing import Any
from typing import Dict
from functools import partial
from cftool.misc import is_numeric
from cftool.misc import StrideArray


def naive_rolling_sum(
    array: np.ndarray,
    window: int,
    mean: bool,
    axis: int = -1,
) -> np.ndarray:
    if window > array.shape[axis]:
        raise ValueError("`window` is too large for current array")
    pad_width = [[0, 0] for _ in range(len(array.shape))]
    pad_width[axis][0] = 1
    pad = partial(np.pad, mode="constant", pad_width=pad_width)
    nan_mask = np.isnan(array).astype(np.float32)
    nan_mask = np.swapaxes(pad(nan_mask, constant_values=1.0), axis, -1)
    arr = np.swapaxes(pad(array, constant_values=0.0), axis, -1)

    def _rolling_sum(arr_: np.ndarray) -> np.ndarray:
        cumsum = np.nancumsum(arr_, axis=-1)
        return cumsum[..., window:] - cumsum[..., :-window]

    arr_rolled, nan_rolled = map(_rolling_sum, [arr, nan_mask])
    all_nan_mask = nan_rolled == window
    dtype = arr_rolled.dtype
    arr_rolled = arr_rolled.astype(np.float64)
    if not mean:
        arr_rolled[all_nan_mask] = np.nan
    else:
        nan_rolled[all_nan_mask] = np.nan
        arr_rolled /= window - nan_rolled
    return np.swapaxes(arr_rolled.astype(dtype), axis, -1)


def naive_rolling_min(array: np.ndarray, window: int, axis: int = -1) -> np.ndarray:
    while axis < 0:
        axis += len(array.shape)
    return np.nanmin(StrideArray(array).roll(window, axis=axis), axis + 1)


def naive_rolling_max(array: np.ndarray, window: int, axis: int = -1) -> np.ndarray:
    while axis < 0:
        axis += len(array.shape)
    return np.nanmax(StrideArray(array).roll(window, axis=axis), axis + 1)


def naive_ema(array: np.ndarray, window: int, axis: int = -1) -> np.ndarray:
    shape = list(array.shape)
    while axis < 0:
        axis += len(shape)
    rolled = StrideArray(array).roll(window, axis=axis)
    rolled_axis = axis + 1
    shape.insert(rolled_axis, window)
    new_shape = [1] * len(shape)
    new_shape[rolled_axis] = -1
    ratio = 2.0 / (window + 1.0)
    multipliers = ((1.0 - ratio) ** np.arange(window))[::-1].reshape(new_shape)
    return ratio * np.nansum(rolled * multipliers, rolled_axis)


def naive_transform_flat_data_with_dict(
    flat_data: np.ndarray,
    transform_dict: Dict[Any, Any],
    need_truncate: bool,
) -> np.ndarray:
    nan_value = transform_dict.get("nan", 0)
    oob_value = nan_value if need_truncate else 0
    for i, elem in enumerate(flat_data):
        elem = float(elem)
        if math.isnan(elem):
            flat_data[i] = nan_value
        else:
            flat_data[i] = transform_dict.get(elem, oob_value)
    return flat_data


def naive_is_all_numeric(array: np.ndarray) -> bool:
    return all(map(is_numeric, array))


def naive_flat_arr_to_float32(array: np.ndarray) -> np.ndarray:
    return np.asarray(array, np.float32)


__all__ = [
    "naive_rolling_sum",
    "naive_rolling_min",
    "naive_rolling_max",
    "naive_ema",
    "naive_transform_flat_data_with_dict",
    "naive_is_all_numeric",
    "naive_flat_arr_to_float32",
]
