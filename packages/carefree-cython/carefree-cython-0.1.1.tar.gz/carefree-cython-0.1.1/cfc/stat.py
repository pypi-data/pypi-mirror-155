import numpy as np

from functools import partial

from .api import ema
from .api import rolling_min
from .api import rolling_max
from .api import rolling_sum
from .api import naive_ema
from .api import naive_rolling_min
from .api import naive_rolling_max
from .api import naive_rolling_sum


class RollingStat:
    @staticmethod
    def _sum(
        arr: np.ndarray,
        window: int,
        *,
        mean: bool,
        axis: int = -1,
    ) -> np.ndarray:
        if len(arr.shape) == 1 and axis in (0, -1):
            return rolling_sum(arr, window, mean)
        if rolling_sum is naive_rolling_sum:
            return naive_rolling_sum(arr, window, mean, axis)
        rolling_sum_ = partial(rolling_sum, window=window, mean=mean)
        return np.apply_along_axis(rolling_sum_, axis, arr)

    @staticmethod
    def sum(arr: np.ndarray, window: int, *, axis: int = -1) -> np.ndarray:
        return RollingStat._sum(arr, window, mean=False, axis=axis)

    @staticmethod
    def mean(arr: np.ndarray, window: int, *, axis: int = -1) -> np.ndarray:
        return RollingStat._sum(arr, window, mean=True, axis=axis)

    @staticmethod
    def std(arr: np.ndarray, window: int, *, axis: int = -1) -> np.ndarray:
        mean = RollingStat.mean(arr, window, axis=axis)
        second_order = RollingStat.sum(arr**2, window, axis=axis)
        return np.sqrt(second_order / float(window) - mean**2)

    @staticmethod
    def min(arr: np.ndarray, window: int, *, axis: int = -1) -> np.ndarray:
        if len(arr.shape) == 1 and axis in (0, -1):
            return rolling_min(arr, window)
        return naive_rolling_min(arr, window, axis)

    @staticmethod
    def max(arr: np.ndarray, window: int, *, axis: int = -1) -> np.ndarray:
        if len(arr.shape) == 1 and axis in (0, -1):
            return rolling_max(arr, window)
        return naive_rolling_max(arr, window, axis)

    @staticmethod
    def ema(arr: np.ndarray, window: int, *, axis: int = -1) -> np.ndarray:
        if len(arr.shape) == 1 and axis in (0, -1):
            return ema(arr, window)
        if ema is naive_ema:
            return naive_ema(arr, window, axis)
        return np.apply_along_axis(partial(ema, window=window), axis, arr)


__all__ = [
    "RollingStat",
]
