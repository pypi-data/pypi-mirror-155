"""The `component_checks` module is an utils module for 'component-scope' constraints."""
from maxoptics.macros import (
    XYZ_3D,
    X_Normal,
    Y_Normal,
    Z_Normal,
    Point,
    X_Linear,
    Y_Linear,
    Z_Linear,
)


def get_monitor_type(x, y, z):
    """Return monitor_type with given x, y, z.

    Args:
        x (float): x_span.
        y (float): y_span.
        z (float): z_span.

    Returns:
        Macro: one of XYZ_3D, Z_Normal, Y_Normal, X_Normal, X_Linear, Y_Linear, Z_Linear and Point.
    """

    # binary like
    _1_0_rep = tuple(1 if _ != 0 else 0 for _ in [x, y, z])

    return {
        (1, 1, 1): XYZ_3D,
        (1, 1, 0): Z_Normal,
        (1, 0, 1): Y_Normal,
        (0, 1, 1): X_Normal,
        (1, 0, 0): X_Linear,
        (0, 1, 0): Y_Linear,
        (0, 0, 1): Z_Linear,
        (0, 0, 0): Point,
    }[_1_0_rep]
