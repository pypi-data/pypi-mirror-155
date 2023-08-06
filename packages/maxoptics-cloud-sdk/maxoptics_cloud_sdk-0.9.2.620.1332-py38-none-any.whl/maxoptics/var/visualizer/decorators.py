from functools import wraps

import numpy as np

from maxoptics.core.utils import decohints


@decohints
def nonzero(minvalue=1e-10):
    def _(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            ret = func(*args, **kwargs)
            data = ret["data"]
            ret["data"] = np.maximum(
                data, np.ones(shape=np.shape(data)) * minvalue
            ).tolist()
            return ret

        return wrapper

    return _
