

def lerp(a: float, b: float, t: float) -> float:
    """
    Returns a linear interpolation between `a` and `b`.

    Args:
        a (float): the starting value
        b (float): the ending value
        t (float): a time variable between 0 and 1, where 0 will return value
                   `a` and 1 will return value `b`.

    Returns:
        float: a number between `a` and `b`.
    """
    assert 0 <= t <= 1, 't must be between 0 and 1'
    return a + (t * (b - a))
    # return (a * (1.0 - f)) + (b * f)  # more precise implementation
