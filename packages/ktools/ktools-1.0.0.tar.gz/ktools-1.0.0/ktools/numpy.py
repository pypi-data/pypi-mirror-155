import numba as nb
import numpy as np


@nb.jit
def _ffill(out, current_loc, shape_idx, shape_len):
    if len(current_loc) == shape_len:
        if np.isnan(out[tuple(current_loc)]):
            previous_loc = current_loc.copy()
            previous_loc[-1] -= 1
            out[tuple(current_loc)] = out[tuple(previous_loc)]
    else:
        start_idx = 0 if len(current_loc) + 1 < shape_len else 1
        next_shape_idx = shape_idx + 1
        for idx in range(start_idx, out.shape[shape_idx]):
            next_loc = current_loc.copy()
            next_loc.append(idx)
            _ffill(out, next_loc, next_shape_idx, shape_len)


@nb.jit
def ffill(arr):
    out = arr.copy()
    shape_len = len(out.shape)
    _ffill(out, [], 0, shape_len)
    return out
