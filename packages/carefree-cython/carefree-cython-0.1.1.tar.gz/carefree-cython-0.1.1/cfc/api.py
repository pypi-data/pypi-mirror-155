from .cython_substitute import naive_rolling_sum
from .cython_substitute import naive_rolling_min
from .cython_substitute import naive_rolling_max
from .cython_substitute import naive_ema
from .cython_substitute import naive_transform_flat_data_with_dict
from .cython_substitute import naive_flat_arr_to_float32
from .cython_substitute import naive_is_all_numeric

try:
    from .cython_wrappers import c_rolling_sum as rolling_sum
    from .cython_wrappers import c_rolling_min as rolling_min
    from .cython_wrappers import c_rolling_max as rolling_max
    from .cython_wrappers import c_ema as ema
    from .cython_wrappers import (
        c_transform_flat_data_with_dict as transform_flat_data_with_dict,
    )
    from .cython_wrappers import c_flat_arr_to_float32 as flat_arr_to_float32
    from .cython_wrappers import c_is_all_numeric as is_all_numeric
except ImportError:
    rolling_sum = naive_rolling_sum
    rolling_min = naive_rolling_min
    rolling_max = naive_rolling_max
    ema = naive_ema
    transform_flat_data_with_dict = naive_transform_flat_data_with_dict
    flat_arr_to_float32 = naive_flat_arr_to_float32
    is_all_numeric = naive_is_all_numeric


__all__ = [
    "rolling_sum",
    "rolling_min",
    "rolling_max",
    "ema",
    "transform_flat_data_with_dict",
    "flat_arr_to_float32",
    "is_all_numeric",
    "naive_rolling_sum",
    "naive_rolling_min",
    "naive_rolling_max",
    "naive_ema",
    "naive_transform_flat_data_with_dict",
    "naive_flat_arr_to_float32",
    "naive_is_all_numeric",
]
