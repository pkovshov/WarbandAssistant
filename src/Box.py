from typing import NamedTuple


class Box(NamedTuple):
    """LEFT, TOP, RIGHT, BOTTOM"""
    l: int  # Left coordinate
    t: int  # Top coordinate
    r: int  # Right coordinate
    b: int  # Bottom coordinate
