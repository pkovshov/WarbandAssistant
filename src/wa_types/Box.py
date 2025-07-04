from typing import NamedTuple, Tuple

from typeguard import typechecked


class Box(NamedTuple):
    """LEFT, TOP, RIGHT, BOTTOM
    Tests:
    >>> box = Box(0, 100, 200, 250)
    >>> print(box.l, box.t, box.r, box.b)
    0 100 200 250
    >>> print(*box)
    0 100 200 250
    >>> for idx in range(len(box)): print(box[idx], end=',')
    0,100,200,250,
    >>> for itm in box: print(itm, end=',')
    0,100,200,250,
    >>> print(list(box))
    [0, 100, 200, 250]
    >>> print(box.slice)
    (slice(100, 250, None), slice(0, 200, None))
    """
    l: int  # Left coordinate
    t: int  # Top coordinate
    r: int  # Right coordinate
    b: int  # Bottom coordinate

    @property
    @typechecked
    def slice(self) -> Tuple[slice, slice]:
        return slice(self.t, self.b), slice(self.l, self.r)


if __name__ == "__main__":
    import doctest
    doctest.testmod(optionflags=doctest.IGNORE_EXCEPTION_DETAIL)
