"""
Parametric curve generation for cycloid, epicycloid, and hypocycloid curves.
All coordinates are unitless — the caller provides a rolling radius in whatever
unit system they need, and the output (x, y) pairs use the same unit.
"""

import math


def generate_cycloid(rolling_radius, num_arches, points_per_arch):
    """Standard cycloid: a circle of radius *r* rolling along a straight line.

    The curve starts at the origin (a cusp) and extends along the +X axis.
    Each arch spans 2*pi*r in X and reaches a peak height of 2*r.

    Returns a list of (x, y) tuples.
    """
    r = rolling_radius
    total_points = num_arches * points_per_arch
    t_max = num_arches * 2.0 * math.pi
    points = []
    for i in range(total_points + 1):
        t = t_max * i / total_points
        x = r * (t - math.sin(t))
        y = r * (1.0 - math.cos(t))
        points.append((x, y))
    return points


def generate_epicycloid(rolling_radius, num_cusps, points_per_cusp):
    """Epicycloid: a circle of radius *r* rolling **outside** a fixed circle.

    The base radius is computed as R = num_cusps * r so that the curve
    produces exactly *num_cusps* cusps in one full revolution (t: 0 → 2π).
    A single cusp (num_cusps=1) produces a cardioid.

    Returns a list of (x, y) tuples centred at the origin.
    """
    r = rolling_radius
    R = num_cusps * r
    k = (R + r) / r                       # = num_cusps + 1
    total_points = num_cusps * points_per_cusp
    t_max = 2.0 * math.pi
    points = []
    for i in range(total_points + 1):
        t = t_max * i / total_points
        x = (R + r) * math.cos(t) - r * math.cos(k * t)
        y = (R + r) * math.sin(t) - r * math.sin(k * t)
        points.append((x, y))
    return points


def generate_hypocycloid(rolling_radius, num_cusps, points_per_cusp):
    """Hypocycloid: a circle of radius *r* rolling **inside** a fixed circle.

    The base radius is computed as R = num_cusps * r so that the curve
    produces exactly *num_cusps* cusps in one full revolution (t: 0 → 2π).
    Special cases: 3 cusps → deltoid, 4 cusps → astroid.
    num_cusps must be >= 3 (2 cusps degenerates to a line segment).

    Returns a list of (x, y) tuples centred at the origin.
    """
    if num_cusps < 3:
        raise ValueError("Hypocycloid requires at least 3 cusps (2 degenerates to a line).")
    r = rolling_radius
    R = num_cusps * r
    k = (R - r) / r                       # = num_cusps - 1
    total_points = num_cusps * points_per_cusp
    t_max = 2.0 * math.pi
    points = []
    for i in range(total_points + 1):
        t = t_max * i / total_points
        x = (R - r) * math.cos(t) + r * math.cos(k * t)
        y = (R - r) * math.sin(t) - r * math.sin(k * t)
        points.append((x, y))
    return points
