"""The `heatmap` module provides a simple heatmap implementation with `matplotlib.pyplot`.

How to Use
----------

x, y, Z = data.raw_data["horizontal"], data.raw_data["vertical"], data.raw_data["data"]
fig, ax = heatmap(x, y, Z)

"""
from typing import Tuple, Union, List

import matplotlib.pyplot as plt
from matplotlib.pyplot import Axes, Figure

import numpy as np
from numpy import ndarray


def heatmap(x, y, Z: Union[List[List[float]], ndarray]) -> Tuple[Figure, Axes]:
    """This is a small example of visualizing data. You can build your own
    visualization method referring to this method.

    .. code-block:: python

        x, y, Z = data.raw_data["horizontal"], data.raw_data["vertical"], data.raw_data["data"]
        fig, ax = heatmap(x, y, Z)

    Args:
        x (list[float]): A 1-D array.

        y (list[float]): A 1-D array.

        Z (list[list[float]] | ndarray): A 2-D array or numpy array.

    Returns:
        tuple[Figure, Axes]: fig, ax
    """
    if len(x) == 1:
        x = [x[0] - 0.001, x[0] + 0.001]
    elif len(x) == len(Z[0]):
        x = [x[0] - (x[1] - x[0])] + x

    if len(y) == 1:
        y = [y[0] - 0.001, y[0] + 0.001]
    elif len(y) == len(Z):
        y = [y[0] - (y[1] - y[0])] + y

    X, Y = np.meshgrid(x, y)
    fig, ax = plt.subplots()
    pmesh = ax.pcolormesh(X, Y, Z, cmap="jet")
    plt.colorbar(pmesh, ax=ax)

    return fig, ax
