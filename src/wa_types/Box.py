from typing import NamedTuple, Tuple

from wa_typechecker import typechecked

from .Resolution import Resolution


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
    >>> print(box.resolution)
    Resolution(width=200, height=150)
    """
    l: int  # Left coordinate
    t: int  # Top coordinate
    r: int  # Right coordinate
    b: int  # Bottom coordinate

    @property
    def slice(self) -> Tuple[slice, slice]:
        return slice(self.t, self.b), slice(self.l, self.r)

    @property
    def resolution(self) -> Resolution:
        return Resolution(self.r - self.l, self.b - self.t)

    @property
    def point(self) -> Tuple[int, int]:
        return self.l, self.t

    def __add__(self, offset: Tuple[int, int]) -> "Box":
        x, y = offset
        return Box(l=self.l + x,
                   t=self.t + y,
                   r=self.r + x,
                   b=self.b + y)

    __radd__ = __add__

    def __contains__(self, box: "Box") -> bool:
        """
        Tests:
        >>> b1 = Box(100, 200, 300, 400)
        >>> b2 = Box(130, 230, 270, 370)
        >>> b1 in b1
        True
        >>> b2 in b1
        True
        >>> b1 in b2
        False
        """
        return (self.l <= box.l and
                self.t <= box.t and
                self.r >= box.r and
                self.b >= box.b)


if __name__ == "__main__":
    box = Box(100, 200, 300, 400)
    print(box)
    point = Box.point
    print(point)
    # import doctest
    # doctest.testmod(optionflags=doctest.IGNORE_EXCEPTION_DETAIL)
